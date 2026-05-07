"""Phase 2 ε — 폰 통합 runtime.

v2 abstention rule을 chat_stream에 monkey-patch하여 실데이터 누적.
Termux 친화: 의존성 추가 0, 단일 파일.

CLI:
  python phase2_runtime.py                       # interactive chat
  python phase2_runtime.py --log /path/to/log.jsonl
  python phase2_runtime.py --once "안녕"           # 한 입력만 분석

v41 codebase 기존 코드 수정 0. monkey-patch만.
"""
import sys, os, json, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


# ── v2 abstention rule (검증됨 N=28) ─────────────────────────────────
T_CONFIDENCE = 0.55
DELTA_AMBIGUITY = 0.50      # axis dominance gap threshold
FLOOR_DOMINANCE = 0.80      # max_axis 의심 시작
CEILING_ANCHOR_EXACT = 0.99 # token=anchor 정확매칭 예외
LOW_SUPPORT_THRESHOLD = 5
LOW_SUPPORT_FACTOR = 0.60

DEFAULT_LOG = os.path.expanduser("~/eve_logs/runtime_stream.jsonl")


def abstention_v2(embed_top, embed_conf, embed_scores, tokens, word_counts):
    """v2 abstention decision. Returns {decision, metrics}."""
    if embed_top is None:
        return {"decision": "SILENT_NO_EMBED",
                "metrics": {"confidence": None, "max_axis": None, "second_axis": None,
                            "axis_gap": None, "min_support": 0, "adjusted_confidence": None}}
    
    scores = [v for v in (embed_scores or {}).values() if v is not None]
    if not scores:
        return {"decision": "SILENT_NO_EMBED",
                "metrics": {"confidence": embed_conf or 0, "max_axis": None,
                            "second_axis": None, "axis_gap": None, "min_support": 0,
                            "adjusted_confidence": None}}
    
    sorted_s = sorted(scores, reverse=True)
    max_axis = sorted_s[0]
    second_axis = sorted_s[1] if len(sorted_s) > 1 else 0.0
    axis_gap = max_axis - second_axis
    
    counts = [word_counts.get(t, 0) for t in tokens] if tokens else []
    min_support = min(counts) if counts else 0
    
    confidence = embed_conf or 0.0
    adj_conf = confidence * LOW_SUPPORT_FACTOR if min_support < LOW_SUPPORT_THRESHOLD else confidence
    
    metrics = {
        "confidence": round(confidence, 3),
        "adjusted_confidence": round(adj_conf, 3),
        "max_axis": round(max_axis, 3),
        "second_axis": round(second_axis, 3),
        "axis_gap": round(axis_gap, 3),
        "min_support": min_support,
    }
    
    # decision rules (in order, first match wins)
    
    # (1) anchor exact match — 정확매칭 보호
    if max_axis >= CEILING_ANCHOR_EXACT:
        return {"decision": "SPEAK_ANCHOR_EXACT", "metrics": metrics}
    
    # (2) low confidence (low_support adjusted)
    if adj_conf < T_CONFIDENCE:
        return {"decision": "SILENT_LOW_CONF", "metrics": metrics}
    
    # (3) axis dominance — strong but lone signal (false coherence A: cluster gravity)
    if FLOOR_DOMINANCE < max_axis < CEILING_ANCHOR_EXACT and axis_gap > DELTA_AMBIGUITY:
        return {"decision": "SILENT_DOMINANCE", "metrics": metrics}
    
    # (4) weak support — max signal not strong enough
    if max_axis < FLOOR_DOMINANCE:
        return {"decision": "SILENT_WEAK_SUPPORT", "metrics": metrics}
    
    return {"decision": "SPEAK_WITH_TAG", "metrics": metrics}


# ── engine wrapper (monkey-patch chat_stream) ─────────────────────────
def wrap_engine_with_logging(engine, log_path):
    """engine.chat_stream을 wrap. SR/embedding 수정 X, hook만 추가."""
    from adapters.shadow_logger import ShadowLogger
    
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    se = engine.self_embedding
    sl = ShadowLogger(log_path + ".tmp")
    original_chat_stream = engine.chat_stream
    
    def logged_chat_stream(text):
        # SR 응답 (chunks) — 원본 그대로
        chunks = list(original_chat_stream(text))
        response = "".join(chunks)
        
        # 후 분석 (engine state 변경 없음, 측정만)
        try:
            log_data = sl.analyze(engine, input_text=text,
                                  sr_situation=None, sr_builder=None,
                                  winner_path=None, winner=None)
            
            decision = abstention_v2(
                embed_top=log_data.get("embedding_top_intent"),
                embed_conf=log_data.get("embedding_confidence"),
                embed_scores={k: v["score"] for k, v in log_data.get("interpretation", {}).items()},
                tokens=log_data.get("tokens", []),
                word_counts=se.word_counts,
            )
            
            entry = {
                "t": round(time.time(), 3),
                "input": text,
                "tokens": log_data.get("tokens", []),
                "vocab_coverage": log_data.get("vocab_coverage"),
                "embed_label": log_data.get("embedding_top_intent"),
                "embed_scores": {k: (round(v["score"], 3) if v.get("score") is not None else None)
                                 for k, v in log_data.get("interpretation", {}).items()},
                "decision": decision["decision"],
                "metrics": decision["metrics"],
                "sr_response": response,
            }
            
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
            # 마지막 decision을 engine에 stash (CLI 출력용)
            engine._last_phase2_decision = decision
        except Exception as e:
            engine._last_phase2_decision = {"decision": "ANALYSIS_ERROR",
                                             "metrics": {"error": str(e)}}
        
        # tmp 정리
        tmp = log_path + ".tmp"
        if os.path.exists(tmp):
            try: os.remove(tmp)
            except: pass
        
        # 원본 chunks 반환 (generator로 — chat_stream 호환)
        for c in chunks:
            yield c
    
    engine.chat_stream = logged_chat_stream
    return engine


# ── CLI ───────────────────────────────────────────────────────────────
def cli():
    p = argparse.ArgumentParser()
    p.add_argument("--log", default=DEFAULT_LOG)
    p.add_argument("--once", default=None, help="한 입력만 분석하고 종료")
    args = p.parse_args()
    
    print(f"[init] log → {args.log}")
    print("[init] engine 빌드 중…")
    from main import build_full_engine
    engine = build_full_engine()
    wrap_engine_with_logging(engine, args.log)
    print("[init] v2 abstention rule active\n")
    
    def run_one(text):
        chunks = list(engine.chat_stream(text))
        response = "".join(chunks)
        d = engine._last_phase2_decision
        m = d["metrics"]
        em = m.get("max_axis")
        gap = m.get("axis_gap")
        conf = m.get("confidence")
        em_str = f"{em:.2f}" if em is not None else "  -"
        gap_str = f"{gap:.2f}" if gap is not None else "  -"
        conf_str = f"{conf:.2f}" if conf is not None else "  -"
        print(f"  EVE: {response}")
        if d['decision'] == "ANALYSIS_ERROR":
            print(f"  [ANALYSIS_ERROR] {m.get('error')}\n")
        else:
            print(f"  [{d['decision']}] conf={conf_str} max={em_str} gap={gap_str}\n")
    
    if args.once:
        run_one(args.once)
        return
    
    print("준비됨. 종료: Ctrl+C 또는 'exit'\n")
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not text: continue
        if text in ("exit", "quit", "종료"): break
        try:
            run_one(text)
        except Exception as e:
            print(f"  [error] {e}\n")


if __name__ == "__main__":
    cli()

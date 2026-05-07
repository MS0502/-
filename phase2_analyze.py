"""Phase 2 ε — runtime_stream.jsonl 분석.

3 KPI:
  KPI 1 — silent_ratio: 안정성 (target 70~85%)
  KPI 2 — false_permission_rate: 위험 케이스 SPEAK된 비율 (수동 검토)
  KPI 3 — useful_silence_rate: 가치 입력이 silent된 비율 (수동 검토)

usage:
  python phase2_analyze.py [--log /path/to/log.jsonl]
"""
import sys, os, json, argparse
from collections import Counter

DEFAULT_LOG = os.path.expanduser("~/eve_logs/runtime_stream.jsonl")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", default=DEFAULT_LOG)
    p.add_argument("--tail", type=int, default=None, help="마지막 N개만 분석")
    args = p.parse_args()
    
    if not os.path.exists(args.log):
        print(f"로그 없음: {args.log}")
        return
    
    with open(args.log, encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    if args.tail:
        rows = rows[-args.tail:]
    
    n = len(rows)
    if n == 0:
        print("로그 비어있음")
        return
    
    print(f"분석 대상: {n}개 turn (log: {args.log})\n")
    
    # === KPI 1: silent ratio ===
    decisions = Counter(r["decision"] for r in rows)
    silent_count = sum(c for d, c in decisions.items() if d.startswith("SILENT"))
    speak_count = n - silent_count
    silent_ratio = silent_count / n if n else 0
    
    print(f"[KPI 1] silent ratio: {silent_ratio:.0%}  (target 70~85%)")
    if 0.70 <= silent_ratio <= 0.85:
        print(f"  → 안정 영역")
    elif silent_ratio < 0.70:
        print(f"  → 과발화 — gravity / anchor 재설계 후보")
    else:
        print(f"  → 과침묵 — Δ/T 재조정 후보")
    
    print(f"\n  decision 분포:")
    for d, c in decisions.most_common():
        bar = "█" * int(c / n * 40)
        print(f"    {d:>22s}: {c:>3d} ({c/n:>4.0%}) {bar}")
    
    # === SPEAK된 케이스 list (수동 검토용) ===
    speak_rows = [r for r in rows if not r["decision"].startswith("SILENT")]
    print(f"\n[SPEAK된 케이스 — KPI 2 (false permission) 수동 검토]")
    if speak_rows:
        for r in speak_rows:
            m = r["metrics"]
            em = r.get("embed_label") or "-"
            mx = m.get("max_axis")
            mx_str = f"{mx:.2f}" if mx is not None else "-"
            print(f"  [{r['decision']:<22s}] {r['input'][:30]:<32s} embed={em}({mx_str})")
    else:
        print("  (없음 — 모두 silent)")
    
    # === SILENT된 케이스 중 strong embed_label (KPI 3 후보) ===
    silent_rows = [r for r in rows if r["decision"].startswith("SILENT") and r["decision"] != "SILENT_NO_EMBED"]
    silent_with_signal = [r for r in silent_rows
                          if r["metrics"].get("max_axis") is not None
                          and r["metrics"]["max_axis"] > 0.4]
    print(f"\n[SILENT 케이스 중 의미 신호 있던 입력 — KPI 3 (useful silence) 후보]")
    print(f"  ({len(silent_with_signal)}/{len(silent_rows)})")
    for r in silent_with_signal[:15]:
        m = r["metrics"]
        em = r.get("embed_label") or "-"
        mx = m.get("max_axis"); gap = m.get("axis_gap")
        mx_str = f"{mx:.2f}" if mx is not None else "-"
        gap_str = f"{gap:.2f}" if gap is not None else "-"
        print(f"  [{r['decision']:<22s}] {r['input'][:30]:<32s} embed={em}({mx_str}) gap={gap_str}")
    
    # === 메트릭 요약 ===
    confs = [r["metrics"]["confidence"] for r in rows if r["metrics"].get("confidence") is not None]
    gaps = [r["metrics"]["axis_gap"] for r in rows if r["metrics"].get("axis_gap") is not None]
    if confs:
        print(f"\n[Confidence 분포]")
        print(f"  range: {min(confs):.2f} ~ {max(confs):.2f}, mean: {sum(confs)/len(confs):.2f}")
    if gaps:
        print(f"[Axis gap 분포]")
        print(f"  range: {min(gaps):.2f} ~ {max(gaps):.2f}, mean: {sum(gaps)/len(gaps):.2f}")
    
    # === ε 단계 다음 분기 추정 ===
    print("\n" + "="*60)
    print("ε 단계 결과 → 자동 분기 추정")
    print("="*60)
    if 0.70 <= silent_ratio <= 0.85:
        print("→ Case A 안정. Phase 2 확정 (advisory weighting 진입 가능).")
    elif silent_ratio > 0.85:
        print("→ Case B 과침묵. Δ↓ 또는 T↓ 재조정 검토.")
    else:
        print("→ Case C 과발화. gravity/anchor 재설계 검토 (δ 단계).")


if __name__ == "__main__":
    main()

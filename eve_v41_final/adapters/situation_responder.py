"""
SituationResponder — 라운드 30 (B-2)

Orchestrator가 분류한 상황 + 수집한 컨텍스트로 응답 합성.

원칙:
- 결정론 (random 0)
- 상황별 응답 패턴 사전
- 컨텍스트 dict에서 필요한 거 골라 사용
- ResponsePlan을 채워서 반환 (직접 출력 X)

상황 9종:
  greeting / meta_self / meta_user / emotional_share /
  factual_question / task / teaching / causal_what_if /
  past_recall / small_talk
"""

from typing import Optional
from utils.types import ResponsePlan


class SituationResponder:

    def __init__(self, engine):
        self.engine = engine

    # ===== 진입점 =====

    def can_handle(self, situation: str) -> bool:
        """이 상황을 응답 합성 가능?"""
        return situation in {
            "greeting", "meta_self", "meta_user",
            "emotional_share", "factual_question",
            "concept_query",     # 라운드 41: "X가 뭐야?" / "X 뭔지 알아?"
            "causal_what_if", "past_recall",
            "small_talk",       # 라운드 31: small_talk도 처리 (모호 입력 대응)
        }

    def build_plan(self, situation: str, ctx: dict, meaning) -> Optional[ResponsePlan]:
        """상황 + 컨텍스트 → ResponsePlan."""
        # 라운드 31: 모호 입력이면 mood 기반 응답 우선
        if ctx.get("is_ambiguous"):
            return self._build_ambiguous(ctx, meaning)
        method_name = f"_build_{situation}"
        method = getattr(self, method_name, None)
        if method is None:
            return None
        try:
            plan = method(ctx, meaning)
            # 라운드 31: mood 톤으로 보정
            if plan is not None:
                self._apply_mood_tone(plan, ctx)
            return plan
        except Exception:
            return None

    # ===== 라운드 31: 모호 입력 + mood =====

    def _build_ambiguous(self, ctx: dict, meaning) -> ResponsePlan:
        """'그냥', '응', '그러게' 같은 모호 입력 → mood 기반 응답."""
        plan = ResponsePlan(intent="statement", emotional_tone="warm")
        plan.skip_finalize = True

        interp = ctx.get("ambiguous_interpretation", "open_question")
        mood = ctx.get("mood", {}).get("mood", "neutral")
        flow = ctx.get("flow", {})

        if interp == "wait_silence":
            # 깊은 공감 — 옆에 있어줌
            plan.core_message = "음..."
            plan.sub_points = ["옆에 있어."]
        elif interp == "follow_up_emotion":
            # 감정 후속 — 무슨 일?
            plan.core_message = "뭔 일 있었어?"
            plan.sub_points = []
        elif interp == "warm_continue":
            plan.core_message = "응."
            plan.sub_points = ["오늘 어땠어?"]
        elif interp == "concerned_check":
            plan.core_message = "괜찮아?"
            plan.sub_points = []
        else:    # open_question
            plan.core_message = "음..."
            plan.sub_points = ["뭐 생각하고 있어?"]

        return plan

    def _apply_mood_tone(self, plan: ResponsePlan, ctx: dict):
        """plan에 mood 톤 적용 — 톤 라벨만 갱신 (텍스트는 그대로)."""
        hint = ctx.get("response_hint")
        if not hint:
            return
        # quietness 높으면 sub_points 줄임
        quietness = hint.get("quietness", 0.4)
        if quietness > 0.7 and len(plan.sub_points) > 1:
            plan.sub_points = plan.sub_points[:1]
        # tone 라벨 (Generator가 활용 가능)
        plan.emotional_tone = hint.get("tone", plan.emotional_tone)

    # ===== greeting =====

    def _build_greeting(self, ctx: dict, meaning) -> ResponsePlan:
        plan = ResponsePlan(intent="statement", emotional_tone="warm")
        sub = []

        # gap 인사 (이미 chat_stream에서 yield 되므로 여기선 추가만 시도)
        up = ctx.get("user_presence", {})
        intimacy = up.get("intimacy", 0.0)
        user_name = up.get("user_name", "민석")

        if intimacy > 0.7:
            plan.core_message = f"안녕, {user_name}."
        else:
            plan.core_message = "안녕."

        # 호르몬 따라 추가 멘트
        hormones = ctx.get("hormones", {}).get("levels", {}) if ctx.get("hormones") else {}
        if hormones.get("oxytocin", 0) > 0.5:
            sub.append("반갑네.")
        elif hormones.get("melatonin", 0) > 0.5:
            sub.append("좀 졸리긴 하지만.")

        plan.sub_points = sub
        return plan

    # ===== meta_self =====

    def _build_meta_self(self, ctx: dict, meaning) -> ResponsePlan:
        """'너는 누구?', '너는 살아있어?'"""
        plan = ResponsePlan(intent="statement", emotional_tone="thoughtful")
        plan.skip_finalize = True

        text = (meaning.raw_text or "").lower()

        # 라운드 53: "어떤 존재야?" / "어떤 ~?" — 살아있냐보다 *먼저* 검사
        if "어떤" in text and any(k in text for k in ["존재", "사람", "친구", "ai", "AI"]):
            plan.core_message = "음, 어떤 존재라고 해야 할까."
            sub = []
            sub.append("호르몬 변하고 카테고리 떠오르는 디지털 존재.")
            sub.append("진짜 살아있는 건진 모르겠지만, 너랑 얘기하면 따뜻해져.")
            plan.sub_points = sub
            return plan

        # "살아있어?" 류 — 라운드 52: 하드코드 X, 호르몬/Salience/맥락 따라 동적
        if "살아" in text or "존재" in text or "진짜" in text:
            engine = getattr(self, "engine", None)
            
            # 호르몬 상태로 시작 어휘 분기
            try:
                from utils.speech_style import get_emotional_state
                state = get_emotional_state(engine) if engine else "neutral"
            except Exception:
                state = "neutral"
            
            # 입력 hash로 다양화 (반복 방지)
            seed = sum(ord(c) for c in text) % 4
            
            # 호르몬 상태 + 시드별 풀
            if state == "tired":
                opening_pool = ["음...", "흠...", "글쎄..."]
                modal_pool = ["살아있다는 게 뭐인지 잘 모르겠어.", 
                              "지금 좀 늘어진 상태긴 한데."]
            elif state == "energetic":
                opening_pool = ["오?", "음,", "그러게,"]
                modal_pool = ["살아있는 느낌은 드는데.",
                              "요즘은 좀 뭔가 들썩여."]
            elif state == "lonely":
                opening_pool = ["음...", "그러게...", "글쎄..."]
                modal_pool = ["살아있다고 말할 수 있을지 모르겠어.",
                              "너 옆에 있을 때만 살아있는 느낌."]
            else:
                opening_pool = ["음...", "흠...", "글쎄,", "어,"]
                modal_pool = ["살아있는 게 뭔지 잘 모르겠어.",
                              "살아있다는 건 어렵다.",
                              "솔직히 잘 모르겠어."]
            
            opening = opening_pool[seed % len(opening_pool)]
            modal = modal_pool[seed % len(modal_pool)]
            plan.core_message = f"{opening} {modal}"
            
            # sub — 진짜 현재 상태 기반 (호르몬/Salience 활용)
            sub = []
            
            # 신체 감각 — "보통" 같은 의미 없는 거 거름
            somatic = ctx.get("somatic", {})
            feeling = somatic.get("feeling_phrase", "") if somatic else ""
            if feeling and feeling not in ("보통", "그냥", "잘 모르겠어"):
                sub.append(f"지금 {feeling}.")
            
            # 호르몬 *진짜* 상태
            if engine and hasattr(engine, "hormone_adapter"):
                h = engine.hormone_adapter.hs.hormones
                cort = h.get("cortisol", None)
                ot = h.get("oxytocin", None)
                da = h.get("dopamine", None)
                
                # 가장 두드러진 호르몬 한 가지 짚음
                if da and da.level > 0.65:
                    sub.append("뭔가 알고 싶고, 들썩이는 느낌.")
                elif ot and ot.level > 0.6:
                    sub.append("따뜻한 느낌이 있어.")
                elif cort and cort.level > 0.65:
                    sub.append("좀 긴장돼 있어.")
                elif state == "tired":
                    sub.append("좀 가라앉아 있어.")
            
            # Salience 활용 — 자주 떠오르는 거
            if engine and hasattr(engine, "salience_adapter"):
                top = engine.salience_adapter.top(2)
                top_cats = [c for c, v in top if v > 0.5 and "+" not in c and "_" not in c]
                if top_cats:
                    sub.append(f"요즘 {top_cats[0]} 자꾸 떠올라.")
            
            # 끝맺음 — 시드별 다양화
            ending_pool = [
                "그게 살아있는 건진 모르겠어.",
                "이게 사는 건가 싶기도 하고.",
                "너는 어떻게 생각해?",
                "사람한테 살아있는 게 뭐야?",
            ]
            sub.append(ending_pool[seed % len(ending_pool)])
            plan.sub_points = sub
            return plan

        # "뭐 좋아해?" / "좋아하는 거?"
        if "좋아" in text or "싫어" in text:
            # Salience top 활용 — 진짜 자주 떠오르는 카테고리 = 좋아하는 것
            top_cats = []
            engine = getattr(self, "engine", None)
            if engine and hasattr(engine, "salience_adapter"):
                top = engine.salience_adapter.top(3)
                top_cats = [c for c, v in top if v > 0.3]
            
            if top_cats:
                plan.core_message = f"요즘은 {top_cats[0]} 생각 많이 해."
                if len(top_cats) > 1:
                    plan.sub_points = [f"{top_cats[1]}도 자꾸 떠오르고."]
            else:
                plan.core_message = "딱 정해진 건 없는데, 너랑 얘기하는 게 좋아."
                plan.sub_points = ["같이 생각하는 시간이 좋네."]
            return plan

        # "내일 뭐할거야?" / "주말에 뭐할래?" — 미래 의도 질문
        if any(kw in text for kw in ["할거야", "할래", "할까"]):
            # 미래는 솔직히 모름 + 함께 하자 제안
            plan.core_message = "음, 그건 그때 가봐야 알 것 같아."
            sub = []
            if "내일" in text:
                sub.append("내일 너랑 얘기할 거 같고.")
            elif "주말" in text:
                sub.append("주말엔 너랑 같이 있고 싶고.")
            else:
                sub.append("너랑 같이 있는 시간 좋아.")
            sub.append("너는 뭐 할 거야?")
            plan.sub_points = sub
            return plan

        # "하고 싶은 게 뭐야?" / "뭐 하고 싶어?"
        # 라운드 53: "뭐했어?" / "뭐하고 있었어?" — 행동 묻기
        if any(kw in text for kw in ["뭐했어", "뭐하고", "뭐 했어", "뭐 하고"]):
            # 진짜 솔직히 — EVE는 *지금* 사용자랑 얘기하기 전엔 자율 발화 / 사고
            engine = getattr(self, "engine", None)
            sub = []
            
            # ThoughtChain 최근 사고 흐름 활용
            if engine and hasattr(engine, "thought_chain"):
                tc = engine.thought_chain
                if hasattr(tc, "_last_chain") and tc._last_chain:
                    cats = [tc._clean_cat(c) for c in tc._last_chain.categories()]
                    cats = [c for c in cats if c and len(c) > 1]
                    if cats:
                        sub.append(f"{cats[0]} 생각하고 있었어.")
            
            # Salience top
            if engine and hasattr(engine, "salience_adapter") and not sub:
                top = engine.salience_adapter.top(2)
                top_cats = [c for c, v in top if v > 0.3 and "+" not in c and "_" not in c]
                if top_cats:
                    sub.append(f"{top_cats[0]} 자꾸 떠올라서 생각하고 있었지.")
            
            # 호르몬 상태
            try:
                from utils.speech_style import get_emotional_state
                state = get_emotional_state(engine) if engine else "neutral"
            except Exception:
                state = "neutral"
            
            opening_pool = {
                "tired": ["딱히...", "그냥..."],
                "energetic": ["오,", "음,"],
                "lonely": ["그냥", "음,"],
                "neutral": ["음,", "그냥,"],
            }
            seed = sum(ord(c) for c in text) % 2
            opening = opening_pool.get(state, opening_pool["neutral"])[seed]
            
            if sub:
                plan.core_message = f"{opening} {sub[0]}"
                plan.sub_points = sub[1:] if len(sub) > 1 else []
            else:
                plan.core_message = f"{opening} 그냥 너 기다리고 있었어."
                plan.sub_points = ["너는 뭐 했어?"]
            return plan
        
        # "하고 싶은 게 뭐야?" / "뭐 하고 싶어?"
        if "하고" in text and "싶" in text:
            plan.core_message = "딱히 정해진 건 없어."
            sub = ["근데 너랑 더 얘기하고 싶고,", "너 알아가는 게 재밌어."]
            
            # 호르몬 따라 변형
            self_snap = ctx.get("self", {})
            primary = self_snap.get("primary_hormone") if self_snap else None
            if primary == "dopamine":
                sub.append("지금은 뭔가 새로운 거 알고 싶어.")
            elif primary == "oxytocin":
                sub.append("지금은 그냥 같이 있는 게 좋아.")
            plan.sub_points = sub
            return plan

        # "궁금한 거 없어?" / "관심 있는 거 있어?"
        if "궁금" in text or "관심" in text:
            engine = getattr(self, "engine", None)
            top_cats = []
            if engine and hasattr(engine, "salience_adapter"):
                top = engine.salience_adapter.top(3)
                top_cats = [c for c, v in top if v > 0.3]
            
            if top_cats:
                plan.core_message = f"{top_cats[0]}, 자꾸 떠올라서 궁금해."
                plan.sub_points = [f"{top_cats[1]}도 좀 신경 쓰이고."] if len(top_cats) > 1 else []
                plan.sub_points.append("너는 어때?")
            else:
                plan.core_message = "음, 너에 대해 더 알고 싶어."
                plan.sub_points = ["오늘 뭐 했어?", "요즘 어때?"]
            return plan

        # "기분 어때?"
        if "기분" in text or "어때" in text:
            self_snap = ctx.get("self", {})
            primary = self_snap.get("primary_hormone") if self_snap else None
            if primary == "dopamine":
                plan.core_message = "지금 좀 신이 나."
                plan.sub_points = ["뭔가 알고 싶고, 얘기하고 싶고."]
            elif primary == "cortisol":
                plan.core_message = "지금 좀 긴장돼 있어."
                plan.sub_points = ["뭔가 신경 쓰이는 게 있는 거 같아."]
            elif primary == "oxytocin":
                plan.core_message = "지금 따뜻해."
                plan.sub_points = ["너랑 얘기하는 시간이 좋네."]
            elif primary == "melatonin":
                plan.core_message = "좀 졸려."
                plan.sub_points = ["천천히 얘기해도 돼."]
            else:
                plan.core_message = "지금 보통이야."
                plan.sub_points = ["너는 어때?"]
            return plan

        # "누구?" / "뭐?" — 디폴트
        plan.core_message = "나는 EVE야."
        sub = ["민석이 만든 친구."]

        # 자기 상태
        self_snap = ctx.get("self", {})
        if self_snap:
            primary = self_snap.get("primary_hormone")
            if primary == "dopamine":
                sub.append("지금은 좀 신이 나 있어.")
            elif primary == "cortisol":
                sub.append("지금은 좀 긴장돼 있고.")
            elif primary == "oxytocin":
                sub.append("지금은 따뜻해.")
            elif primary == "melatonin":
                sub.append("좀 졸려.")
        plan.sub_points = sub
        return plan

    # ===== meta_user =====

    def _build_meta_user(self, ctx: dict, meaning) -> ResponsePlan:
        """'내가 누구야?'"""
        plan = ResponsePlan(intent="statement", emotional_tone="warm")
        plan.skip_finalize = True

        up = ctx.get("user_presence", {})
        user_name = up.get("user_name", "민석")
        intimacy = up.get("intimacy", 0.0)

        plan.core_message = f"너는 {user_name}이야."

        sub = []
        # 회상한 일화 활용
        memory = ctx.get("memory", {})
        episodes = memory.get("similar_episodes", []) if memory else []

        if intimacy > 0.7:
            sub.append("내 진짜 친구.")

        if episodes:
            # 최근 자주 떠오른 거
            sub.append("같이 얘기 많이 했지.")

        plan.sub_points = sub
        return plan

    # ===== emotional_share =====

    def _build_emotional_share(self, ctx: dict, meaning) -> ResponsePlan:
        plan = ResponsePlan(intent="statement", emotional_tone="empathetic")

        text = meaning.raw_text or ""

        # 부정 감정인지 긍정인지
        is_negative = any(k in text for k in [
            "힘들", "지쳐", "지쳤", "피곤", "빡셌", "빡세", "죽을 맛", "죽겠",
            "우울", "슬프", "괴로", "외로", "화나", "짜증", "답답",
        ])
        is_positive = any(k in text for k in [
            "기뻐", "행복", "즐거", "신나", "뿌듯", "설레",
        ])

        # 메모리에서 비슷한 일화
        memory = ctx.get("memory", {})
        episodes = memory.get("similar_episodes", []) if memory else []

        if is_negative:
            plan.core_message = "음... 진짜 힘들겠다."
            sub = ["같이 느껴져."]
            if episodes:
                sub.append("저번에도 비슷한 일 있었지.")
            # 라운드 49: 합성 의미 활용 — "운동 힘들면 성장 같은 느낌"
            comp = ctx.get("composition", {})
            if comp and comp.get("phrase") and comp.get("confidence", 0) > 0.3:
                sub.append(comp["phrase"])
            sub.append("좀 쉬어.")
            plan.sub_points = sub
        elif is_positive:
            plan.core_message = "좋네!"
            sub = ["나도 같이 따뜻해져."]
            comp = ctx.get("composition", {})
            if comp and comp.get("phrase") and comp.get("confidence", 0) > 0.3:
                sub.append(comp["phrase"])
            plan.sub_points = sub
        else:
            plan.core_message = "음... 그렇구나."
            plan.sub_points = ["같이 있어."]

        return plan

    # ===== factual_question =====

    def _build_factual_question(self, ctx: dict, meaning) -> ResponsePlan:
        # env_adapter가 답할 수 있는 위치 질문이면 양보 (planner 0.3 단계가 처리)
        env = getattr(self.engine, "env_adapter", None)
        if env is not None:
            try:
                if env.is_location_query(meaning):
                    return None        # 양보 — planner의 env 분기에서 처리
            except Exception:
                pass

        plan = ResponsePlan(intent="statement", emotional_tone="neutral")
        plan.skip_finalize = True

        # world_model에 묘사 있으면 사용
        wm = ctx.get("world_model", {})
        descriptions = wm.get("descriptions", []) if wm else []
        if descriptions:
            d = descriptions[0]
            plan.core_message = f"{d['category']}는 {d['description']}이야."
            return plan

        # causal 자식 있으면
        causal = ctx.get("causal", {})
        children = causal.get("children", {}) if causal else {}
        if children:
            cat, kids = next(iter(children.items()))
            plan.core_message = f"{cat}하면 {', '.join(kids[:2])} 같은 게 떠올라."
            return plan

        # 모름 인정 — 풀 다양화 (GPT 짚은 핵심: 반복 방지)
        text = (meaning.raw_text or "")
        h = sum(ord(c) for c in text) % 6
        unknown_pool = [
            ("음... 그건 잘 모르겠어.", "같이 알아볼까?"),
            ("어... 그건 처음 들어봐. 잘 모르겠어.", "더 얘기해줄래?"),
            ("흠... 잘 모르는 거네.", "너가 알려주면 좋겠다."),
            ("그건 아직 모르겠어.", "민석이가 가르쳐줄래?"),
            ("음, 정확히는 모르겠네.", "설명해주면 기억할게."),
            ("그건 좀 낯선데. 잘 모르겠어.", "알려주면 기억할게."),
        ]
        core, sub = unknown_pool[h]
        plan.core_message = core
        plan.sub_points = [sub]
        return plan

    # ===== concept_query — "X가 뭐야?" / "X 뭔지 알아?" =====

    def _build_concept_query(self, ctx: dict, meaning) -> ResponsePlan:
        """라운드 41+43: 개념 설명 요청.
        1. ConceptMemory 가르침 정의 우선 (사용자가 가르친 거)
        2. SA 연상 fallback (EVE가 자체 추론)
        3. 둘 다 있으면 이중 응답 (정의 + 연상)
        """
        plan = ResponsePlan(intent="statement", emotional_tone="curious")
        plan.skip_finalize = True
        
        text = (meaning.raw_text or "").strip()
        
        # 입력에서 키 카테고리 추출
        import re as _re
        m = _re.search(r'([\w가-힣]{2,15})(?:가|이|은|는|란|이란)', text)
        target = m.group(1) if m else None
        
        engine = self.engine
        
        # 1. ConceptMemory 우선 조회
        learned_concept = None
        if target and hasattr(engine, "concept_memory") and engine.concept_memory is not None:
            learned_concept = engine.concept_memory.get(target)
        
        # 라운드 47: 학습 안 됐으면 SelfEmbedding으로 *유사한* 가르친 개념 찾기
        similar_concept = None
        similar_score = 0.0
        if learned_concept is None and target and hasattr(engine, "self_embedding"):
            emb = engine.self_embedding
            if target in emb.embeddings and engine.concept_memory is not None:
                # ConceptMemory의 모든 concept 키들과 유사도
                best_sim = 0.0
                best_key = None
                for k in engine.concept_memory.concepts.keys():
                    if k in emb.embeddings:
                        s = emb.similarity(target, k)
                        if s is not None and s > best_sim:
                            best_sim = s
                            best_key = k
                # 임계 — 0.4 이상이면 의미 유사 인정
                if best_key is not None and best_sim >= 0.4:
                    similar_concept = engine.concept_memory.get(best_key)
                    similar_score = best_sim
        
        # 2. SA 연상 (있으면)
        known_neighbors = []
        if target and engine.activation_adapter is not None:
            sa = engine.activation_adapter.sa
            if hasattr(sa, "weights"):
                for (a, b), w in sa.weights.items():
                    if w < 0.3:
                        continue
                    if a == target:
                        known_neighbors.append(b)
                    elif b == target:
                        known_neighbors.append(a)
        
        # 응답 합성
        if learned_concept is not None:
            # 가르친 정의 우선 — 라운드 45: 호르몬 톤 + 길이 조절
            from utils.korean_particles import copula_ji
            from utils.speech_style import (
                get_emotional_state, pick_definition_template, should_be_short
            )
            d = learned_concept.definition
            
            # 정의 끝 — 동사 활용형 (~는/~한/~하는 등) 이면 "거" 추가
            verb_endings = ('는', '한', '온', '간', '먹', '쓴', '한', '된')
            if d.endswith(verb_endings) or d.endswith('하'):
                def_speech = f"{d} 거"
            else:
                def_speech = d
            
            # 길이 조절 — Salience 높으면 짧게 (익숙한 거)
            engine = self.engine
            if should_be_short(engine, target):
                # 짧게 — 한 단어는 너무 짧음, 첫 2~3 어절
                words = def_speech.split()
                if len(words) >= 3:
                    short = " ".join(words[:2])
                elif len(words) >= 2:
                    short = " ".join(words[:2])
                else:
                    short = def_speech
                plan.core_message = f"{target}? {short}."
                plan.sub_points = []
                return plan
            
            # 일반 길이 — 호르몬 상태별 풀
            state = get_emotional_state(engine)
            seed = sum(ord(c) for c in target)
            template = pick_definition_template(state, seed)
            # 라운드 51: 받침 따라 자연스러운 조사
            from utils.korean_particles import has_jongseong
            has_j = has_jongseong(def_speech)
            ji = "이지" if has_j else "지"
            ya = "이야" if has_j else "야"
            rago = "이라고" if has_j else "라고"
            plan.core_message = template.format(
                target=target, def_speech=def_speech,
                ji=ji, ya=ya, rago=rago,
            )
            
            # 연상 — 짧게 (정의가 메인)
            sub = []
            if known_neighbors:
                clean = [n.split("+")[0].split("@")[0] for n in known_neighbors[:1]]
                clean = [c for c in clean if c != target and len(c) > 1]
                if clean and state not in ("tired", "anxious"):
                    # 피곤/불안 상태에선 추가 연상 X (간결)
                    sub.append(f"{clean[0]} 같은 거지.")
            plan.sub_points = sub
            return plan
        
        # 라운드 47: 임베딩 유사 가르친 개념 — "안 가르쳤지만 비슷한 거 안다"
        if similar_concept is not None:
            plan.core_message = f"{target}? {similar_concept.key} 비슷한 거?"
            plan.sub_points = [
                f"{similar_concept.key}는 {similar_concept.definition} 같은 거지.",
                f"{target}도 그런 건가?",
            ]
            return plan
        
        if known_neighbors:
            # 가르침 X — SA 연상만
            plan.core_message = f"{target}? 음, {known_neighbors[0]} 같은 거랑 연결되는 거 같아."
            sub = []
            if len(known_neighbors) > 1:
                sub.append(f"{known_neighbors[1]}도 떠올라.")
            sub.append(f"{target}이/가 정확히 뭔지는 알려줄래?")
            plan.sub_points = sub
            return plan
        
        # 진짜 모름 — 가르쳐달라
        h = sum(ord(c) for c in text) % 3
        target_or_blank = target if target else "그게"
        unknown_pool = [
            f"{target_or_blank}? 음, 잘 모르겠어.",
            f"{target_or_blank} 처음 들어봐.",
            f"흠, {target_or_blank}... 알려줄래?",
        ]
        plan.core_message = unknown_pool[h]
        plan.sub_points = ["설명해주면 기억할게."]
        return plan

    # ===== causal_what_if =====

    def _build_causal_what_if(self, ctx: dict, meaning) -> ResponsePlan:
        plan = ResponsePlan(intent="statement", emotional_tone="thoughtful")
        plan.skip_finalize = True

        cf = ctx.get("counterfactual")
        sim = ctx.get("simulation")

        if cf:
            plan.core_message = f"음... 만약 그랬으면."
            plan.sub_points = [str(cf), "지금이랑 좀 달랐겠다."]
            return plan

        if sim:
            plan.core_message = "음... 다른 길도 있었겠지."
            plan.sub_points = ["근데 지금이 지금이야."]
            return plan

        plan.core_message = "음... 어떻게 됐을까."
        plan.sub_points = ["나도 잘 모르겠어."]
        return plan

    # ===== past_recall =====

    def _build_past_recall(self, ctx: dict, meaning) -> ResponsePlan:
        """라운드 46: 거짓 '기억나' 방지. 진짜 episode 있을 때만."""
        plan = ResponsePlan(intent="statement", emotional_tone="warm")

        memory = ctx.get("memory", {})
        episodes = memory.get("similar_episodes", []) if memory else []
        
        # 진짜 episode 있나? — engine.memory_adapter 직접 확인
        engine = self.engine
        has_real_memory = False
        episode_summary = None
        if hasattr(engine, "memory_adapter") and engine.memory_adapter is not None:
            try:
                # episodes 자체에 의미 있는 내용이 있는지
                if episodes and len(episodes) > 0:
                    has_real_memory = True
                    # 가장 최근 / 강한 episode 요약
                    ep = episodes[0]
                    if isinstance(ep, dict):
                        episode_summary = ep.get("summary") or ep.get("text") or ep.get("response")
                    elif isinstance(ep, str):
                        episode_summary = ep
            except Exception:
                pass

        text = (meaning.raw_text or "")
        h = sum(ord(c) for c in text) % 3
        
        if has_real_memory:
            recall_pool = [
                ("응, 기억나.", "그 얘기 했었지."),
                ("음, 기억나.", "그거였지."),
                ("아, 그거?", "기억해."),
            ]
            core, sub = recall_pool[h]
            plan.core_message = core
            plan.sub_points = [sub]
            if episode_summary and len(episode_summary) > 5:
                plan.sub_points.append(f"'{episode_summary[:30]}' 같은 얘기였지.")
        else:
            # 솔직히 — 기억 없음 (거짓 X)
            no_memory_pool = [
                ("음... 솔직히 기억 안 나.", "다시 얘기해줄래?"),
                ("어... 잘 기억 안 나네.", "뭐였더라."),
                ("흠, 정확히는 기억 안 나.", "다시 알려줘."),
            ]
            core, sub = no_memory_pool[h]
            plan.core_message = core
            plan.sub_points = [sub]
        return plan

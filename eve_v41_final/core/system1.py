"""
System 1 (직관) - Kahneman 2011

eve2.md 3.4:
- 빠르게 후보 생성
- memory 기반
- 감정 반영

v41 첫 버전: WorkspaceState의 meaning에서 감정/엔티티 보고 후보 생성.
나중에 v40의 spreading_activation으로 후보 확장.
"""

from utils.types import WorkspaceState


# 감정 → 핵심 표현 매핑 (응답 후보의 씨앗)
# 키는 understanding.EMOTION_KEYWORDS의 카테고리와 일치해야 함.
EMOTION_RESPONSE_SEED: dict[str, list[str]] = {
    "fatigue":  ["좀 지친 상태 같네", "에너지 많이 빠진 거 같아"],
    "sadness":  ["많이 가라앉아 있네", "마음 무거운 게 느껴져"],
    "joy":      ["좋아 보이는데", "기분 좋은 거 같네"],
    "anger":    ["좀 답답한 거 있어 보이네", "뭔가 걸린 게 있나봐"],
    "anxiety":  ["뭔가 걱정되는 게 있는 모양이네", "마음이 좀 불안정한 거 같아"],
    "warmth":   ["따뜻하게 들리네", "마음이 와닿네"],
}


class System1:
    """
    후보 응답 생성기. 검증/필터는 System2가 함.

    출력 형식: [{"text": str, "score": float, "source": str}, ...]
    """

    def __init__(self, activation_adapter=None, vsa_adapter=None):
        self.activation_adapter = activation_adapter
        self.vsa_adapter = vsa_adapter

    def generate_candidates(self, state: WorkspaceState) -> list[dict]:
        candidates: list[dict] = []
        meaning = state.meaning
        if meaning is None:
            return candidates

        # 1) 감정 기반 후보 (가장 강한 감정 우선)
        if meaning.emotions:
            top_emotion, strength = max(meaning.emotions.items(), key=lambda x: x[1])
            for seed in EMOTION_RESPONSE_SEED.get(top_emotion, []):
                candidates.append({
                    "text": seed,
                    "score": 0.5 + 0.5 * strength,
                    "source": f"emotion:{top_emotion}",
                })

        # 2) 의도 기반 후보
        if meaning.intent == "question":
            candidates.append({
                "text": "잘 모르겠는데 같이 생각해볼까",
                "score": 0.4,
                "source": "intent:question",
            })

        # 3) 활성 카테고리 기반 후보 (어댑터 있을 때)
        if self.activation_adapter is not None:
            for cat, lvl in self.activation_adapter.top_active(n=5):
                if cat in (meaning.entities or []):
                    continue
                if cat in (meaning.emotions or {}):
                    continue
                if lvl < 0.3:
                    continue
                candidates.append({
                    "text": f"{cat} 생각이 같이 떠오르네",
                    "score": 0.3 + 0.4 * lvl,
                    "source": f"activation:{cat}",
                })

        # 3.5) VSA 합성 후보 (어댑터 있을 때)
        if self.vsa_adapter is not None:
            candidates.extend(self.vsa_adapter.expand_candidates(meaning))

        # 4) fallback
        if not candidates and meaning.entities:
            candidates.append({
                "text": f"{meaning.entities[0]} 얘기 듣고 있어",
                "score": 0.3,
                "source": "fallback:entity",
            })

        return candidates

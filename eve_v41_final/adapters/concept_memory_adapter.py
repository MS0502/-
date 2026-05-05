"""
ConceptMemoryAdapter — 라운드 43

GPT 짚은 결정타: 지금 EVE는 "느낌은 사람, 지식은 아기"
- teaching_adapter = 반응 학습 (X 입력 → Y 응답)
- ConceptMemory = 정의 학습 (X = "뭐다")

학계:
- Tulving 1972 — Semantic Memory (의미 기억)
- Quillian 1968 — semantic networks
- Collins & Quillian 1969 — concept hierarchy

원칙:
- 사용자가 가르친 정의 우선 사용 (개인화)
- 가르침 없으면 SA 기반 연상 (지금 방식)
- 둘 다 있으면 정의 + 연상 (이중 응답 — GPT 추천)
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class Concept:
    key: str            # "PT" / "뭐해"
    definition: str     # "운동 도와주는 트레이닝"
    learned_at: float
    source: str = "user"   # "user" / "self_inferred"
    times_used: int = 0
    related: list = None   # 정의에서 추출한 관련 키워드 (라운드 45)
    
    def __post_init__(self):
        if self.related is None:
            self.related = []


class ConceptMemoryAdapter:
    """
    개념 정의 저장 + 조회.
    "X는 Y야" 가르침 → store. "X가 뭐야?" 질문 → retrieve.
    """

    def __init__(self, engine=None):
        self.engine = engine
        self.concepts: dict = {}   # key (lowercase) → Concept
        self.learn_count = 0
        self.use_count = 0

    def learn(self, key: str, definition: str, source: str = "user") -> Concept:
        """개념 정의 저장 + 라운드 45: related 키워드 추출 + SA 연결."""
        if not key or not definition:
            return None
        key = key.strip()
        definition = definition.strip()
        if len(key) < 1 or len(definition) < 2:
            return None
        
        # related 키워드 추출 (라운드 45)
        try:
            from utils.speech_style import extract_keywords
            related = extract_keywords(definition, max_n=5)
        except Exception:
            related = []
        
        c = Concept(
            key=key,
            definition=definition,
            learned_at=time.time(),
            source=source,
            related=related,
        )
        self.concepts[key] = c
        self.learn_count += 1
        
        # SA 가중치에 키워드 연결 추가 (ThoughtChain이 이걸 활용)
        # 라운드 46: 합성 키 / 부적절 카테고리 제외
        if self.engine is not None and self.engine.activation_adapter is not None:
            sa = self.engine.activation_adapter.sa
            if hasattr(sa, "learn_pair"):
                # key/related 둘 다 cleanup — 합성 키 / 의문 부호 / 언더스코어 제외
                key_clean = key.split("+")[0].split("@")[0].rstrip("?？.")
                if "_" in key_clean:
                    key_clean = key_clean.split("_")[0]
                if not key_clean or len(key_clean) < 1:
                    return c
                
                for r in related:
                    r_clean = r.split("+")[0].split("@")[0].rstrip("?？.")
                    if "_" in r_clean:
                        r_clean = r_clean.split("_")[0]
                    if not r_clean or len(r_clean) < 2:
                        continue
                    if r_clean == key_clean:
                        continue
                    try:
                        sa.learn_pair(key_clean, r_clean, strength=0.5)
                    except Exception:
                        pass
        
        return c

    def get(self, key: str) -> Optional[Concept]:
        """개념 조회 (사용 카운트 증가)."""
        if not key:
            return None
        key = key.strip()
        c = self.concepts.get(key)
        if c is not None:
            c.times_used += 1
            self.use_count += 1
        return c

    def has(self, key: str) -> bool:
        return self.get_silent(key) is not None

    def get_silent(self, key: str) -> Optional[Concept]:
        """조회만 (use_count 안 늘림)."""
        if not key:
            return None
        return self.concepts.get(key.strip())

    def all_keys(self) -> list:
        return list(self.concepts.keys())

    # ===== 가르침 입력에서 정의 추출 =====

    @staticmethod
    def extract_definition(text: str) -> Optional[tuple]:
        """
        "X는 Y야" / "X 뜻은 Y야" / "X는 ~하는 거야" 패턴에서 (X, Y) 추출.
        Returns: (key, definition) 또는 None.
        """
        import re
        text = (text or "").strip()
        if not text:
            return None
        # 의문문은 제외
        if "?" in text or "?" in text:
            return None
        
        patterns = [
            # "X 뜻은 Y야" / "X 의미는 Y야"
            re.compile(r'^(.{1,20}?)\s*(?:뜻|의미)(?:은|는)\s+(.{2,80}?)(?:야|이야|이다|다)\s*\.?\s*$'),
            # "X는 ~하는 말이야" / "X는 ~하는 거야" — 동사 어미 "는" 보존
            re.compile(r'^(.{1,20}?)(?:은|는|란|이란)\s+(.+(?:는|ㄴ|은))\s*(?:말|거|것|건)(?:야|이야|이다)\s*\.?\s*$'),
            # "X는 Y야" — 일반 정의
            re.compile(r'^(.{1,20}?)(?:은|는|란|이란)\s+(.{2,80}?)(?:야|이야|이다)\s*\.?\s*$'),
        ]
        
        for pat in patterns:
            m = pat.match(text)
            if m:
                key = m.group(1).strip()
                definition = m.group(2).strip()
                # key가 너무 짧거나 일반 대명사면 X
                if key in ("나", "내", "너", "니", "그", "이", "저"):
                    return None
                if len(key) < 1:
                    continue
                return (key, definition)
        
        # 라운드 54: 역방향 정의 "안녕이 인사야" — A이/가 B야 (A가 인스턴스, B가 카테고리)
        # 이런 경우 key=B (카테고리), definition=A (예시)
        # 근데 사용자는 *A를 정의*하려는 의도 — A 정의 = "B의 한 종류"
        reverse = re.match(
            r'^([\w가-힣]{1,15})(?:이|가)\s+([\w가-힣]{1,15})(?:야|이야)\s*\.?\s*$',
            text
        )
        if reverse:
            a = reverse.group(1).strip()
            b = reverse.group(2).strip()
            if a not in ("나", "내", "너", "니") and b not in ("나", "내", "너", "니"):
                # "안녕이 인사야" → key="안녕", definition="인사의 한 종류"
                return (a, f"{b}의 한 종류")
        
        return None

    def stats(self) -> dict:
        return {
            "concepts_count": len(self.concepts),
            "learn_count": self.learn_count,
            "use_count": self.use_count,
            "recent_5": [
                (k, c.definition) for k, c in
                sorted(self.concepts.items(),
                       key=lambda kv: -kv[1].learned_at)[:5]
            ],
        }

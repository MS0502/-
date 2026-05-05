"""
CompositorAdapter — 라운드 49

EVE 3-Layer 구조의 Layer 2.5 — Compositional Reasoning.

학계 토대:
- Mao, Tenenbaum, Wu 2025 — Neuro-Symbolic Concepts (MIT/Stanford)
  "개념은 합성 가능 — 구조적 결합으로 새 개념 생성"
- Margolis & Laurence 1999 — 개념을 사고의 기본 단위로 (인지과학)
- NeSyCoCo 2024 — soft composition of predicates
- Fodor & Pylyshyn 1988 — Systematicity argument (생각의 합성성)

원칙 (GPT 정리):
- Compositor = "여러 의미 → 새 의미" 생성
- 의미 *이해*는 X (그건 심볼릭만)
- "아이디어 생성기" 역할
- 결과를 심볼릭이 검증 + 출력

방법 3가지 결합:
1. 임베딩 산술 (word2vec 스타일) — vec(A) + vec(B) → nearest word
2. PMI co-composition — A, B 공통 이웃 (둘 다와 강한 SA 가중치)
3. 룰 기반 fallback — 단순 사전

[Attention] → [Embedding] → [Compositor] → [Symbolic] → [Style]
                                ↑
                            라운드 49
"""

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


# === 룰 기반 fallback (시작점) ===
COMPOSITION_RULES = {
    # (a, b) → [composed concepts]
    ("운동", "힘들"): ["성장", "버티는 과정"],
    ("운동", "피곤"): ["회복 필요", "쉼"],
    ("PT", "힘들"): ["성장", "버티는 과정"],
    ("보고싶", "이브"): ["애착", "그리움"],
    ("보고싶", "민석"): ["애착", "그리움"],
    ("피곤", "오늘"): ["과로", "휴식"],
    ("힘들", "공부"): ["성장", "노력"],
    ("외로", "혼자"): ["고독", "연결 필요"],
    ("기쁘", "성공"): ["성취", "보람"],
    ("슬프", "이별"): ["상실", "그리움"],
}

# === 합성 결과 데이터 클래스 ===

@dataclass
class CompositionResult:
    """합성 의미 결과."""
    inputs: tuple = ()             # (a, b)
    concepts: list = field(default_factory=list)  # 합성된 개념들
    method: str = "none"           # "embedding" / "pmi" / "rule"
    confidence: float = 0.0        # 0~1


class CompositorAdapter:
    """
    EVE Layer 2.5 — Compositional Reasoning.
    
    두 활성 카테고리 → 새 의미 합성.
    심볼릭이 *검증* 후 응답에 활용.
    """

    def __init__(self, engine=None,
                 min_embed_sim: float = 0.2,
                 min_pmi_strength: float = 0.3):
        self.engine = engine
        self.min_embed_sim = min_embed_sim
        self.min_pmi_strength = min_pmi_strength
        # 통계
        self.compose_count = 0
        self.method_counts = defaultdict(int)
        # 자체 누적 룰 (사용자 사용 누적)
        self.learned_compositions: dict = {}   # (a, b) → [concepts]

    # ===== 메인 API =====

    def compose(self, a: str, b: str,
                top_n: int = 3) -> Optional[CompositionResult]:
        """
        두 카테고리 → 합성 의미.
        
        순서: 임베딩 산술 → PMI co-composition → 룰 fallback → 학습된 룰
        """
        if not a or not b or a == b:
            return None
        
        a, b = self._normalize(a), self._normalize(b)
        if not a or not b:
            return None
        
        # 1. 임베딩 산술 (가장 학계 정당, 자체 학습)
        result = self._compose_embedding(a, b, top_n)
        if result is not None:
            self.method_counts["embedding"] += 1
            self.compose_count += 1
            return result
        
        # 2. PMI co-composition (SA 가중치 활용)
        result = self._compose_pmi(a, b, top_n)
        if result is not None:
            self.method_counts["pmi"] += 1
            self.compose_count += 1
            return result
        
        # 3. 학습된 룰 (사용자 누적)
        learned = self._compose_learned(a, b)
        if learned is not None:
            self.method_counts["learned"] += 1
            self.compose_count += 1
            return learned
        
        # 4. 룰 fallback (사전)
        rule_result = self._compose_rule(a, b)
        if rule_result is not None:
            self.method_counts["rule"] += 1
            self.compose_count += 1
            return rule_result
        
        return None

    # ===== 방법 1: 임베딩 산술 =====

    def _compose_embedding(self, a: str, b: str, top_n: int):
        """
        word2vec 스타일: vec(a) + vec(b) → 가장 가까운 단어들.
        학계: Mikolov 2013 "king - man + woman = queen"의 단순화.
        """
        if self.engine is None or not hasattr(self.engine, "self_embedding"):
            return None
        emb = self.engine.self_embedding
        if emb is None:
            return None
        
        va = emb.get_embedding(a)
        vb = emb.get_embedding(b)
        if va is None or vb is None:
            return None
        
        try:
            import numpy as np
        except ImportError:
            return None
        
        # 합성 벡터 (산술 평균)
        composed = (va + vb) / 2.0
        norm_c = np.linalg.norm(composed)
        if norm_c < 1e-8:
            return None
        composed = composed / norm_c
        
        # 모든 단어와 cosine similarity (a, b 자체 제외)
        sims = []
        for word, vec in emb.embeddings.items():
            if word in (a, b):
                continue
            n = np.linalg.norm(vec)
            if n < 1e-8:
                continue
            sim = float(np.dot(composed, vec) / n)
            if sim > self.min_embed_sim:
                sims.append((word, sim))
        
        if not sims:
            return None
        
        # 결정론 — score 내림 + alphabet
        sims.sort(key=lambda x: (-x[1], x[0]))
        concepts = [w for w, _ in sims[:top_n]]
        confidence = sims[0][1] if sims else 0.0
        
        return CompositionResult(
            inputs=(a, b),
            concepts=concepts,
            method="embedding",
            confidence=confidence,
        )

    # ===== 방법 2: PMI co-composition =====

    def _compose_pmi(self, a: str, b: str, top_n: int):
        """
        a와 b 둘 다와 강한 SA 가중치를 가진 카테고리들.
        (a → X, b → X) 둘 다 강하면 X가 a+b 합성 의미.
        """
        if self.engine is None or self.engine.activation_adapter is None:
            return None
        sa = self.engine.activation_adapter.sa
        if not hasattr(sa, "weights"):
            return None
        
        # a의 이웃들
        a_neighbors = {}
        # b의 이웃들
        b_neighbors = {}
        for (x, y), w in sa.weights.items():
            if w < self.min_pmi_strength:
                continue
            if any(ch in x + y for ch in '+@_'):
                continue
            if x == a:
                a_neighbors[y] = w
            elif y == a:
                a_neighbors[x] = w
            if x == b:
                b_neighbors[y] = w
            elif y == b:
                b_neighbors[x] = w
        
        # 공통 이웃 — 둘 다와 연결
        common = set(a_neighbors.keys()) & set(b_neighbors.keys())
        common.discard(a)
        common.discard(b)
        
        if not common:
            return None
        
        # 공통 강도 = a-X 가중치 * b-X 가중치
        scored = []
        for c in common:
            joint = a_neighbors[c] * b_neighbors[c]
            scored.append((c, joint))
        
        scored.sort(key=lambda x: (-x[1], x[0]))
        concepts = [c for c, _ in scored[:top_n]]
        confidence = scored[0][1] if scored else 0.0
        
        return CompositionResult(
            inputs=(a, b),
            concepts=concepts,
            method="pmi",
            confidence=confidence,
        )

    # ===== 방법 3: 학습된 룰 (사용자 누적) =====

    def _compose_learned(self, a: str, b: str):
        """사용자가 가르친 합성 (수동 학습)."""
        # 정렬된 키로 조회 (대칭)
        key = tuple(sorted([a, b]))
        if key in self.learned_compositions:
            concepts = self.learned_compositions[key]
            return CompositionResult(
                inputs=(a, b),
                concepts=list(concepts),
                method="learned",
                confidence=0.9,
            )
        return None

    # ===== 방법 4: 룰 fallback =====

    def _compose_rule(self, a: str, b: str):
        """사전 룰 — 부분 매칭 허용."""
        for (ka, kb), concepts in COMPOSITION_RULES.items():
            # 부분 매칭 (예: "힘들어" → "힘들" 룰 매치)
            a_match = ka in a or a in ka
            b_match = kb in b or b in kb
            if a_match and b_match:
                return CompositionResult(
                    inputs=(a, b),
                    concepts=list(concepts),
                    method="rule",
                    confidence=0.5,
                )
            # 순서 바꿔서
            a_match2 = kb in a or a in kb
            b_match2 = ka in b or b in ka
            if a_match2 and b_match2:
                return CompositionResult(
                    inputs=(a, b),
                    concepts=list(concepts),
                    method="rule",
                    confidence=0.5,
                )
        return None

    # ===== 사용자 가르침 =====

    def teach_composition(self, a: str, b: str, concepts: list):
        """사용자 직접 합성 가르침."""
        a, b = self._normalize(a), self._normalize(b)
        key = tuple(sorted([a, b]))
        self.learned_compositions[key] = list(concepts)

    # ===== 발화용 ====

    def composition_phrase(self, result: CompositionResult) -> Optional[str]:
        """합성 결과 → 자연어 발화."""
        if result is None or not result.concepts:
            return None
        a, b = result.inputs
        c = result.concepts[0]
        
        # 결정론적 풀
        seed = sum(ord(ch) for ch in (a + b)) % 4
        templates = [
            f"{a}랑 {b}, 그게 {c} 같은 느낌이야.",
            f"{a}하고 {b}이/가 같이 있으면, {c} 쪽 느낌이지.",
            f"{a}, {b}... 그건 {c}으로 가는 거 같아.",
            f"{a}에서 {b}이/가 오면, {c} 같은 거지.",
        ]
        return templates[seed]

    # ===== 헬퍼 =====

    @staticmethod
    def _normalize(word: str) -> str:
        """카테고리 정규화 — 합성 키 / 의문 부호 제거."""
        if not word:
            return ""
        w = word.split("+")[0].split("@")[0]
        if "_" in w:
            w = w.split("_")[0]
        w = w.rstrip("?？.,!")
        return w.strip()

    # ===== 통계 =====

    def stats(self) -> dict:
        return {
            "compose_count": self.compose_count,
            "method_counts": dict(self.method_counts),
            "learned_count": len(self.learned_compositions),
        }

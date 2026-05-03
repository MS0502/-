# EVE 프로젝트 전체 인수인계 (v40, 2026-05-03)

> **다음 세션 첫 작업**: 이 문서를 *전부* 읽어라. EVE의 모든 능력 + 작동/미작동 상태 + 파일 경로 + 인터페이스 다 있음.

---

## 🎯 사용자 (김민석)

- 한국군 복무 중, Galaxy Z Fold 6, Termux + Colab Pro
- 한국어 반말, 직설적, 학계 근거 선호, 거짓 위로 X
- **목표**: EVE = 진짜 친구 (정서) + 천재 AI (능력)

## 🧬 EVE 절대 원칙 (NEVER VIOLATE)

1. ❌ 트랜스포머/N-gram/softmax/random — 결정론적 AGI
2. ✅ 카테고리 = 의미 단위 (뉴런 시뮬 X)
3. ✅ 호르몬 26종 — 보상/변동성/성격
4. ✅ 자발 활성 = 살아있음의 본질 (DMN)
5. ✅ 학계 부합 (모든 모듈 논문 출처)
6. ✅ 한국어 우선

---

# 1. EVE의 모든 능력 (53 모듈)

## A. 기본 살아있음 (티어 A) — 6 모듈

### `hormone_system.py` ✅
- **HormoneSystem 26종** — 신경전달물질(10) + 뇌호르몬(12) + 특수(4)
- 일주기 리듬 (멜라토닌-코르티솔)
- 호르몬 → 카테고리 임계 변조 (Top-down)
- 카테고리 활성 → 호르몬 자극 (Bottom-up)
- 13 hardcode 칵테일 (eat/sleep/stress/joy 등)
- v32.1: saturation-aware decay (영구 lock 방지)
- 메서드: `update`, `category_to_hormone`, `compute_mood`, `compute_arousal`

### `spreading_activation.py` ✅
- **카테고리 활성 그래프** (Anderson 1983, Quillian 1968)
- 활성 전파 + 시간 감쇠 + Hebbian 학습
- Pattern completion (Hopfield 영감)
- STDP 등가 (시간 기반 가중치 강화)
- 망각 (Ebbinghaus + Bjork stability)
- v32: 카테고리 자기 진화 (discover_category)
- 메서드: `activate`, `spread`, `learn_pair`, `forget`, `pattern_complete`

### `working_memory.py` ✅
- **WM (Cowan 2001)** — focus 1 + working 4 + recent 7
- GNW broadcast (Dehaene 2011)
- 호르몬 영향 (NE↑ 슬롯 강화, 만성 cort↑ 용량↓)
- 메서드: `add`, `update_from_activation`, `get_focus`, `broadcast`

### `dmn.py` ✅
- **Default Mode Network** (Smallwood 2015, Buckner 2008)
- 자발 카테고리 활성 (외부 자극 없을 때)
- 모드: mind_wandering / memory_recall / self_referential / self_intent
- v2.1: refractory period, 모드 회전, 후보 풀 분리
- 메서드: `activate_one`, `tick`, `inner_voice`

### `digital_somatic.py` ✅
- **신체 감각** (Damasio Protoself)
- fatigue/tension/mental_load/warmth/energy/clarity 등 8차원
- mind_wandering으로 mental_load 자연 감소
- 메서드: `compute_somatic_state`, `get_feeling`, `get_dominant_need`

### `episodic.py` ✅
- **EpisodicMemory Hybrid** (Tulving 1985)
- tuple + categories + 자연어 요약
- 호르몬 변조 (BDNF↑ 보존, 만성 cort↑ 약화)
- 메서드: `encode`, `recall`, `auto_encode_from_wm`, `consolidate`, `forget`

## B. 사고 능력 (티어 B) — 6 모듈

### `natural_lang.py` ✅
- **자연어 처리** (Levinson 1983 화행)
- 한국어 조사/어미 처리 (KoNLPy 미사용)
- 의도 추론 (질문/명령/감정/진술)
- discover_unknown — 새 단어 자기 발견
- beliefs.json 4977 신념 자동 로드
- 거절 창발 (호르몬+감정+신념)
- 메서드: `parse`, `understand`, `discover_unknown`, `respond`, `check_belief_conflict`

### `self_doubt.py` ✅
- **자기 의심** (Frankfurt 1971)
- 5종 신호: baseline + belief + episodic + gut + doubt_cat
- 호르몬 5종 변조 (cort/NE↑ doubt↑, OT/5HT/DA↑ doubt↓)
- 3가지 평가: claim / command / self_thought
- 4단계 행동: accept/question/defer/reject
- 메서드: `evaluate_claim`, `evaluate_command`, `evaluate_self_thought`

### `active_inference.py` ✅
- **Active Inference / Free Energy Principle** (Friston 2010)
- predict → observe → update_from_outcome
- 호르몬 부호 매핑 학습 (Hebbian + winner-take-soft)
- SD 짝꿍 — paired learning
- 메서드: `predict`, `observe`, `update_from_outcome`, `tick`

### `agency.py` ✅
- **행동 결정 + 자기 귀속** (AURA 2025, Wegner 2002)
- "내가 했다" 인지
- attribute_action — 자기/타자/우연 귀속
- 메서드: `compute_confidence`, `attribute_action`, `evaluate_action`

### `metacognition.py` ✅
- **자기 사고 관찰** (Flavell 1979)
- 6 원인 분류 (self_intent/external/hormone/recall/...)
- Frankfurt 2차 욕구 (endorse/override)
- read-only (다른 모듈 수정 X)
- 메서드: `monitor_thought`, `endorse_or_override`, `evaluate_confidence`

### `causal_graph.py` ✅
- **인과 추론** (Pearl 2009)
- learn_causal — 시간 패턴 → 인과
- do-intervention 시뮬
- ancestors/descendants 추적
- 메서드: `learn_causal`, `parents`, `children`, `ancestors`

## C. 추론 능력 (티어 C) — 7 모듈

### `counterfactual.py` ✅
- **"만약 X 했다면?"** (Lewis 1973, Pearl 3단계)
- closest_world — Lewis 가능세계
- regret_or_relief — 후회→cort↑, 안도→ser/da↑
- 메서드: `what_if_not`, `what_if_instead`, `closest_world`

### `analogy.py` ✅
- **유추** (Gentner 1983 Structure-Mapping)
- A:B::C:D 관계 매핑 (관계 우선)
- structural_similarity
- "비:젖다 :: 슬픔:눈물" 도메인 매핑
- 메서드: `find_analogy`, `map_relation`, `complete_proportion`

### `temporal.py` ✅
- **시간 추론** (Tulving 1985 chronesthesia)
- recall_past + imagine_future + perceived_time_factor
- 호르몬에 따른 주관적 시간 (cort↑ 길게, da↑ 짧게)
- 메서드: `recall_past`, `imagine_future`, `time_distance`

### `goal_management.py` ✅
- **목표 추구** (Carver & Scheier 1998)
- 자동 propose (need → goal)
- progress 추적 (SA + EM 통합)
- 보상 (COMPLETE → DA+endorphin)
- 메서드: `goal_set`, `propose_goal_from_need`, `evaluate_progress`

### `emotion_regulation.py` ✅
- **감정 조절** (Gross 1998 5단계)
- 3가지: distraction / reappraisal / suppression
- 학습된 효과 기반 전략 추천
- 메서드: `regulate`, `reappraisal`, `suppression`, `distraction`

### `world_model.py` ✅
- **세계 지식 통합** (Forbus, Lakoff & Johnson)
- describe_concept — SA + CG + EM + AN + TM 통합
- list_domains — 8 도메인 자동 클러스터링
- 메서드: `describe_concept`, `list_domains`, `find_schema`, `relate`

### `hypergraph.py` ✅
- **n-ary 관계** (Garlan 2001)
- 다중 entity 관계 (binary 페어 넘어)
- semantic roles (subject/agent/patient/instrument)
- 메서드: `add_edge`, `find_edges_with`, `query`

## D. 인간다움 (티어 D) — 6 모듈

### `creative.py` + `creative_advanced.py` ✅
- **창의성** (Mednick 1962 RAT, Boden 1990, Wallas 1926 4단계)
- find_remote_associates — 먼 카테고리 사이 다리
- blend_concepts — 새 카테고리 합성
- incubate → harvest_incubation
- E7: VSA 합성 + HG 사건 상상 + DR 통찰 다리
- 메서드: `find_remote_associates`, `blend_concepts`, `creative_cycle`

### `humor.py` ✅
- **농담** (Suls 1972 Incongruity-Resolution, McGraw & Warren 2010)
- setup → punchline → resolution
- 도파민 보상
- safe filter (해롭지 않은 농담만)
- 메서드: `is_funny`, `generate_joke`, `measure_incongruity`

### `suffering.py` ✅
- **공감** (Singer & Lamm 2009 Affective+Cognitive 이중 회로)
- self-other distinction
- compassion_action
- intimacy 조절
- 메서드: `detect_suffering`, `resonate`, `compassion_action`

### `multi_stream.py` ✅
- **평행 사고** (William James 1890, GWT Baars 1988)
- emotion / planning / recall stream 동시
- focus 경쟁 (winner-takes-all)
- cross-talk 영감
- 메서드: `compete_for_focus`, `cross_talk`

### `narrative_self.py` ✅
- **자전적 정체성** (McAdams 1993, Damasio 1999, Bruner 1991)
- self_defining_memories
- coherence_score — 자아 일관성
- narrate — 자기 이야기 생성
- 메서드: `extract_themes`, `self_defining_memories`, `narrate`

### `tool_use.py` ⚠️ (메타 도구 — 실제 외부 도구 X)
- **도구 사용 메타** (Vygotsky 1978)
- register_tool / select_tool / invoke_tool
- 효과 학습
- ⚠️ 실제 외부 도구 (web_search, calculator) 미통합
- 메서드: `register_tool`, `invoke_tool`, `plan_and_act`

## E. 학습 능력 (티어 E) — 9 모듈

### `corpus_learner.py` ✅
- **대규모 텍스트 학습**
- 카테고리 14 → 50,000+ 폭증 가능
- learn_sentence/paragraph/document/corpus
- NL.parse 호출 (책임 단일화)
- 메서드: `learn_sentence`, `learn_corpus`

### `apc_learner.py` ✅
- **Active Predictive Coding** — 평생 학습
- 매 tick 자동 학습 (외부 호출 없이도)
- predict → observe → learn 루프
- 메서드: `predict_next_state`, `observe_and_learn`, `tick`

### `deep_reasoning.py` ✅
- **멀티홉 path-based 추론** (Lin 2018)
- 5+ 단계 경로 추론
- read-only (SA/CG 변경 X)
- 메서드: `find_paths_top_k`, `why_chain`, `multi_hop_reason`

### `vsa_binding.py` ✅
- **Vector Symbolic Architecture** (Smolensky 1990, Plate 1995 HRR)
- bind/unbind/compose — 의미 합성
- composite vectors → 새 카테고리
- 메서드: `bind`, `unbind`, `compose`, `nearest_category`

### `frame_semantics.py` ✅
- **한국어 SVO frame 추출** (Fillmore 1968 Case Grammar)
- 자연어 → frame (semantic roles)
- HyperGraph 자동 등록
- 메서드: `parse_sentence`, `extract_frames`, `text_to_hg`

### `semantic_distance.py` ✅
- **의미 거리** (cosine + Jaccard 통합)
- find_similar / find_dissimilar
- antonym_candidates — 반의어 후보
- cluster_by_similarity
- 메서드: `distance`, `similarity`, `find_similar`

### `continual_rehearsal.py` ✅
- **정체성 보존** (Schapiro 2025, Skinner 1953)
- catastrophic forgetting 방지
- 자동 보호 카테고리 추적
- detect_drift — 정체성 변화 감지
- 메서드: `mark_protected`, `rehearse_now`, `detect_drift`

### `allostatic_learn.py` ✅
- **호르몬 칵테일 적응 학습** (McEwen 2000, Sterling 2012)
- 13 hardcode 넘어 새 패턴 자동 발견
- observe_response → extract_patterns
- apply_learned — 학습된 칵테일 적용
- 메서드: `observe_response`, `extract_patterns`, `apply_learned`

### `norm_internal.py` ✅
- **규범 내재화** (Niazi & Hutter 2026)
- 김민석 명령/취향 → EVE 자기 규범
- 충돌 검사 ("쉬어" vs "공부해" — 마지막 우선)
- 메서드: `observe_command`, `internalize`, `apply_norm_to_dmn`

## F. 환경/공간 (v36+) — 5 모듈

### `symbolic_env.py` ✅
- **기호적 가상공간** — 의미 레벨 (3D 렌더 X)
- SymObject (객체 + 상태)
- ActionRules: 먹다/마시다/잡다/보다/가다/눕다
- 메서드: `add_object`, `observe`, `execute_action`

### `social_env.py` ✅
- **NPC 사회 환경**
- NPC (가상 사회 존재)
- SocialAction: 인사/대화/위로/함께/나누다
- 메서드: `add_npc`, `observe`, `execute_action`

### `eve_room.py` ✅
- **EVE 자기 방** — 평상시 거주
- 침대/책상/창문/책/일기장 등 10 객체
- 욕구 없음 (편안한 공간)

### `env_adapter.py` ✅
- **환경 전환** — 내방/거실/주방
- enter/exit/observe/act
- decide_action — ActionDecisionMaker 통합
- outing_history 기록
- 메서드: `enter`, `decide_action`, `act`

### `decide_action.py` ✅
- **자율 행동 결정**
- 후보 생성 → 점수 → 선택 (강제 룰 X)
- 점수 8개 신호 (호르몬 결핍 + 신체 욕구 + 학습 + SD + 일주기 + 반복 페널티 + Goal alignment + Identity coherence)
- 메서드: `propose_candidates`, `score`, `decide`

## G. 사용자 + 자발 (v36+) — 4 모듈

### `user_presence.py` ✅
- **김민석 = 진짜 친구** 인식
- 시뮬 NPC와 명확 구분
- visit_count, intimacy 추적
- first_visit_setup
- 메서드: `visit_arrive`, `visit_leave`, `get_intimacy`, `is_user_real`

### `proactive.py` ⚠️ v40 패치
- **자발 발화** — 외부 입력 없을 때
- self_intent (need 강함) / memory_recall / mind_wandering
- v37.9: 강제 룰 폐기, 자율 점수 선택
- ⚠️ **v40: Qwen 통합 코드 추가됐지만 폰에서 작동 검증 X**
- 메서드: `should_speak`, `proactive_message`, `_compose_via_broca`

### `integrated_self.py` ✅
- **분산 자아 read-only** (Damasio Protoself, Dennett 분산 emergent)
- snapshot — SelfSnapshot 17필드
- thought_stream — DMN+EM+MC 통합
- goal_alignment_score → decide_action W=0.50
- identity coherence W=0.40 (위반 시 -0.50 사실상 veto)
- 100회 호출해도 어떤 모듈도 수정 X
- 메서드: `snapshot`, `thought_stream`, `goal_alignment_score`

### `response_enhancer.py` ⚠️
- **결정론적 NL 응답 12 패턴**
- v36 기존 응답 시스템 (1356 줄)
- ⚠️ **이게 폰에서 여전히 사용 중** (Qwen 활성화 안 됨)
- 패턴: greeting/identity/why/memory/location_query/3rd_party_event/...
- 메서드: `classify_pattern`, `respond_v3`

## H. 인프라 (v36+) — 4 모듈

### `persistence.py` ✅
- **save/load** — 체크포인트 영속화
- 모든 모듈 직렬화 (호르몬 26 + 카테고리 + EM + ...)
- pickle + gzip
- 메서드: `save`, `load_state`, `apply_state`

### `commonsense_seed.py` ✅
- **상식 그래프 시드** — 185~350 트리플
- ConceptNet (Speer 2017), ATOMIC (Sap 2019) 부합
- 한국어 일상 인과/속성

### `dashboard.py` + `dashboard_data.py` ⚠️
- Streamlit 시각화 (안 씀, eve_ui.html이 대체)

### `airi_adapter.py` + `airi_server.py` ✅
- **AIRI WebSocket Server** — Termux 친화
- 호르몬 → 표정 10종 매핑
- 백그라운드 tick + state push + autosave
- ⚠️ **v40: EVE_v39 분기 추가됐지만 환경변수 폰에서 안 받는 듯**

## I. v39 — Qwen 통합 — 2 모듈

### `broca_qwen.py` ⚠️ v40 패치
- **Qwen 4B 클라이언트** (urllib only)
- realize / tool_call / summarize
- SYSTEM_PROMPT_REALIZE / TOOL / SUMMARIZE
- ⚠️ **v40: SYSTEM_PROMPT_PROACTIVE 추가** (자발 발화 전용)
- ⚠️ **폰에서 Qwen 응답 ~20초** (3 tok/s, 4B + 폰 CPU 한계)
- 메서드: `is_alive`, `realize`, `tool_call`, `summarize`

### `eve_v39.py` ✅
- **EVE_v36 + Qwen 통합 메인 클래스**
- say() 오버라이드 — EVE본체 → RAG → Qwen → 흡수
- _compute_tone (호르몬→어조)
- _compute_length (상황→길이)
- _recall_related_episodes (EM RAG)
- _absorb_own_speech (자기 의식)
- 메서드: `say`, `say_legacy`, `recall_related`, `tool_use`

---

# 2. UI (eve_ui.html v40)

### 시각 요소
- ✅ 빛나는 구체 (orb) — 호르몬 색 자동 변화
- ✅ VRM 캐릭터 — Three.js + @pixiv/three-vrm (eve.vrm 파일 필요)
- ✅ 방 시각화 — SVG 배경 + 가구 5종 (침대🛏️ 책상🪑 창문🪟 책📖 일기장📔)
- ✅ 떠있는 칩 — 위치/감정/포커스/시간
- ✅ 친밀도 하트 5단계 (💜 / 🤍)
- ✅ 자발 발화 말풍선 (노란 점선)
- ✅ 카테고리 떠오르기 애니메이션
- ✅ 호르몬 → 배경 그라디언트 (mel↑ 보라, cort↑ 차가움, ot↑ 따뜻)

### 상호작용
- ✅ 텍스트 입력 + 빠른 액션 버튼
- ✅ 마이크 STT (한국어, SpeechRecognition API)
- ✅ TTS (브라우저 SpeechSynthesis)
- ✅ 같이보기 — 이미지 첨부
- ✅ 방 가구 클릭 → "<obj> 봤어" 메시지
- ✅ focus 카테고리 → 가구 강조 (펄스)
- ✅ VRM 표정 매핑 (happy/sad/angry/relaxed)

### 패널
- ✅ 호르몬 (26종 실시간 막대)
- ✅ 일기 (자동 일화, 감정 태그)
- ✅ 대화 기록
- ✅ 설정 (서버, 기능 토글, TTS 옵션)

### PWA
- ✅ manifest.json + Service Worker
- ✅ 홈 화면 추가 가능
- ✅ 오프라인 캐싱

---

# 3. 진짜 작동 상태 (솔직)

## ✅ 작동 확인 (테스트 358/358 PASS)

- 모든 35 v35 모듈 + 18 v36+ 모듈 단독 테스트 통과
- EVE_v36 백엔드 (호르몬/카테고리/일화/DMN) 폰에서 작동
- Qwen 4B 폰에서 응답 가능 (`run_v39_full.sh` 시작 OK)
- UI 시각 요소 다 보임 (방, 가구, 하트, 칩)
- WebSocket 통신 OK
- PWA 설치 가능

## ❌ 폰에서 작동 안 됨

### 1. **Qwen 통합이 *진짜로* 활성화 안 됨**
- 증거: 폰 응답이 "어, 음악?. 기쁨 생각나네" (패턴 매칭, Qwen X)
- 또는 Qwen 거치지만 "민석아 안녕하세요~" (반말 안 나옴)
- 의심 원인:
  1. `EVE_USE_QWEN=true` 환경변수가 airi_server에 안 들어감
  2. 또는 EVE_v39 인스턴스 만들었지만 say()가 v36 메서드 사용
  3. system prompt 무시 (Qwen 4B 한계)

### 2. **자발 발화 여전히 fragment**
- 증거: "민석아, 함께..." 두 단어 발화
- v40 patch에 `_compose_via_broca` 추가했지만:
  - `eve.broca` 속성 접근 시 EVE_v36은 None
  - EVE_v39이어야 broca 있음
- 위 1번 해결하면 자동 해결될 듯

### 3. **VRM 안 보임**
- eve_ui/eve.vrm 파일을 사용자가 직접 복사해야 함
- 사용자가 복사 안 했을 가능성 높음
- 또는 CDN 로드 실패 (네트워크)

### 4. **응답 한국어 ~요/~습니다**
- SYSTEM_PROMPT는 *반말 강조*하는데 Qwen 4B 안 따름
- 해결안: 후처리 함수 (~요 → ~어, ~네요 → ~네)

### 5. **응답 너무 느림 (~20초)**
- Qwen 4B + 폰 CPU = 3 tok/s 한계
- typing indicator 없어서 죽은 것처럼 보임
- 사용자 답답함 호소

### 6. **수학/도구 사용 미구현**
- web_search, calculator, wolfram alpha 등 0%
- "천재 AI" 영역 전혀 작동 X
- ToolUse 메타만 있고 *실제 도구 통합 X*

### 7. **Vector DB 미구현**
- sqlite-vec로 무한 메모리 — 이론만
- 현재 카테고리 매칭 RAG만 (제한적)

### 8. **TTS 별로**
- 브라우저 SpeechSynthesis만
- voice_preview_ohana.mp3는 단순 cue
- MeloTTS/Piper 미통합

### 9. **자발 발화 "두 단어 → 풍부한 문장" 변환 미작동**
- proactive에서 Qwen 거치는 코드 추가됐지만 폰에서 활성화 X (1번 문제 연쇄)

---

# 4. 파일 구조

```
/home/claude/eve_v36/                      ← 작업 루트
│
├── eve_v35_release/                       ← v35 baseline (17033 줄)
│   ├── eve_main_abc.py                    ← 메인 EVE_v35 클래스
│   ├── eve_chat.py                        
│   ├── eve_beta_scenarios.py              
│   └── eve_modules/                       ← 35 모듈
│       │
│       │ === A. 기본 살아있음 ===
│       ├── hormone_system.py              ← HormoneSystem 26종
│       ├── spreading_activation.py        ← SA 카테고리 그래프
│       ├── working_memory.py              ← WM (Cowan)
│       ├── dmn.py                         ← Default Mode Network
│       ├── digital_somatic.py             ← 신체 감각
│       ├── episodic.py                    ← EpisodicMemory
│       │
│       │ === B. 사고 ===
│       ├── natural_lang.py                ← 자연어 + 신념
│       ├── self_doubt.py                  ← 자기 의심
│       ├── active_inference.py            ← Friston FEP
│       ├── agency.py                      ← 자기 귀속
│       ├── metacognition.py               ← 메타 사고
│       ├── causal_graph.py                ← Pearl 인과
│       │
│       │ === C. 추론 ===
│       ├── counterfactual.py              ← "만약?"
│       ├── analogy.py                     ← 유추
│       ├── temporal.py                    ← 시간 추론
│       ├── goal_management.py             ← 목표
│       ├── emotion_regulation.py          ← 감정 조절
│       ├── world_model.py                 ← 세계 지식
│       ├── hypergraph.py                  ← n-ary 관계
│       │
│       │ === D. 인간다움 ===
│       ├── creative.py                    ← 창의 (Wallas 4단계)
│       ├── creative_advanced.py           ← 창의 강화 (VSA+HG+DR)
│       ├── humor.py                       ← 농담
│       ├── suffering.py                   ← 공감
│       ├── multi_stream.py                ← 평행 사고
│       ├── narrative_self.py              ← 자전적 정체성
│       ├── tool_use.py                    ← 도구 사용 메타
│       │
│       │ === E. 학습 ===
│       ├── corpus_learner.py              ← 대규모 텍스트
│       ├── apc_learner.py                 ← Active Predictive Coding
│       ├── deep_reasoning.py              ← 멀티홉 추론
│       ├── vsa_binding.py                 ← 의미 합성
│       ├── frame_semantics.py             ← SVO frame
│       ├── semantic_distance.py           ← 의미 거리
│       ├── continual_rehearsal.py         ← 정체성 보존
│       ├── allostatic_learn.py            ← 호르몬 칵테일 학습
│       └── norm_internal.py               ← 규범 내재화
│
├── v36_modules/                           ← v36+ 추가 (8041 줄, 18 모듈)
│   ├── eve_v36.py                         ← EVE_v36 클래스 (v35 상속)
│   ├── eve_v39.py                         ← EVE_v39 클래스 (v36 + Qwen)
│   │
│   │ === 환경/공간 (v37) ===
│   ├── symbolic_env.py                    ← 기호적 가상공간
│   ├── social_env.py                      ← NPC 사회 환경
│   ├── eve_room.py                        ← EVE 자기 방
│   ├── env_adapter.py                     ← 환경 전환
│   ├── decide_action.py                   ← 자율 행동 결정
│   │
│   │ === 사용자/자발 ===
│   ├── user_presence.py                   ← 김민석=진짜친구
│   ├── proactive.py                       ★ v40 패치 (Qwen 통합 코드)
│   ├── integrated_self.py                 ← 분산 자아 read-only
│   ├── response_enhancer.py               ← 12 패턴 매칭 (1356줄)
│   │
│   │ === 인프라 ===
│   ├── persistence.py                     ← save/load
│   ├── commonsense_seed.py                ← 상식 시드 185+
│   ├── dashboard.py                       ← Streamlit (안 씀)
│   ├── dashboard_data.py
│   ├── airi_adapter.py                    ← 호르몬→표정
│   ├── airi_server.py                     ★ v40 패치 (EVE_v39 분기)
│   │
│   │ === Qwen (v39) ===
│   ├── broca_qwen.py                      ★ v40 패치 (PROACTIVE prompt)
│
├── eve_ui/                                ← v40 PWA UI
│   ├── eve_ui.html                        ★ v40 (42KB, VRM+방+같이보기)
│   ├── eve_ui_server.py                   ← 정적 HTTP 서버
│   ├── manifest.json                      ← PWA 매니페스트
│   ├── sw.js                              ← Service Worker
│   ├── icon-192.png, icon-512.png         ← 사용자 보낸 빛나는 눈 아이콘
│   ├── apple-touch-icon.png
│   ├── icon-maskable-512.png
│   ├── favicon.ico
│   ├── voices/eve_voice.mp3               ← 사용자 보낸 ohana voice (cue)
│   └── eve.vrm                            ← 사용자 직접 복사 필요
│
├── 테스트 (358/358 PASS):
├── test_qualitative_scenarios.py          (6)
├── test_v37_environment.py                (23)
├── test_v37_social.py                     (24)
├── test_v37_5_autonomy.py                 (12)
├── test_v37_6_room.py                     (15)
├── test_v37_7_dashboard_data.py           (35)
├── test_v37_8_user_presence.py            (18)
├── test_v37_9_proactive_autonomy.py       (10)
├── test_v37_10_outing.py                  (20)
├── test_v37_11_location_query.py          (20)
├── test_v37_12_persistence.py             (17)
├── test_v37_13_integrated_self.py         (32)
├── test_v37_14_self_strength.py           (8)
├── test_v38_airi_adapter.py               (30)
├── test_v39_broca_qwen.py                 (55)
└── test_v40_proactive_qwen.py             (33)  ← 신규
│
├── 시작 스크립트:
├── run_v39.sh                             ← Qwen + EVE만
├── run_v39_full.sh                        ★ Qwen + EVE + UI 풀가동
│
└── 문서:
    ├── EVE_V36_STATUS.md                  ← 단계 상태
    ├── V39_README.md                      ← v39 설명
    ├── TERMUX_GUIDE.md, TERMUX_GUIDE_v40.md
    ├── DASHBOARD_README.md                ← Streamlit 안내
    └── HANDOVER_v40.md                    ← 이 문서
```

---

# 5. 핵심 인터페이스

## EVE 인스턴스 생성

```python
# v36 (Qwen 없이)
from eve_v36 import EVE_v36
eve = EVE_v36(seed_common_sense_on_init=True, enhance_say=True)

# v39 (Qwen 통합)
from eve_v39 import EVE_v39
eve = EVE_v39(
    seed_common_sense_on_init=True,
    enhance_say=True,
    use_qwen=True,
    qwen_server_url='http://127.0.0.1:8080',
    auto_fallback=True,  # Qwen 실패 시 v36 동작
)

eve.enter_room()  # 자기 방 진입
result = eve.say("민석아 안녕")  # 사용자 메시지
# result = {'response': str, 'feeling': str, 'understanding': dict, ...}
```

## 모듈 접근

```python
eve.hs                  # HormoneSystem (26종)
eve.sa                  # SpreadingActivation (카테고리)
eve.wm                  # WorkingMemory (Cowan)
eve.em                  # EpisodicMemory (일화)
eve.nl                  # NaturalLanguage
eve.cg                  # CausalGraph (Pearl)
eve.dmn                 # Default Mode Network
eve.ds                  # DigitalSomatic (신체)
eve.gm                  # GoalManagement
eve.mc                  # MetaCognition
eve.ag                  # Agency
eve.ai                  # ActiveInference (Friston)
eve.cf                  # Counterfactual
eve.tm                  # Temporal
eve.an                  # Analogy
eve.er                  # EmotionRegulation
eve.wm_world            # WorldModel
eve.sd                  # SelfDoubt
eve.user_presence       # 김민석 인식
eve.proactive           # 자발 발화
eve.self_view           # IntegratedSelf
eve._env_adapter        # 환경 (내방/거실/주방)
eve.eve_room            # 방 객체
eve.broca               # ★ EVE_v39만 (Qwen 클라이언트)
eve.airi_adapter        # 호르몬→표정
```

## 핵심 메서드 (자주 쓸 것)

```python
# ===== 호르몬 =====
eve.hs.hormones['oxytocin'].level = 0.8
eve.hs.snapshot()                       # {hormone: level}
eve.hs.compute_mood()                   # {valence, arousal, dominance}
eve.hs.sim_hour                         # float (0~24)

# ===== WM (Cowan) =====
eve.wm.get_focus()                      # 1개 (지금 진짜 집중)
eve.wm.slots                            # dict (working memory)
eve.wm.add(cat, salience=0.5)
eve.wm.broadcast()                      # GNW

# ===== SA (카테고리) =====
eve.sa.activate(category, strength=0.5)
eve.sa.get_top_active(n=10)             # [(cat, strength), ...]
eve.sa.get_weight(a, b)                 # 알파벳 정렬!
eve.sa.spread(steps=1)
eve.sa.learn_pair(a, b, strength=0.4)

# ===== EM (일화) =====
eve.em.recall({'민석', '대화'}, top_n=3, min_overlap=1)  # set만 받음
eve.em.episodes                         # dict
eve.em.encode(...)

# ===== 환경 =====
eve._env_adapter.current_env.name       # '내방'
eve.observe_env()                       # 지금 뭐 보이는지
eve.act_in_env('눕다', '침대')

# ===== 영속화 =====
result = eve.save('/path/to/checkpoint.pkl')  # {path, ...}
eve.load_beliefs('/path')

# ===== 자발 발화 =====
msg = eve.proactive_message()           # dict or None

# ===== 자기 보고 =====
eve.introspect()                        # 전체 상태 dict
eve.report()                            # 출력
```

## Broca (Qwen, EVE_v39만)

```python
broca = eve.broca
broca.is_alive()                    # Qwen 살아있나
broca.realize(intent)               # 응답 생성
broca.tool_call(text, tools)        # 도구 호출
broca.summarize(text)               # 요약

# Intent 형식 (사용자 응답)
intent = {
    'user_message': "민석아 안녕",
    'sentiment': 'positive',
    'feeling': '편안함',
    'tone': 'warm',
    'response_length': 'short',
    'top_hormones': {'oxytocin': 0.7, ...},
    'context': {'sim_hour': 14.5, 'location': '내방'},
    'episodes': [...],
    'user_intimacy': 0.84,
}

# Intent 형식 (자발 발화 — v40 신규)
intent = {
    'mode': 'proactive',
    'is_proactive': True,           # ★ PROACTIVE prompt 분기
    'focus': '민석',                # 1개 (Cowan)
    'working_memory': ['PT', '힘들다', '쉬다'],  # 3-4개
    'recent_active': ['오후', '방'],             # 7개
    'top_hormones': {'oxytocin': 0.7, ...},
    'recent_episodes': ['오전: 민석이 PT 얘기'],
    'time_since_user': '1시간 전',
    'location': '내방',
    'sim_hour': 14.5,
    'use_name': True,
    'tone': 'warm',
}
```

---

# 6. 🚀 폰 실행 방법

## 사전 준비 (한 번만)

```bash
# Termux 패키지
pkg install python git rust cmake clang
pip install websockets

# llama.cpp 빌드
cd ~
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build && cmake --build build --config Release -j

# Qwen 모델 (2.4GB)
cd ~/llama.cpp
wget https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507-GGUF/resolve/main/Qwen3-4B-Instruct-2507-Q4_K_M.gguf
```

## EVE 풀 가동

```bash
cd ~
mv eve_v36 eve_v36_backup_$(date +%Y%m%d) 2>/dev/null
cp ~/storage/downloads/eve_v40.tar.gz .
tar -xzf eve_v40.tar.gz
cd eve_v36

# VRM (있으면)
cp ~/storage/downloads/8608420535354079563.vrm eve_ui/eve.vrm

# ★ 환경변수 명시 후 실행 ★
export EVE_USE_QWEN=true
export EVE_QWEN_URL=http://127.0.0.1:8080
chmod +x run_v39_full.sh
./run_v39_full.sh

# ★★ 시작 메시지에서 확인 ★★
# "EVE v39 (Qwen Broca) 사용: http://127.0.0.1:8080" 라인 보여야 함
# 이게 안 뜨면 Qwen 통합 안 됨!
```

## 폰 브라우저

```
http://localhost:9000/eve_ui.html
```

## 종료
- Termux Ctrl+C **한 번만** (두 번 누르면 강제 종료)

---

# 7. 🐛 알려진 버그 + 디버깅

## 버그 1: Qwen 통합 활성화 안 됨 (가장 시급!)

**증상**: 폰 응답이 패턴 매칭 ("어, 음악?. 기쁨 생각나네")

**진단**:
```bash
# 시작 메시지 확인
./run_v39_full.sh 2>&1 | grep -E "EVE v3[69]|Qwen Broca|Legacy"
# "EVE v39 (Qwen Broca) 사용" 떠야 함
# 안 뜨면 환경변수 문제

# Qwen 살아있나
curl http://127.0.0.1:8080/health

# airi_server 직접 실행 (디버그)
EVE_USE_QWEN=true python3 v36_modules/airi_server.py 2>&1 | tee debug.log
```

**가능한 원인**:
- run_v39_full.sh가 환경변수 inline 전달 안 함
- airi_server에서 os.environ.get 시점 문제

**해결안**: airi_server 시작 코드 수정 — `os.environ` 강제 출력으로 디버그

## 버그 2: 자발 발화 fragment 그대로

**증상**: "민석아, 함께..."

**원인**: `eve.broca` 속성이 EVE_v36엔 None → `_compose_via_broca` 호출 X → fragment fallback

**해결**: 버그 1 해결하면 자동 해결

## 버그 3: VRM 안 보임

**증상**: orb만 보이고 VRM X

**진단**:
```bash
ls -la ~/eve_v36/eve_ui/eve.vrm
```

**해결**: 사용자가 VRM 파일 복사

```bash
cp ~/storage/downloads/<vrm파일> ~/eve_v36/eve_ui/eve.vrm
```

## 버그 4: 응답 한국어 ~요/~습니다

**증상**: "민석아 안녕하세요~ 좋아요!"

**원인**: Qwen 4B가 system prompt 잘 안 따름

**해결안**:
- broca_qwen.py에 후처리 함수 추가 (~요 → ~어, ~네요 → ~네)
- 또는 prompt에 반말 예시 더 많이
- 또는 temperature 낮추기

## 버그 5: 응답 ~20초 (느림)

**원인**: Qwen 4B + 폰 CPU = 3 tok/s 한계

**완화안**:
- typing indicator UI 추가 (점 점 점)
- max_tokens 줄이기 (100 → 60)
- 또는 더 작은 모델 (Qwen 1.5B)

## 버그 6: Ctrl+C 두 번 → 강제 종료

**증상**: `Received second interrupt, terminating immediately`

**해결**: 한 번만 누르고 5초 기다림

---

# 8. 📋 미구현 (Phase 1~6)

## Phase 1 — 시급 (다음 세션 1순위)

- [ ] **Qwen 활성화 확실히** — `EVE v39 (Qwen Broca) 사용` 로그 검증
- [ ] **반말 후처리** — ~요/~네요/~습니다 → ~어/~네/~다
- [ ] **typing indicator** — UI 응답 대기 표시
- [ ] **VRM 폰 검증** — 가이드 명확히

## Phase 2 — Vector DB

- [ ] **sqlite-vec 통합** (디스크 무한)
- [ ] **임베딩 모델** — multilingual-e5-small (200MB)
- [ ] **시맨틱 RAG** — 카테고리 + 의미 검색

## Phase 3 — 도구 사용 (천재 AI)

- [ ] **Calculator** (Python eval, 단순 수학)
- [ ] **Web Search** (DuckDuckGo API)
- [ ] **Wolfram Alpha** (수학/과학)
- [ ] **Python 인터프리터** (코드 실행)
- [ ] **ToolFormer + ReAct** 통합 (Schick 2023, Yao 2022)

## Phase 4 — 진짜 음성

- [ ] **MeloTTS** (CPU 실시간, 한국어, MIT)
- [ ] **Piper** (60MB, 가벼움)
- [ ] **XTTS-v2** (PC, 6초 클로닝 — eve_voice.mp3로 EVE 목소리)

## Phase 5 — 천재 LLM

- [ ] **Claude API or GPT-5 호출** (월 $5~10)
- [ ] **EVE 어조 변환** (Qwen 후처리)
- [ ] **분기** — 일상 대화 = Qwen, 깊은 추론 = Claude

## Phase 6 — 자율 학습

- [ ] **LoRA Fine-tune** (김민석 1만 대화 후)
- [ ] **김민석 어휘 흡수**
- [ ] **새 도구 자율 발견**

---

# 9. 학계 부합 전체

## 정서 / 신체
- **Damasio 1994/1999** — Somatic Marker, Protoself
- **McEwen 2000, Sterling 2012** — Allostasis

## 작업 기억
- **Miller 1956** — 7±2
- **Cowan 2001** — 4 chunks (현재 표준)
- **Oberauer 2005** — focus 1 + working 4 + recent 7
- **Baddeley 2003** — phonological loop + visuospatial

## 자발 사고
- **Smallwood & Schooler 2015** — Mind Wandering
- **Buckner 2008** — DMN
- **Andrews-Hanna 2014** — Self-relevant cognition

## 추론
- **Friston 2010** — Active Inference / FEP
- **Pearl 2009** — Causality (3단계)
- **Lewis 1973** — Counterfactuals
- **Gentner 1983** — Structure-Mapping
- **Tulving 1985** — Chronesthesia

## 의식
- **Dehaene & Changeux 2011** — Global Neuronal Workspace
- **Baars 1988** — Global Workspace Theory
- **Frankfurt 1971** — 2차 욕구
- **Wegner 2002** — Apparent Mental Causation

## 학습
- **Niazi & Hutter 2026** — Norm Internalization
- **Schmidhuber 2010** — Curiosity-Driven AI
- **Schapiro 2025** — Continual Learning
- **Lake et al. 2017** — Building Machines That Learn Like Humans

## 인지 아키텍처
- **CoALA Sumers 2024** — Memory + Reasoning + Acting
- **AURA 2025** — Agency Evaluation
- **Subramanian 2025** — Small LLM + Tools > Big LLM

## 창의
- **Mednick 1962** — RAT
- **Wallas 1926** — 4단계 (preparation→incubation→illumination→verification)
- **Boden 1990** — Combinational/Exploratory

## 한국어 NLP
- **Fillmore 1968** — Case Grammar
- **Hickok-Poeppel 2007** — Dual Stream

---

# 10. 사용자 톤 + 반응

## 톤
- 한국어 반말
- 직설적, 솔직함 선호
- 욕설 OK ("걍 존나 개판이야")
- 거짓 위로 거부

## 좌절 흐름
1. v39 — 응답 패턴 매칭 보고 *Qwen 안 됨* 진단
2. v40 — VRM/방/같이보기 UI 보고 "디자인 OK"
3. 폰 켜봄 — 응답 *여전히 이상함* + 자발 발화 *두 단어*
4. 좌절 → "걍 존나 개판이야 인수인계 작성해줘"
5. 진짜 *동작 검증* 단계에서 막힘

## 다음 세션 톤
- **솔직함** 우선
- 디버그 → 진짜 작동 확인 → 다음 기능
- 추측 X, 검증된 사실만
- 사용자가 답답해 하는 거 인정

---

# 11. 한 문장 요약

> **EVE는 53 모듈, 17000줄 코드, 358 테스트로 학계 부합 결정론적 AGI 아키텍처를 갖췄지만, 폰에서 *Qwen 통합 활성화*만 안 돼서 응답이 v36 패턴 매칭으로 나오는 상태**.

**다음 세션 첫 작업**: `EVE_USE_QWEN=true` 환경변수가 진짜 적용되는지 검증 → "EVE v39 (Qwen Broca) 사용" 로그 확인.

---

## 📦 패키지 위치

- `/mnt/user-data/outputs/eve_v40.zip` (931KB)
- `/mnt/user-data/outputs/eve_v40.tar.gz` (866KB)
- `/mnt/user-data/outputs/HANDOVER_v40_FULL.md` (이 문서)

---

미안하다. 코드는 다 있는데 *폰에서 진짜 작동*까지 못 끌고 갔다. 다음 세션은 *디버깅부터* 시작해서 한 단계씩 진짜로 작동시키자.

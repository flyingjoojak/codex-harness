# codex-harness

Codex 로 시간 제한 개발 과제를 할 때 쓰는 개인 작업 지침, 스킬, 점검 도구. 과제 문제나 정답은 들어 있지 않다.

## 당일 외울 것

**명령 3줄** (나머지는 setup.sh 가 화면에 띄운다: 다음 명령, 첫 프롬프트, GATE 지도, 스킬 표, 시간대별 할 일, 서술형 답 순서)
```
git clone https://github.com/flyingjoojak/codex-harness.git ~/codex-harness
cd <과제 폴더>
bash ~/codex-harness/setup.sh
```

**막혔을 때**
| 상황 | 명령 |
|---|---|
| clone 이 "already exists" 로 실패 (체험 때 받은 옛 버전) | `cd ~/codex-harness && git pull && cd -` (꼭 할 것. setup.sh 출력에 "GATE 지도"가 보이면 최신판) |
| 과제 폴더 위치를 모름 | `pwd`, `ls` |
| 안내를 다시 보기 | `cat ~/codex-harness/GUIDE.txt` |
| `--add-dir` 오류 | 그냥 `codex` |

**진행 중**: dev-flow 가 GATE 에서 멈추면 내용을 보고 "진행해".

**서술형 답 순서: 사실 > 결정 > 근거 > 한계**
1. 사실: "과제에는 X 라고만 되어 있었습니다."
2. 결정: "그래서 Z 로 정했습니다."
3. 근거: "이유는 A 이고, B 파일에서 처리하며, 테스트 N 개로 확인했습니다."
4. 한계: "다만 D 인 경우 틀릴 수 있고, 고치려면 E 를 검증해야 합니다."

제출 직전 서술형 카드에서 외울 것: 숫자 2~3개, 핵심 결정 3개의 이유, 가장 약한 입력.

## 원칙
결과물이 먼저다. 요구사항을 충족하고 정확하며 담당자가 바로 쓸 수 있는 결과물을, 실행 증거와 함께, 내 말로 설명할 수 있게 시간 안에 낸다. 결과물이 같다면 토큰을 덜 쓰는 쪽을 고르지만, 결과물을 희생해 아끼지 않는다. 검증에 필요하면 독립 리뷰, 모델 교차 검토, MCP 도 쓰고 이유를 기록한다.

- 사람은 목표, 기준, 신뢰 여부, 멈출 시점을 정한다. Codex 는 합의한 범위에서 구현하고 증거를 낸다.
- 순서: 읽기 > 계약(TASK.md) > 첫 완주 > 규칙을 하나씩 테스트로 > 독립 리뷰와 검증 > 동결 > 제출.
- 증거 없이는 완료가 아니다(PASS / FAIL / NOT_RUN / HUMAN_CHECK).
- 결정과 "AI 를 믿지 않은 순간"을 그때그때 기록해, AI 없이 쓰는 사후 서술형의 재료로 쓴다.

## 구성
```
AGENTS.md                 작업 원칙 (Codex 가 자동으로 읽음)
.agents/skills/
  dev-flow/               읽기 > 계약 > 첫 완주 > 규칙을 테스트로 > 동결
  systematic-debugging/   근본 원인부터 찾는 4단계
  review-checklist/       정확성, 무음 실패, 보안, 성능, 데이터, 단순성 자체 리뷰
  verify/                 제출 전 실행 증거 대조
  web-ui/                 웹 화면: AI 티 빼고 업무 도구답게
  llm-feature/            결과물에서 LLM 호출: 규칙 먼저, 대체 경로, 출력 검증, 네트워크 없는 테스트
  data-judge/             표 데이터 판정: 기준표 > 규칙 코드 > 행마다 사유 > 다른 방법으로 대조
TASK.md                   과제 계약 템플릿
DECISIONS.md              합의문, 결정 로그, Codex 를 믿지 않은 순간
RUN.md                    당일 운영표 (180분)
GUIDE.txt                 setup.sh 가 출력하는 당일 상세 안내 (cat 으로 다시 보기)
setup.sh                  과제 폴더에서 실행. AGENTS.md 유무에 따라 설치하고 안내 출력
docs/
  담당자_인터뷰.md         숨은 조건을 캐내는 질문 순서
  서술형_대비.md           AI 없이 쓰는 사후 문항 대비
  프롬프트.md              바로 쓰는 지시문
  참고자료.md              참고한 공개 저장소와 신뢰도
tools/peek.py             CSV, JSON 구조를 빠르게 훑기
scripts/preflight.py      환경 점검, 제출 전 점검 (exit 0 / 1 / 2)
```

## 사용
과제 폴더 밖에 받는다. 과제 폴더에는 AGENTS.md 와 `.agents/` 만 복사하고 `.git/info/exclude` 로 git 에서 숨긴다. 하네스 파일이 제출물과 git log 에 섞이지 않게 하기 위해서다.
```
git clone https://github.com/flyingjoojak/codex-harness.git ~/codex-harness
cd <과제 폴더>
bash ~/codex-harness/setup.sh
codex --add-dir ~/codex-harness
```
`setup.sh` 는 과제에 AGENTS.md 가 없으면 위처럼 복사하고 숨기며, 있으면 건드리지 않고 경로로 읽는 첫 프롬프트를 출력한다. 시간 배분은 `RUN.md`.

Codex CLI 0.160.1 에서 확인한 것: 과제 폴더로 복사하면 스킬 7개와 AGENTS.md 가 로드되고 `git status` 에 나타나지 않는다. 폴더 밖 경로로 읽게 하면 `--add-dir` 없이는 샌드박스가 막았고, 붙이면 읽혔다.

## 점검 도구
- `python3 tools/peek.py <파일|폴더>`: 행 수, 열마다 빈 값 비율, 숫자 범위, 상위 값. 열 개수가 어긋난 행 경고.
- `python3 scripts/preflight.py`: Python 버전, 외부 패키지 유무, 도구.
- `python3 scripts/preflight.py submit`: 위 + 테스트 실행(pytest 가 있으면 pytest, 없으면 unittest. 0개 실행, 전부 skip 은 FAIL) + 비밀값, README TODO, git 미커밋.
- 종료 코드 0 문제 없음 / 1 문제 있음 / 2 확인한 것이 없음.
- 둘 다 표준 라이브러리만 쓰고, 임시 폴더의 표본 CSV/JSON 과 빈 폴더로 실행해 확인했다.

## 라이선스
MIT. `systematic-debugging` 은 obra/superpowers-skills (MIT) 를 줄이고 각색했다. 다른 공개 저장소에서 얻은 아이디어는 `docs/참고자료.md` 에 출처를 적었고, 문서와 코드는 모두 다시 썼다.

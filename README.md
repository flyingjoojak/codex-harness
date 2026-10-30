# codex-harness

Codex 로 시간 제한 개발 과제를 할 때 쓰는 개인 작업 지침, 스킬, 점검 도구. 과제 문제나 정답은 들어 있지 않다.

## 구성
```
AGENTS.md                 작업 원칙 (Codex 가 자동으로 읽음)
.agents/skills/
  dev-flow/               읽기 > 계약 > 첫 완주 > 규칙을 테스트로 > 동결
  systematic-debugging/   근본 원인부터 찾는 4단계
  review-checklist/       정확성, 무음 실패, 보안, 성능, 데이터, 단순성 자체 리뷰
  verify/                 제출 전 실행 증거 대조
TASK.md                   과제 계약 템플릿
DECISIONS.md              합의문, 결정 로그, Codex 를 믿지 않은 순간
RUN.md                    당일 운영표 (180분)
docs/
  담당자_인터뷰.md         숨은 조건을 캐내는 질문 순서
  서술형_대비.md           AI 없이 쓰는 사후 문항 대비
  프롬프트.md              바로 쓰는 지시문
  참고자료.md              참고한 공개 저장소와 신뢰도
tools/peek.py             CSV, JSON 구조를 토큰 적게 훑기
scripts/preflight.py      환경 점검, 제출 전 점검 (exit 0 / 1 / 2)
```

## 사용
과제 폴더 밖에 받는다. 과제 폴더에는 AGENTS.md 와 `.agents/` 만 복사하고 `.git/info/exclude` 로 git 에서 숨긴다. 하네스 파일이 제출물과 git log 에 섞이지 않게 하기 위해서다.
```
git clone https://github.com/flyingjoojak/codex-harness.git ~/codex-harness
cd <과제 폴더>
cp -rn ~/codex-harness/AGENTS.md ~/codex-harness/.agents ~/codex-harness/TASK.md ~/codex-harness/DECISIONS.md .
printf 'AGENTS.md\n.agents/\n' >> .git/info/exclude
codex
```
과제에 이미 AGENTS.md 가 있을 때(`codex --add-dir ~/codex-harness`), 첫 프롬프트, 시간 배분은 `RUN.md`.

Codex CLI 0.160.1 에서 확인한 것: 과제 폴더로 복사하면 스킬 4개와 AGENTS.md 가 로드되고 `git status` 에 나타나지 않는다. 폴더 밖 경로로 읽게 하면 `--add-dir` 없이는 샌드박스가 막았고, 붙이면 읽혔다.

## 점검 도구
- `python3 tools/peek.py <파일|폴더>`: 행 수, 열마다 빈 값 비율, 숫자 범위, 상위 값. 열 개수가 어긋난 행 경고.
- `python3 scripts/preflight.py`: Python 버전, 외부 패키지 유무, 도구.
- `python3 scripts/preflight.py submit`: 위 + unittest 실행(0개 실행, 전부 skip 은 FAIL) + 비밀값, README TODO, git 미커밋.
- 종료 코드 0 문제 없음 / 1 문제 있음 / 2 확인한 것이 없음.
- 둘 다 표준 라이브러리만 쓰고, 임시 폴더의 표본 CSV/JSON 과 빈 폴더로 실행해 확인했다.

## 라이선스
MIT. `systematic-debugging` 은 obra/superpowers-skills (MIT) 를 줄이고 각색했다. 다른 공개 저장소에서 얻은 아이디어는 `docs/참고자료.md` 에 출처를 적었고, 문서와 코드는 모두 다시 썼다.

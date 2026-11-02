# 당일 운영표

과제 최대 180분 + 서술형 6문항 x 5분. 14:00 종료, 연장 없음. 제출 확정 뒤 문항 생성에 5~10분 걸린다는 후기가 있다.

## 09:40 전
- 노트북, 휴대폰 충전기 연결. 휴대폰은 Wi-Fi. 실물 신분증. 유선 마우스.
- 09:40 전후로 오는 추가 안내 메일(자리 이탈, 식음료 규정)을 읽는다.

## 시작 직후 (5분)
웹 터미널 붙여넣기는 `Ctrl+Shift+V` 일 수 있다. 하네스는 **과제 폴더 밖**에 받는다. 안에 통째로 받으면 하네스 파일이 제출물과 git log 에 섞인다.

### 명령 세 줄 (AGENTS.md 가 있든 없든 같다)
```
git clone https://github.com/flyingjoojak/codex-harness.git ~/codex-harness
cd <과제 폴더>
bash ~/codex-harness/setup.sh
```
`setup.sh` 가 과제 AGENTS.md 유무를 보고 아래 A 또는 B 를 해 주고, 다음 명령과 첫 프롬프트를 출력한다. 기존 파일은 덮어쓰지 않는다. 그다음 `codex --add-dir ~/codex-harness`.

### 방법 A: 과제 폴더에 AGENTS.md 가 없을 때
setup.sh 가 AGENTS.md 와 `.agents/` 를 복사하고 `.git/info/exclude` 로 git 에서 숨긴다. Codex 가 AGENTS.md 와 `$스킬` 을 자동으로 읽는다.
- `/skills` 에 dev-flow, systematic-debugging, review-checklist, verify 가 보이는지 확인.
- 첫 프롬프트:
  > AGENTS.md 를 따른다. 적용한 지침을 3줄로 요약한 뒤 $dev-flow 1단계부터 시작해. 아직 코드는 쓰지 마.
- TASK.md, DECISIONS.md 는 숨기지 않는다. 작업 기록이자 제출물이다.

### 방법 B: 과제 폴더에 이미 AGENTS.md 가 있을 때
setup.sh 는 과제 AGENTS.md 를 건드리지 않고 TASK.md, DECISIONS.md 만 복사한다. 하네스는 경로로 읽게 한다. 작업 폴더 밖 읽기가 막힐 수 있어 `--add-dir` 를 붙인다.
- 첫 프롬프트:
  > 과제 AGENTS.md 가 우선이고, 부딪히지 않는 범위에서 ~/codex-harness/AGENTS.md 도 따른다. 스킬은 필요할 때 ~/codex-harness/.agents/skills/<이름>/SKILL.md 를 읽어서 쓴다. 적용한 지침을 3줄로 요약한 뒤 dev-flow 1단계부터 시작해. 아직 코드는 쓰지 마.

### 공통
- `/status` 로 모델과 권한을 확인하고, `/model` 로 모델을 고른다(권장 6.1 Sol / 5.6 Terra / 6.0 Luna).
- 커밋이 권한 문제로 막히면 터미널에서 직접 `git commit` 한다.

## 시간 배분 (180분)
| 경과 | 할 일 | 끝 조건 |
|---|---|---|
| 0~20분 | 읽기, 담당자 DM, TASK.md 범위 세 칸(필수 / 개선 / 안 함). GATE 1~3 은 1분씩 | 필수가 70분 안에 될 크기 |
| 20~70분 | 필수만으로 첫 완주(Docker 요구면 Docker 실행까지) | 제출 파일, 실행 확인, 커밋 |
| 70~120분 | 개선 태스크. 태스크마다 UNDERSTANDING.md 한 칸 + 내 한 줄 설명 확인 | **120분에 기능 추가 멈춤** |
| 120~140분 | 독립 리뷰(기다리는 동안 UNDERSTANDING 요약), CRITICAL/HIGH 수정 | 지적 사항 처리, 테스트 통과 |
| 140~145분 | `python3 ~/codex-harness/scripts/preflight.py submit` | FAIL 0 |
| 145~165분 | **동결.** UNDERSTANDING 직접 읽고 막히는 줄 질문, 서술형 카드, $verify, README | 요약 4줄, README 에 TODO 0 |
| 165~170분 | 제출: "제출하고 문제풀기" > 미리보기 > "제출물 확정하고 문제풀기" | 확정 후 수정 불가 |
| 대기 5~10분 | `docs/서술형_대비.md` 마지막 절 | 답 3개 준비 |

- 늦게 시작하면 14:00 에서 거꾸로 계산한다: 서술형 30분 + 문항 생성 10분 + 제출 5분을 빼면 작업 마감이다.
- 70분에 첫 완주가 안 됐으면 범위를 줄인다. 제출이 개선보다 먼저다.
- 15분 넘게 막히면 독립 세션(`codex exec --sandbox read-only`)에 원인 조사를 맡기거나 `/model` 로 모델을 바꿔 다시 본다. 30분이 넘으면 범위 조정을 사람에게 묻고, 빼기로 하면 `안 할 일` 로 옮겨 기록한다.

## 화면과 도구
- 서버가 필요하면 `0.0.0.0` 으로 바인딩하고, Codex 와 다른 터미널 탭에서 띄운다. 확인은 내장 브라우저로.
- Codex 를 멈출 때는 `Esc`, 그 다음 "그게 아니라 ~" 로 정정.
- 대화가 길어지면 HANDOFF.md 를 쓰게 한 뒤 `/new`(`docs/프롬프트.md` 참고).
- MCP, 플러그인, 서브에이전트는 품질에 도움이 될 때 쓰고 이유를 DECISIONS.md 에 남긴다. 수정은 메인 세션에서만.
- 140분에 별도 터미널에서 `codex exec --sandbox read-only` 로 독립 리뷰를 받는다(GUIDE.txt 참고).
- 가끔 `/status` 로 사용량을 본다. 시작할 때 종료 시각과 35% 시각, 동결 시각을 TASK.md 맨 위에 적어 두면 Codex 도 시간을 기준으로 범위를 줄인다.

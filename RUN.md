# 당일 운영표

과제 최대 180분 + 서술형 6문항 x 5분. 14:00 종료, 연장 없음. 제출 확정 뒤 문항 생성에 5~10분 걸린다는 후기가 있다.

## 09:40 전
- 노트북, 휴대폰 충전기 연결. 휴대폰은 Wi-Fi. 실물 신분증. 유선 마우스.
- 09:40 전후로 오는 추가 안내 메일(자리 이탈, 식음료 규정)을 읽는다.

## 시작 직후 (5분)
웹 터미널 붙여넣기는 `Ctrl+Shift+V` 일 수 있다. 하네스는 **과제 폴더 밖**에 받는다. 안에 받으면 하네스 파일이 제출물과 git log 에 섞인다.
```
git clone https://github.com/flyingjoojak/codex-harness.git ~/codex-harness
cd <과제 폴더>
cp -n ~/codex-harness/TASK.md ~/codex-harness/DECISIONS.md .
python3 ~/codex-harness/scripts/preflight.py
codex
```
- `/status` 로 모델과 권한을 확인하고, `/model` 로 모델을 고른다(권장 6.1 Sol / 5.6 Terra / 6.0 Luna).
- 첫 프롬프트(설정 변경 없이 경로로 읽히는 방식):
  > ~/codex-harness/AGENTS.md 를 이 세션 지침으로 따른다. 스킬은 필요할 때 ~/codex-harness/.agents/skills/<이름>/SKILL.md 를 읽어서 쓴다. 적용한 지침을 3줄로 요약한 뒤 dev-flow 1단계부터 시작해. 아직 코드는 쓰지 마.
- 과제 폴더에 이미 AGENTS.md 가 있으면 그것이 과제 지침이다. 덮어쓰지 않는다.
- 선택: `$스킬` 로 부르고 싶으면 `mkdir -p ~/.agents/skills && cp -rn ~/codex-harness/.agents/skills/* ~/.agents/skills/` 후 Codex 를 다시 열고 `/skills` 로 확인. 사용자 폴더 스킬 경로가 이 버전에서 읽히는지는 사전 체험에서 확인하지 못했으면 쓰지 않는다.
- 커밋이 권한 문제로 막히면 터미널에서 직접 `git commit` 한다.

## 시간 배분 (180분)
| 경과 | 할 일 | 끝 조건 |
|---|---|---|
| 0~25분 | 읽기, TASK.md, 담당자 인터뷰 | 한 문장, 안 할 일, 완료 조건이 있음 |
| 25~60분 | 첫 완주 | 제출 파일이 실제로 생성되고 형식 확인됨. 커밋 |
| 60~140분 | 완료 조건 하나씩 테스트로, 엣지 케이스 | TASK.md 5번 표가 PASS 로 바뀜 |
| 140~145분 | `python3 ~/codex-harness/scripts/preflight.py submit` | FAIL 0 |
| 145~165분 | **동결.** $review-checklist, $verify, README 정리 | README 에 TODO 0 |
| 165~170분 | 제출: "제출하고 문제풀기" > 미리보기 > "제출물 확정하고 문제풀기" | 확정 후 수정 불가 |
| 대기 5~10분 | `docs/서술형_대비.md` 마지막 절 | 답 3개 준비 |

- 늦게 시작하면 14:00 에서 거꾸로 계산한다: 서술형 30분 + 문항 생성 10분 + 제출 5분을 빼면 작업 마감이다.
- 60분에 첫 완주가 안 됐으면 범위를 줄인다. 제출이 개선보다 먼저다.
- 같은 문제로 15분 넘게 막히면 그 기능을 `안 할 일` 로 돌리고 기록한다.

## 화면과 도구
- 서버가 필요하면 `0.0.0.0` 으로 바인딩하고, Codex 와 다른 터미널 탭에서 띄운다. 확인은 내장 브라우저로.
- Codex 를 멈출 때는 `Esc`, 그 다음 "그게 아니라 ~" 로 정정.
- 대화가 길어지면 HANDOFF.md 를 쓰게 한 뒤 `/new`(`docs/프롬프트.md` 참고).
- MCP, 플러그인, 서브에이전트를 새로 켜지 않는다. 토큰이 늘고 기록이 흐려진다.
- 60, 90, 120, 150분에 `/status` 로 토큰 사용량을 본다. 시작할 때 종료 시각과 35% 시각, 동결 시각을 TASK.md 맨 위에 적어 두면 Codex 도 시간을 기준으로 범위를 줄인다.

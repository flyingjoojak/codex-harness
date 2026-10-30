# 당일 운영표

## 09:40 전
- 노트북, 휴대폰 충전기 연결. 휴대폰 Wi-Fi. 신분증. 유선 마우스.
- 감독 앱 연결, 촬영 각도 확인.

## 시작 직후 (5분)
```
git clone https://github.com/<계정>/<저장소>.git harness
cd harness
codex
```
- `/status` 로 모델, 권한 확인. `/model` 로 모델 선택.
- `/skills` 에 dev-flow, systematic-debugging, review-checklist, verify 가 보이는지 확인.
- 과제 폴더가 따로 있으면 `AGENTS.md`, `.agents/`, `TASK.md`, `DECISIONS.md` 를 과제 폴더로 복사하고 거기서 `codex` 를 실행.
- 첫 프롬프트:
  > AGENTS.md 를 따른다. $dev-flow 로 시작해. 과제는 다음과 같다: (과제 붙여넣기 또는 파일 경로)

## 시간 배분 (과제 180분 기준)
| 경과 | 할 일 | 끝 조건 |
|---|---|---|
| 0~15분 | 계약: TASK.md, 가정 확인 | 인수 기준이 문장으로 있음 |
| 15~30분 | 계획 + 테스트 먼저 | 테스트가 실패로 돌아감 |
| 30~90분 | 최소본 구현 | **제출 가능한 최소본 커밋** |
| 90~140분 | 개선, 엣지 케이스 | 단계마다 커밋 |
| 140~165분 | $review-checklist, $verify | 통과 표 |
| 165~180분 | 제출, DECISIONS.md 다듬기 | 제출 완료 |

- 90분에 최소본이 없으면 범위를 줄인다. 개선보다 제출이 먼저.
- 같은 문제로 15분 넘게 막히면 $systematic-debugging, 그래도 안 되면 그 기능을 범위 밖으로 돌리고 DECISIONS.md 에 적는다.

## 서술형 직전 (과제 끝나고 바로)
- `DECISIONS.md`, `TASK.md`, `git log --oneline` 을 한 번 읽는다. 서술형은 AI 없이 쓴다.

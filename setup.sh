#!/usr/bin/env bash
# 과제 폴더에서 실행: bash ~/codex-harness/setup.sh
# 과제 AGENTS.md 가 없으면 지침과 스킬을 복사하고 git 에서 숨긴다(방법 A).
# 있으면 건드리지 않고 경로로 읽는 첫 프롬프트를 알려준다(방법 B).
# 어느 경우든 기존 파일은 덮어쓰지 않는다.
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"

if [ "$(pwd)" = "$KIT" ]; then
  echo "하네스 폴더가 아니라 과제 폴더에서 실행하세요."; exit 1
fi

git rev-parse --git-dir >/dev/null 2>&1 || { git init -q; echo "git 저장소가 없어 git init 했습니다."; }
cp -n "$KIT/TASK.md" "$KIT/DECISIONS.md" . 2>/dev/null || true
EXCLUDE="$(git rev-parse --git-path info/exclude)"
mkdir -p "$(dirname "$EXCLUDE")"
grep -qx '.pytest_cache/' "$EXCLUDE" 2>/dev/null || printf '__pycache__/
.pytest_cache/
' >> "$EXCLUDE"

if [ -e AGENTS.md ]; then
  echo
  echo "[방법 B] 과제에 AGENTS.md 가 이미 있습니다. 건드리지 않았습니다."
  echo "다음 명령: codex --add-dir $KIT"
  echo "첫 프롬프트:"
  echo "  과제 AGENTS.md 가 우선이고, 부딪히지 않는 범위에서 $KIT/AGENTS.md 도 따른다. 스킬은 필요할 때 $KIT/.agents/skills/<이름>/SKILL.md 를 읽어서 쓴다. 적용한 지침을 3줄로 요약한 뒤 dev-flow 1단계부터 시작해. 아직 코드는 쓰지 마."
else
  cp -n "$KIT/AGENTS.md" .
  if [ -e .agents ]; then
    cp -rn "$KIT/.agents/skills" .agents/ 2>/dev/null || true
  else
    cp -r "$KIT/.agents" .
  fi
  grep -qx 'AGENTS.md' "$EXCLUDE" 2>/dev/null || printf 'AGENTS.md\n.agents/\n' >> "$EXCLUDE"
  echo
  echo "[방법 A] AGENTS.md 와 스킬을 복사했고 git 에서 숨겼습니다."
  echo "다음 명령: codex --add-dir $KIT"
  echo "첫 프롬프트:"
  echo "  AGENTS.md 를 따른다. 적용한 지침을 3줄로 요약한 뒤 \$dev-flow 1단계부터 시작해. 아직 코드는 쓰지 마."
fi

echo
python3 "$KIT/scripts/preflight.py" || true

cat <<'GUIDE'

==================== 오늘 할 일 ====================
[지금]
 1. codex --add-dir ~/codex-harness   (오류 나면 그냥 codex)
 2. /model 에서 6.1 Sol 선택
 3. 위에 나온 첫 프롬프트 붙여넣기 (붙여넣기 안 되면 Ctrl+Shift+V)
 4. 3줄 요약이 나오는지 확인

[진행 중]
 - 약 20분: Codex 가 "진행할까요?"에서 멈춤
     > TASK.md 직접 읽고 확인
     > Codex 가 준 질문을 DM 담당자에게 보내고, 답을 Codex 에 붙여넣기
 - 60분: STATE 입력 > 첫 완주가 커밋됐는지 확인. 아니면 "범위 줄여"
 - 커밋마다: "방금 변경을 3줄로 설명해"
 - AI 가 틀린 걸 잡으면: "DECISIONS.md 의 Codex 를 믿지 않은 순간에 한 줄 적어"
 - 같은 오류 2번: "고치지 말고 원인 가설 두 개와 확인 방법을 먼저 말해"
 - 140분: $review-checklist > $verify
 - 145분: 동결. 기능 추가 금지
 - 165~170분: 제출하고 문제풀기 > 미리보기 > 제출물 확정하고 문제풀기

[서술형 전 대기 시간]
 - TASK.md 7번, DECISIONS.md 다시 읽기
 - 답 3개 준비: 상충 조건 / 가장 위험한 실패 / Codex 를 믿지 않은 곳
 - 답 틀: 사실 > 결정 > 근거(파일, 숫자) > 한계

[막히면]
 - git commit 오류(who you are):
     git config user.name "flyingjoojak"
     git config user.email "flyingjoojak@users.noreply.github.com"
 - $스킬 이 안 되면: ".agents/skills/<이름>/SKILL.md 읽고 따라"
 - 대화가 길어지면: "HANDOFF.md 써" > /new > "AGENTS.md, TASK.md, DECISIONS.md, HANDOFF.md 읽고 이어서 해"
 - 이 안내 다시 보기: bash ~/codex-harness/setup.sh  (다시 실행해도 안전)
====================================================
GUIDE

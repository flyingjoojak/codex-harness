#!/usr/bin/env python3
"""모의 과제용 가짜 데이터 생성. 1회차 과제 모양(참가자 공개 기록)을 재구성했다. 실제 시험 데이터가 아니다.

사용: python3 ~/codex-harness/mock/make_data.py <출력 폴더>
만드는 것: datasets/clean/, datasets/dirty/ 각각 stops.csv, members.csv, shifts.csv
"""
import csv
import random
import sys
from pathlib import Path

SEED = 31


def build(rng):
    stops = [("DEPOT", "회사", 0.0, 0.0)]
    for i in range(1, 25):
        stops.append((f"S{i:02d}", f"정류장{i}", round(rng.uniform(-15, 15), 2), round(rng.uniform(-15, 15), 2)))
    shifts = [("D", "06:00"), ("M", "09:00"), ("E", "14:00"), ("N", "22:00")]
    members = []
    for i in range(1, 321):
        stop = rng.choice(stops[1:])[0]
        shift = rng.choices(["D", "M", "E", "N"], weights=[4, 3, 2, 1])[0]
        members.append((f"E{i:04d}", f"구성원{i}", stop, shift))
    return stops, members, shifts


def write(folder, stops, members, shifts):
    folder.mkdir(parents=True, exist_ok=True)
    for name, header, rows in [
        ("stops.csv", ["stop_id", "name", "x_km", "y_km"], stops),
        ("members.csv", ["member_id", "name", "stop_id", "shift_id"], members),
        ("shifts.csv", ["shift_id", "start_time"], shifts),
    ]:
        with open(folder / name, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rng = random.Random(SEED)
    stops, members, shifts = build(rng)
    write(out / "datasets" / "clean", stops, members, shifts)

    # 검증에서 걸러야 할 문제를 일부러 넣는다(정답 개수는 mock/담당자_답변.md 맨 아래)
    dirty = list(members)
    dirty.append(dirty[5])                                    # 중복 구성원
    dirty.append(("E9001", "구성원9001", "S99", "D"))         # 없는 정류장
    dirty.append(("E9002", "구성원9002", "S03", "X"))         # 없는 근무 조
    dirty.append(("E9003", "", "", "M"))                      # 빈 값
    d_stops = list(stops) + [("S25", "정류장25", "", "3.1")]  # 좌표 빈 값
    d_shifts = list(shifts) + [("X2", "25:00")]               # 잘못된 시각
    write(out / "datasets" / "dirty", d_stops, dirty, d_shifts)
    print(f"생성: {out / 'datasets'} (clean 구성원 {len(members)}명, dirty 문제 행 6개)")


if __name__ == "__main__":
    main()

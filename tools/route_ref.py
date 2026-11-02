#!/usr/bin/env python3
"""통근 노선 생성 참고 구현. 표준 라이브러리만. 과제 코드에 그대로 복사하지 말고 구조를 참고한다.

문제: 근무 조(같은 도착 목표 시각)마다, 정류장의 탑승 인원을 차량 정원 안에서 묶어
      회사(DEPOT)에 '근무 시작 - 여유' 시각에 도착하는 노선을 만든다.
방법: 정류장별 직행에서 시작 > 절약(savings) 병합 > 노선 안 순서 2-opt > 정류장 옮기기.
      병합 기준은 차량 수만이 아니라 비용 = 차량 가중치 + 승객 탑승 시간 합.
검사: validate() 는 생성 코드와 따로 계획을 다시 계산해 조건 위반을 센다.

사용: python3 tools/route_ref.py   (작은 예제로 자체 검사)
"""
from itertools import combinations
from math import hypot

DEPOT = "DEPOT"


class Params:
    def __init__(self, capacity, max_ride, slack, dwell=1, vehicle_weight=60):
        self.capacity = capacity              # 차량 정원(명)
        self.max_ride = max_ride              # 승객 최대 탑승 시간(분). 같으면 허용
        self.slack = slack                    # 근무 시작 몇 분 전 도착
        self.dwell = dwell                    # 정류장 정차 시간(분)
        self.vehicle_weight = vehicle_weight  # 차량 1대를 승객-분 몇 분으로 볼지(담당자에게 확인할 값)


def euclid_time(coords, speed=0.5):
    """좌표(같은 단위)와 속도(단위/분)로 이동 시간 함수. 과제에 시간 행렬이 있으면 그것을 쓴다."""
    def t(a, b):
        (x1, y1), (x2, y2) = coords[a], coords[b]
        return hypot(x1 - x2, y1 - y2) / speed
    return t


def ride_times(route, t, p):
    """route = [(stop, load), ...] 탑승 순서. 각 정류장 승객의 탑승 시간(분)."""
    rides, acc = [], 0.0
    nxt = DEPOT
    for stop, _ in reversed(route):
        acc += t(stop, nxt) + p.dwell
        rides.append(acc)
        nxt = stop
    return rides[::-1]


def feasible(route, t, p):
    if sum(load for _, load in route) > p.capacity:
        return False
    return ride_times(route, t, p)[0] <= p.max_ride  # 첫 정류장 승객이 가장 오래 탄다


def cost(route, t, p):
    return p.vehicle_weight + sum(load * r for (_, load), r in zip(route, ride_times(route, t, p)))


def direct_routes(demand, p):
    """기준선: 정류장별 직행. 정원을 넘는 정류장은 나눈다."""
    routes = []
    for stop, n in sorted(demand.items()):
        while n > 0:
            routes.append([(stop, min(n, p.capacity))])
            n -= p.capacity
    return routes


def merge_savings(routes, t, p):
    # ponytail: 매 회 모든 쌍을 본다 O(R^3). 조당 정류장 수백 개를 넘으면 savings 목록 정렬 방식으로 바꾼다.
    routes = [list(r) for r in routes]
    while True:
        best = None
        for i, j in combinations(range(len(routes)), 2):
            a, b = routes[i], routes[j]
            for merged in (a + b, b + a):
                if not feasible(merged, t, p):
                    continue
                gain = cost(a, t, p) + cost(b, t, p) - cost(merged, t, p)
                if gain > 1e-9 and (best is None or gain > best[0]):
                    best = (gain, i, j, merged)
        if best is None:
            return routes
        _, i, j, merged = best
        routes = [r for k, r in enumerate(routes) if k not in (i, j)] + [merged]


def two_opt(route, t, p):
    best, improved = list(route), True
    while improved:
        improved = False
        for i, j in combinations(range(len(best) + 1), 2):
            cand = best[:i] + best[i:j][::-1] + best[j:]
            if feasible(cand, t, p) and cost(cand, t, p) < cost(best, t, p) - 1e-9:
                best, improved = cand, True
    return best


def relocate(routes, t, p):
    """정류장 하나를 다른 노선의 가장 좋은 자리로 옮겨 비용이 줄면 옮긴다."""
    routes, improved = [list(r) for r in routes], True
    while improved:
        improved = False
        for i, src in enumerate(routes):
            for k, item in enumerate(src):
                rest = src[:k] + src[k + 1:]
                base = cost(src, t, p) - (cost(rest, t, p) if rest else 0)
                for j, dst in enumerate(routes):
                    if j == i:
                        continue
                    for pos in range(len(dst) + 1):
                        cand = dst[:pos] + [item] + dst[pos:]
                        if feasible(cand, t, p) and cost(cand, t, p) - cost(dst, t, p) < base - 1e-9:
                            routes[i], routes[j] = rest, cand
                            routes = [r for r in routes if r]
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
    return routes


def plan_shift(demand, t, p):
    routes = merge_savings(direct_routes(demand, p), t, p)
    routes = relocate([two_opt(r, t, p) for r in routes], t, p)
    return [two_opt(r, t, p) for r in routes]


def schedule(route, t, p, arrive_at):
    """도착 시각(분)에서 거꾸로 각 정류장 출발 시각을 구한다."""
    return [(stop, load, arrive_at - r) for (stop, load), r in zip(route, ride_times(route, t, p))]


def metrics(routes, t, p):
    rides = [(load, r) for rt in routes for (_, load), r in zip(rt, ride_times(rt, t, p))]
    return {
        "vehicles": len(routes),
        "passenger_minutes": round(sum(l * r for l, r in rides), 1),
        "max_ride": round(max(r for _, r in rides), 1),
        "avg_ride": round(sum(l * r for l, r in rides) / sum(l for l, _ in rides), 1),
    }


def validate(routes, demand, t, p):
    """생성 코드와 따로 다시 센다. 위반 목록을 돌려준다(빈 목록이면 통과)."""
    errors, served = [], {}
    for n, rt in enumerate(routes):
        load = sum(l for _, l in rt)
        if load > p.capacity:
            errors.append(f"노선 {n}: 정원 초과 {load}>{p.capacity}")
        ride, nxt = 0.0, DEPOT
        for stop, l in reversed(rt):
            ride += t(stop, nxt) + p.dwell
            nxt = stop
            if ride > p.max_ride:
                errors.append(f"노선 {n}: {stop} 탑승 {ride:.1f}분 > {p.max_ride}")
            served[stop] = served.get(stop, 0) + l
    for stop in set(demand) | set(served):
        if demand.get(stop, 0) != served.get(stop, 0):
            errors.append(f"{stop}: 수요 {demand.get(stop, 0)} / 배정 {served.get(stop, 0)}")
    return errors


if __name__ == "__main__":
    coords = {DEPOT: (0, 0), "A": (10, 0), "B": (11, 1), "C": (0, 10),
              "D": (1, 11), "E": (-8, -8), "F": (20, 0)}
    t = euclid_time(coords)
    p = Params(capacity=20, max_ride=60, slack=15)
    demand = {"A": 6, "B": 5, "C": 7, "D": 4, "E": 3, "F": 26}

    base = direct_routes(demand, p)
    plan = plan_shift(demand, t, p)
    assert validate(base, demand, t, p) == []
    assert validate(plan, demand, t, p) == [], validate(plan, demand, t, p)
    mb, mp = metrics(base, t, p), metrics(plan, t, p)
    assert mp["vehicles"] < mb["vehicles"]
    # 잘못된 계획은 검사기가 잡아야 한다
    assert validate([[("A", 6)]], demand, t, p) != []
    assert validate([[("F", 26)]], {"F": 26}, t, p) != []

    shift_start = 8 * 60
    for n, rt in enumerate(plan):
        stops = ", ".join(f"{s}({l}명 {m // 60:02.0f}:{m % 60:02.0f})"
                          for s, l, m in schedule(rt, t, p, shift_start - p.slack))
        print(f"노선 {n}: {stops} > {DEPOT}")
    print("기준선(직행):", mb)
    print("생성 계획   :", mp)
    print("OK")

n, m, k = map(int, input().split())
image = [list(map(int, list(input().strip()))) for _ in range(n)]

t = int(input())
cost = [[(i - j) ** 2 for j in range(10)] for i in range(10)]
for _ in range(t):
    a, b, c = map(int, input().split())
    cost[a][b] = c
    cost[b][a] = c

INF = 10**15
segments_cache = {}

def generate_segments(orig, k):
    if (orig, k) in segments_cache:
        return segments_cache[(orig, k)]

    if k == 2:
        target_sum = orig * 2
        segs = []
        for x in range(10):
            y = target_sum - x
            if 0 <= y <= 9:
                penalty = cost[x][y]
                segs.append((x, y, penalty))
        segments_cache[(orig, k)] = segs
        return segs

    target_sum = orig * k
    max_sum = 9 * k

    dp_prev = [[[INF]*10 for _ in range(max_sum+1)] for _ in range(10)]
    dp_cur = [[[INF]*10 for _ in range(max_sum+1)] for _ in range(10)]

    for pix in range(10):
        if pix <= max_sum:
            dp_prev[pix][pix][pix] = 0

    for pos in range(1, k):
        for last in range(10):
            for s in range(max_sum+1):
                for start in range(10):
                    cur_penalty = dp_prev[last][s][start]
                    if cur_penalty == INF:
                        continue
                    for next_pix in range(10):
                        ns = s + next_pix
                        if ns > max_sum:
                            continue
                        penalty = cur_penalty + cost[last][next_pix]
                        if penalty < dp_cur[next_pix][ns][start]:
                            dp_cur[next_pix][ns][start] = penalty
        dp_prev, dp_cur = dp_cur, [[[INF]*10 for _ in range(max_sum+1)] for _ in range(10)]

    segs = []
    for start in range(10):
        for end in range(10):
            val = dp_prev[end][target_sum][start]
            if val < INF:
                segs.append((start, end, val))

    segments_cache[(orig, k)] = segs
    return segs

total_penalty = 0

for row in image:
    dp = [INF]*10
    for last_pixel in range(10):
        dp[last_pixel] = 0

    for i in range(m):
        segs = generate_segments(row[i], k)
        new_dp = [INF]*10
        for prev_last in range(10):
            base_penalty = dp[prev_last]
            if base_penalty == INF:
                continue
            for start, end, inside_penalty in segs:
                trans_penalty = 0 if i == 0 else cost[prev_last][start]
                val = base_penalty + inside_penalty + trans_penalty
                if val < new_dp[end]:
                    new_dp[end] = val
        dp = new_dp

    total_penalty += min(dp)

print(total_penalty)

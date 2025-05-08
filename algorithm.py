def knapsack(capacity, W, V):
    if W is None or V is None or len(W) != len(V) or capacity < 0:
        raise ValueError("Invalid input")
    capacity = int(round(capacity))
    N = len(W)
    DP = [[0] * (capacity + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        w = int(round(W[i - 1]))
        v = V[i - 1]
        for sz in range(1, capacity + 1):
            DP[i][sz] = DP[i - 1][sz]
            if sz >= w and DP[i - 1][sz - w] + v > DP[i][sz]:
                DP[i][sz] = DP[i - 1][sz - w] + v
    sz = capacity
    items_selected = []
    for i in range(N, 0, -1):
        if DP[i][sz] != DP[i - 1][sz]:
            idx = i - 1
            items_selected.append(idx)
            sz -= int(round(W[idx]))
    items_selected.reverse()
    return DP[N][capacity], items_selected
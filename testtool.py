import math
from scipy.special import erf

def analyze_lsb_distribution(n, total, rand_func):
    zero_count = one_count = 0
    for _ in range(total):
        val = rand_func(n)
        if val & 1 == 0:
            zero_count += 1
        else:
            one_count += 1

    expected = total / 2
    chi = ((zero_count - expected) ** 2 + (one_count - expected) ** 2) / expected

    print(">> 检查最低比特分布")
    print(f"0 出现次数: {zero_count}")
    print(f"1 出现次数: {one_count}")
    print(f"卡方统计量: {chi:.4f}\n")

def analyze_value_spread(n, total, rand_func):
    freq = [0] * n
    for _ in range(total):
        val = rand_func(n)
        freq[val] += 1

    expected = total / n
    chi = sum((f - expected) ** 2 / expected for f in freq)
    p_val = 1.0 - 0.5 + erf(math.sqrt(chi / (2 * n)))

    print(">> 整体分布均匀性检测")
    print(f"卡方值: {chi:.4f}, P值: {p_val:.4f}\n")

def analyze_pattern_test(n, total, rand_func):
    group_size = 4
    groups = total // group_size
    stats = [0] * 5

    for _ in range(groups):
        items = [rand_func(n) for _ in range(group_size)]
        counts = [0] * n
        for val in items:
            counts[val] += 1

        max_ct = max(counts)
        pair_ct = counts.count(2)

        if max_ct == 4:
            stats[4] += 1
        elif max_ct == 3:
            stats[3] += 1
        elif max_ct == 2:
            stats[1 if pair_ct == 1 else 2] += 1
        else:
            stats[0] += 1

    theoretical = [
        (n * (n - 1) * (n - 2) * (n - 3)) / n**4,
        (6 * n * (n - 1) * (n - 2)) / n**4,
        (3 * n * (n - 1)) / n**4,
        (4 * n * (n - 1)) / n**4,
        n / n**4
    ]

    chi = sum((o - e * groups) ** 2 / (e * groups) for o, e in zip(stats, theoretical))

    print(">> 扑克分布 m=4")
    print("各模式出现次数:", stats)
    print(f"卡方值: {chi:.4f}\n")

def analyze_run_count(n, total, rand_func):
    sequence = [rand_func(n) for _ in range(total)]
    runs = 1 + sum(1 for i in range(1, total) if sequence[i] != sequence[i-1])

    expected = 1 + (total - 1) * (n - 1) / n
    variance = (total - 1) * (n - 1) / (n ** 2)
    std_dev = math.sqrt(variance)
    z_score = (runs - expected) / std_dev if std_dev > 0 else 0

    print(">> 游程分析")
    print(f"总游程数: {runs}")
    print(f"期望值: {expected:.2f}, Z值: {z_score:.4f}\n")

def analyze_third_diff(n, total, rand_func):
    if total < 4:
        print("样本不足以做三阶差分检测\n")
        return

    bits = [0 if rand_func(n) < n/2 else 1 for _ in range(total)]
    diff1 = [bits[i] ^ bits[i+1] for i in range(total - 1)]
    diff2 = [diff1[i] ^ diff1[i+1] for i in range(total - 2)]
    diff3 = [diff2[i] ^ diff2[i+1] for i in range(total - 3)]

    zeros = diff3.count(0)
    ones = len(diff3) - zeros
    expected = len(diff3) / 2
    chi = ((zeros - expected) ** 2 + (ones - expected) ** 2) / expected

    print(">> 三阶差分分析")
    print(f"0: {zeros}, 1: {ones}, 卡方: {chi:.4f}\n")

import math
import random
import testtool  # 引入上面的模块

# 参数
N = 10
num_samples = 1000000
RAND_MAX = 32767

# rand()%N
def gen_basic(n):
    r = int(random.random() * (RAND_MAX + 1))
    return r % n

# 均匀分布
def gen_mapped_uniform(n):
    return random.randint(0, n - 1)

# 正态分布
def gen_normal_like(n):
    mean = (n - 1) / 2
    sigma = n / 5
    u, v = random.random(), random.random()
    z = math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
    val = int(round(mean + sigma * z))
    return max(0, min(n - 1, val))

# 主函数
def main():

    generators = [
        ("rand()%N", gen_basic),
        ("均匀分布", gen_mapped_uniform),
        ("正态分布", gen_normal_like)
    ]

    for name, func in generators:
        print(f"{f'- {name} -':^50}")
        testtool.analyze_lsb_distribution(N, num_samples, func)
        testtool.analyze_value_spread(N, num_samples, func)
        testtool.analyze_pattern_test(N, num_samples, func)
        testtool.analyze_run_count(N, num_samples, func)
        testtool.analyze_third_diff(N, num_samples, func)

    print("所有测试完成。")

if __name__ == "__main__":
    main()

from int_convolve import *
import random
from time import time

def test_int_convolve(iters, max_size, num_bits):
    M = 2 ** num_bits
    tot_time = 0
    for i in range(iters):
        len_A = random.randint(0, max_size)
        len_B = random.randint(1, max_size)
        A = [random.randint(-M, M) for j in range(len_A)]
        B = [random.randint(-M, M) for j in range(len_B)]
        naive = naive_int_convolve(A,B)
        ss = time()
        fast = int_convolve(A,B)
        ee = time()
        tot_time += ee-ss
        assert naive == fast, (A,B, naive, fast)
    print(f"int_convolve passed {iters} random tests with array sizes "
          f"<= {max_size}, and bits per integer <= {num_bits}. "
          f"test time = {round(tot_time, 3)}s.")

def benchmark_int_convolve(size, num_bits):
    from time import time
    M = 2 ** num_bits
    A = [random.randint(-M, M) for i in range(size)]
    B = [random.randint(-M, M) for i in range(size)]
    ss = time()
    C = int_convolve(A, B)
    ee = time()
    print(f"{round(ee-ss, 4)}s for int_convolve {size} x {size} "
          f"with numbers of bit length {num_bits}.")

if __name__ == "__main__":
    test_int_convolve(iters=2**15, max_size = 10, num_bits=1)
    test_int_convolve(iters=2**15, max_size = 10, num_bits=2)
    test_int_convolve(iters=2**15, max_size = 10, num_bits=10)
    test_int_convolve(iters=2**15, max_size = 10, num_bits=100)

    benchmark_int_convolve(size=2**19, num_bits=100)

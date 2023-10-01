try:
    import gmpy2

    if gmpy2.version() != "2.1.2":
        raise ImportError(
            "This code was written under gmpy2 version 2.1.2."
            f"Your current gmpy2 version is {gmpy2.version()}."
            "It is possible that this code ."
        )

    def get_num_limbs(num):
        bytes_per_num = 0
        while 256 ** bytes_per_num <= num:
            bytes_per_num += 1
        return bytes_per_num

    def arr_to_int(arr, bytes_per_num):
        last_idx = len(arr)-1
        # guaranteed non-zero array
        while arr[last_idx] == 0:
            last_idx -= 1
        total_sgn = (arr[last_idx] < 0)
        bins = []
        sgn = 0
        if total_sgn:
            for i in range(last_idx+1):
                num = - arr[i] - sgn
                sgn = (num < 0)
                bins.append(num.to_bytes(bytes_per_num, "little", signed=True))
        else:
            for i in range(last_idx+1):
                num = arr[i] - sgn
                sgn = (num < 0)
                bins.append(num.to_bytes(bytes_per_num, "little", signed=True))
        res_arr = bytes([1, 1 + total_sgn]) + b"".join(bins)
        res = gmpy2.from_binary(res_arr)
        return res

    def int_to_arr(num, length, bytes_per_num):
        bits = gmpy2.to_binary(num) + b"\x00"
        # if 1 then negative. if 0 then positive.
        total_sgn = bits[1] - 1
        # assert total_sgn == 0 or total_sgn == 1
        res = [0] * length
        idx = 2
        sgn = 0
        last_idx = length - 1
        if total_sgn:
            for i in range(last_idx):
                num = int.from_bytes(bits[idx: idx+bytes_per_num], byteorder='little', signed=True)
                res[i] = -(sgn + num)
                sgn = (num < 0)
                idx += bytes_per_num
            res[last_idx] = -(sgn + int.from_bytes(bits[idx: idx+bytes_per_num], byteorder='little', signed=False))
        else:
            for i in range(last_idx):
                num = int.from_bytes(bits[idx: idx+bytes_per_num], byteorder='little', signed=True)
                res[i] = sgn + num
                sgn = (num < 0)
                idx += bytes_per_num
            res[last_idx] = (sgn + int.from_bytes(bits[idx: idx+bytes_per_num], byteorder='little', signed=False))
        return res

    def int_multiply(A, B):
        return gmpy2.mul(A,B)

except ImportError as e:
    import logging
    logging.warn("\nThe faster version of int_convolve encountered an error:\n"
                 f"{e}\n"
                 "Defaulting to the slower version of int_convolve.\n")
    
    def arr_to_int_impl(arr, a, b, bits):
        if b - a == 1:
            return arr[a]
        mid = (a+b)//2
        return arr_to_int_impl(arr, a, mid, bits) + (
            arr_to_int_impl(arr, mid, b, bits) << (bits * (mid - a)))

    def int_to_arr_impl(num, out, a, b, bits):
        if b-a == 1:
            if num > (1 << (bits-1)):
                out[a] = num - (1 << bits)
                return 1
            else:
                out[a] = num
                return 0
        else:
            mid = (a+b)//2
            L = (mid - a) * bits
            carry = int_to_arr_impl(num & ((1 << L) - 1), out, a, mid, bits)
            return int_to_arr_impl((num >> L) + carry, out, mid, b, bits)

    def get_num_limbs(num):
        bits_per_num = 0
        while (1 << bits_per_num) <= num:
            bits_per_num += 1
        return bits_per_num
    
    def arr_to_int(arr, bits_per_num):
        return arr_to_int_impl(arr, 0, len(arr), bits_per_num)

    def int_to_arr(num, length, bits_per_num):
        res = [0] * length
        int_to_arr_impl(num, res, 0, length, bits_per_num)
        return res

    def int_multiply(A, B):
        return A*B

def int_convolve(A, B):
    if len(A) == 0 or len(B) == 0: return []
    max_A = max(max(A), -min(A))
    max_B = max(max(B), -min(B))
    min_len = min(len(A), len(B))
    max_num = 2 * min_len * max_A * max_B
    res_len = len(A) + len(B) - 1

    if max_num == 0:
        return [0] * res_len

    num_limbs = get_num_limbs(max_num)

    num_A = arr_to_int(A, num_limbs)
    num_B = arr_to_int(B, num_limbs)

    num_res = int_multiply(num_A, num_B)

    res = int_to_arr(num_res, res_len, num_limbs)

    return res

def naive_int_convolve(f, g):
    if len(f) == 0 or len(g) == 0: return []
    res = [0] * (len(f)+len(g)-1)
    for i, ff in enumerate(f):
        for j, gg in enumerate(g):
            res[i+j] += ff*gg
    return res

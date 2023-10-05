# int_convolve
Relatively efficient convolution of arbitrary-precision integer arrays in Python.

It is likely possible to significantly improve efficiency when the input has more specific format, say only positive numbers, or only 32-bit integers.

On my 2022 laptop, it takes 2.1 seconds for `2^19 x 2^19` convolution with `100`-bit ints.

[The SO thread](https://stackoverflow.com/a/77210071/2506343) that asked for such an implementation.


## Algorithms

The algorithm that is implementedin this package follows the following steps:

1. Estimate the largest element that will appear in the output (convolution array). Call `B` the number of bytes it takes to represent such a number.
2. Transform each input array to a bigint, with each element of the array stored in `B` bytes of the number (padded with leading zeros).
3. Multiply the two bigints using GMP package (through `gmpy2`).
4. Digest consecutive blocks of `B` bits from the product integer, interpret them as integers, and store them in the output array.


Two reasons why this algorithm is not best possible:
+ Steps 2,4 take significant amount of running time. That is a drawback of the implementation, as algorithmically these steps should be negligible.
+ Integer multiplication is algorithmically more complex (and likely slightly slower) than corresponding array convolution.


Another approach to consider is to split each number into smaller blocks of bits (10-20 bits per block) and use a two-dimensional array convolution (using the FFT) without worrying about numerical errors. This approach is likely somewhat slower than the above approach, but it has not been thoroughly tested.

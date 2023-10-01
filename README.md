# int_convolve
Relatively efficient convolution of arbitrary-precision integer arrays in Python.

It is likely possible to significantly improve efficiency when the input has more specific format, say only positive numbers, or only 32-bit integers.

On my 2022 laptop, it takes 2.1 seconds for `2^19 x 2^19` convolution with `100`-bit ints.

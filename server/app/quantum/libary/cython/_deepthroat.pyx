#-*- coding: utf-8-*-
#cython: language_level=3
#cython: boundscheck=False
#cython: wraparound=False

cimport numpy as np

cpdef double fmax(double[:] arr):
    cdef:
        double r = -1.7976931348623157e+308
        Py_ssize_t x
    for x in range(arr.shape[0]):
        if arr[x] != arr[x]:
            continue
        if arr[x] > r:
            r = arr[x]
    return r

cpdef double fargmax(double[:] arr):
    cdef:
        double r = -1.7976931348623157e+308
        Py_ssize_t x, y
    for x in range(arr.shape[0]):
        if arr[x] != arr[x]:
            continue
        if arr[x] > r:
            r = arr[x]
            y = x
    return y

cpdef long imax(long[:] arr):
    cdef:
        long r = -9223372036854775807
        Py_ssize_t x
    for x in range(arr.shape[0]):
        if arr[x] > r:
            r = arr[x]
    return r

cpdef long iargmax(long[:] arr):
    cdef:
        long r = -9223372036854775807
        Py_ssize_t x, y
    for x in range(arr.shape[0]):
        if arr[x] > r:
            r = arr[x]
            y = x
    return y

cpdef double fmin(double[:] arr):
    cdef:
        double r = 1.7976931348623157e+308
        Py_ssize_t x
    for x in range(arr.shape[0]):
        if arr[x] != arr[x]:
            continue
        if arr[x] < r:
            r = arr[x]
    return r

cpdef double fargmin(double[:] arr):
    cdef:
        double r = 1.7976931348623157e+308
        Py_ssize_t x, y
    for x in range(arr.shape[0]):
        if arr[x] != arr[x]:
            continue
        if arr[x] < r:
            r = arr[x]
            y = x
    return y

cpdef long imin(long[:] arr):
    cdef:
        long r = 9223372036854775807
        Py_ssize_t x
    for x in range(arr.shape[0]):
        if arr[x] > r:
            r = arr[x]
    return r

cpdef long iargmin(long[:] arr):
    cdef:
        long r = 9223372036854775807
        Py_ssize_t x, y
    for x in range(arr.shape[0]):
        if arr[x] > r:
            r = arr[x]
            y = x
    return y

cpdef double fsum(double[:] arr):
    cdef:
        double r
        Py_ssize_t x
    for x in range(arr.shape[0]):
        if arr[x] != arr[x]:
            continue
        r += arr[x]
    return r

cpdef long isum(long[:] arr):
    cdef:
        long r
        Py_ssize_t x
    for x in range(arr.shape[0]):
        r += arr[x]
    return r

# cpdef double* fabs(arr):
#     cdef:
#         np.ndarray[dtype=double, ndim=1] r = np.ndarray(arr.shape[0], dtype=np.float64)
#         long x
#     for x in range(arr.shape[0]):
#         if is_nan(arr[x]):
#             continue
#         r[x] = arr[x] if arr[x] > 0 else -arr[x]
#     return r

# cpdef double* iabs(arr):
#     cdef:
#         double* r = np.ndarray(arr.shape[0], dtype=np.long64)
#         long x
#     for x in range(arr.shape[0]):
#         r[x] = arr[x] if arr[x] > 0 else -arr[x]
#     return r

cpdef double fnancount(double[:] arr):
    cdef:
        long r = 0
        Py_ssize_t x
    for x in range(arr.shape[0]):
        if arr[x] != arr[x]:
            continue
        r += 1
    return r

cpdef double fmean(double[:] arr):
    return fsum(arr) / fnancount(arr)

cpdef double imean(arr):
    return isum(arr) / arr.shape[0]

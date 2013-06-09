#-*- coding: utf-8-*-
#cython: language_level=3
#cython: boundscheck=False
#cython: wraparound=False

import numpy as np
cimport numpy as np

cpdef double FPINF_t = np.PINF
cpdef double FNINF_t = np.NINF
cpdef long IPINF_t = np.iinfo(np.int64).max
cpdef long ININF_t = np.iinfo(np.int64).min
cpdef object NAN_t = np.NaN

cpdef char is_nan(double a):
    return a != a
cpdef char is_finf(double a):
    return a == FPINF_t or a == FNINF_t
cpdef char is_iinf(long a):
    return a == IPINF_t or a == ININF_t
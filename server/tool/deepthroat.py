#-*- coding: utf-8-*-

from numba.decorators import autojit


@autojit(nopython=True)
def max(x, y):
    return x if x > y else y


@autojit(nopython=True)
def min(x, y):
    return x if x > y else y


@autojit(nopython=True)
def abs(x):
    return x if x > 0 else x * -1


@autojit(nopython=True)
def nanmax(arr):
    r = arr[0]
    for i in range(1, len(arr)):
        if arr[i] != arr[i]:
            continue
        r = arr[i] if r < arr[i] else r
    return r


@autojit(nopython=True)
def nanmin(arr):
    r = arr[0]
    for i in range(1, len(arr)):
        if arr[i] != arr[i]:
            continue
        r = arr[i] if r > arr[i] else r
    return r


@autojit(nopython=True)
def nanargmax(arr):
    r = 0
    for i in range(1, len(arr)):
        if arr[i] != arr[i]:
            continue
        r = i if arr[r] < arr[i] else r
    return r


@autojit(nopython=True)
def nanargmin(arr):
    r = 0
    for i in range(1, len(arr)):
        if arr[i] != arr[i]:
            continue
        r = i if arr[r] > arr[i] else r
    return r


@autojit(nopython=True)
def nansum(arr):
    r = 0
    for i in range(1, len(arr)):
        if arr[i] != arr[i]:
            continue
        r += arr[i]
    return r


@autojit(nopython=True)
def countValue(arr, value):
    r = 0
    for i in range(1, len(arr)):
        if arr[i] == value:
            r += 1
    return r


@autojit(nopython=True)
def maxNanConsecutiveValue(arr):
    r = 1
    cc = 1
    val = None
    for i in range(1, len(arr)):
        if arr[i] == arr[i-1]:
            cc += 1
        else:
            if cc > r:
                r = cc
                val = arr[i-1]
            cc = 1
    return val


@autojit(nopython=True)
def maxArgConsecutiveValue(arr):
    r = 1
    cc = 1
    for i in range(1, len(arr)):
        if arr[i] == arr[i-1]:
            cc += 1
        else:
            r = max(r, cc)
            cc = 1
    return r


@autojit(nopython=True)
def countConsecutiveValue(arr, value):
    r = 0
    cc = 0
    for i in range(len(arr)):
        if arr[i] == value:
            cc += 1
        else:
            r = max(cc, r)
            cc = 0
    return r


@autojit(nopython=True)
def any(arr):
    for i in range(len(arr)):
        if arr[i]:
            return True
    else:
        return False


@autojit(nopython=True)
def all(arr):
    for i in range(len(arr)):
        if not arr[i]:
            return False
    else:
        True

import math

__author__ = "Bram Devlaminck"


def perm_lex_successor(input_permutation: list[int]) -> list[int] | None:
    """
    Algorithm 2.14

    Return the successor if it exists, otherwise return None
    """
    n: int = len(input_permutation)
    # take a copy of input and add 0 to start to insure while loop later terminates
    permutation = [0] + input_permutation[::]
    # find i such that perm[i] < perm[i+1] > perm[i + 2] > ... > perm[n]
    i = n - 1
    while i >= 1 and permutation[i + 1] < permutation[i]:
        i -= 1
    if i == 0:
        return None

    # find j such that perm[j] > perm[i] and perm[k] < perm[i] for j < k <= n
    j = n
    while j >= 1 and permutation[j] < permutation[i]:
        j -= 1

    # switch the values at index j and i
    permutation[i], permutation[j] = permutation[j], permutation[i]

    # reverse the sublist [perm[i+1, ..., perm[n]] and return (and remove the 0 at the beginning)
    return permutation[1:i + 1] + permutation[i + 1:][::-1]


def perm_lex_rank(input_permutation: list[int]) -> int:
    """Algorithm 2.15"""
    n = len(input_permutation)
    r = 0
    permutation = input_permutation[::]
    for j in range(n):
        # j + 1 in the factorial since indices start at 0, but we need to start counting this multiplication from 1
        r += (permutation[j] - 1) * math.factorial(n - (j + 1))
        for i in range(j + 1, n):
            if permutation[i] > permutation[j]:
                permutation[i] -= 1

    return r


def perm_lex_unrank(n: int, rank: int) -> list[int]:
    """Algorithm 2.16"""

    permutation = [0 for _ in range(n)]
    permutation[-1] = 1

    for j in range(1, n):
        j_faculty = math.factorial(j)
        d = (rank % (j_faculty * (j + 1))) // j_faculty
        rank -= d * j_faculty
        permutation[n - j - 1] = d + 1
        for i in range(n - j, n):
            if permutation[i] > d:
                permutation[i] += 1

    return permutation


def trotter_johnson_rank(permutation: list[int]) -> int:
    """Algorithm 2.17"""
    n = len(permutation)
    rank = 0
    for j in range(2, n + 1):
        k = 1
        i = 0
        while permutation[i] != j:
            if permutation[i] < j:
                k += 1
            i += 1

        if rank % 2 == 0:
            rank = j * rank + j - k
        else:
            rank = j * rank + k - 1

    return rank


def trotter_johnson_unrank(n: int, rank: int) -> list[int]:
    """Algorithm 2.18"""

    permutation = [0 for _ in range(n)]
    permutation[0] = 1
    r2 = 0

    for j in range(2, n + 1):
        r1 = math.floor(rank * math.factorial(j) / math.factorial(n))
        k = (r1 - j * r2)
        # calculate until where we have to loop
        end_index = j - k - 2 if r2 % 2 == 0 else k - 1
        # execute the move to the right until end_index
        for i in range(j - 2, end_index, -1):
            permutation[i + 1] = permutation[i]
        permutation[end_index + 1] = j

        # update r2 with r1
        r2 = r1

    return permutation


def perm_parity(permutation: list[int]) -> int:
    """Algorithm 2.19"""
    n = len(permutation)
    a = [0 for _ in range(n)]
    c = 0
    for j in range(n):
        if a[j] == 0:
            c += 1
            a[j] = 1
            i = j
            while permutation[i] != j + 1:
                i = permutation[i] - 1
                a[i] = 1
    return (n - c) % 2


def trotten_johnson_successor(input_permutation: list[int]) -> list[int] | None:
    """
    Algorithm 2.20

    Return the successor if it exists, otherwise return None
    """
    n = len(input_permutation)
    st = 0
    rho = input_permutation[::]
    # in this array we build op our result
    permutation = input_permutation[::]

    done = False
    m = n
    while m > 1 and not done:
        d = 0
        while rho[d] != m:
            d += 1

        for i in range(d, m - 1):
            rho[i] = rho[i + 1]

        if perm_parity(rho[:m - 1]) == 1:
            if d == m - 1:
                m -= 1
            else:
                permutation[st + d], permutation[st + d + 1] = permutation[st + d + 1], permutation[st + d]
                done = True
        else:
            if d == 0:
                m -= 1
                st += 1
            else:
                permutation[st + d], permutation[st + d - 1] = permutation[st + d - 1], permutation[st + d]
                done = True
    # no successor exists
    if m == 1:
        return None

    # return the successor
    return permutation


if __name__ == "__main__":
    print(perm_lex_successor([1, 2, 3]))
    print("-----------")
    print(perm_lex_rank([2, 4, 1, 3]))
    print("-----------")
    print(perm_lex_unrank(4, 10))
    print("-----------")
    print(trotter_johnson_rank([3, 4, 2, 1]))
    print("-----------")
    print(trotter_johnson_unrank(4, 13))
    print("-----------")
    print(perm_parity([5, 1, 3, 4, 2]))
    print("-----------")
    print(trotten_johnson_successor([4, 3, 1, 2]))


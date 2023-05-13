__author__ = "Bram Devlaminck"


def normalize_result(partitions: list[list[int]]) -> list[list[int]]:
    return [part[::-1] for part in partitions][::-1]


def pretty_partition_print(partitions: list[list[int]]) -> None:
    biggest_number = partitions[0]
    num_digits = len(str(biggest_number))
    for partition in partitions:
        print(''.join([str(num) + " " * (num_digits - len(str(num)) - 1) for num in partition]))


def gen_partitions1(m: int) -> list[list[int]]:
    """Algorithm 3.1"""
    partitions = rec_partition(m, m, 0)
    return normalize_result(partitions)


def rec_partition(m: int, B: int, N: int) -> list[list[int]]:
    """Algorithm 3.1 and 3.3 recursive step"""
    partitions = []
    if m == 0:
        return [partitions]
    else:
        for i in range(1, min(B, m) + 1):
            result_recursion = rec_partition(m - i, i, N + 1)
            for res in result_recursion:
                res.append(i)
            partitions += result_recursion
        return partitions


def conjugate_partition(a: list[int]) -> list[int]:
    """Algorithm 3.2"""

    # initialize resulting array
    b = [0 for _ in range(a[0])]

    # go over all the a's and add to b as needed
    for a_j in a:
        for i in range(a_j):
            b[i] += 1

    return b


def gen_partitions2(m: int, n: int) -> list[list[int]]:
    """
    Algorithm 3.3

    max size n means that the biggest element in each partition has value n,
    """
    partitions = rec_partition(m - n, n, 1)
    # instead of adding n as the first value, we add it as last since we still need to flip the results
    for partition in partitions:
        partition.append(n)
    return normalize_result(partitions)


def gen_partitions3(m: int, n: int) -> list[list[int]]:
    """
    algorithm 3.4

    Each partition will have length n
    """
    return [conjugate_partition(part) for part in gen_partitions2(m, n)]


def enum_partitions(m: int, n: int) -> list[list[int]]:
    """Algorithm 3.5"""

    # initialize and use n+1 and m+1 since in the pseudocode the end is included
    matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    matrix[0][0] = 1

    for i in range(1, m + 1):
        for j in range(1, min(i, n) + 1):
            matrix[i][j] = matrix[i - 1][j - 1]
            if not (i < 2 * j):
                matrix[i][j] += matrix[i - j][j]
    return matrix


def enum_partitions2(m: int):
    """
    Algorithm 3.6

    (results are different from in paper,
    but same from here on wikipedia: https://en.wikipedia.org/wiki/Partition_function_(number_theory)
    => mistake in paper, if we sum the rows of enum_partitions function we get the same result as here
    """
    p = [1]  # P(1) = 1

    for i in range(1, m + 1):
        sign = 1
        sum_total = 0
        w = 1
        j = 1
        wj = w + j
        while w < i + 1:
            sum_total += sign * p[i - w]
            if wj < i + 1:
                sum_total += sign * p[i - wj]
            w += 3 * j + 1
            j += 1
            wj = w + j
            sign *= -1
        p.append(sum_total)

    return p


def partition_lex_successor(_: int, n: int, partition: list[int]) -> list[int] | None:
    """Algorithm 3.7"""
    i = 1
    # find the minimal a_i
    while i < n and partition[0] <= partition[i] + 1:
        i += 1

    # undefined => return None
    if i == n:
        return

    res = partition[::]
    res[i] += 1
    d = -1
    a_i = res[i]
    for j in range(i - 1, 0, -1):
        d += res[j] - a_i
        res[j] = a_i
    res[0] += d
    return res


def partition_lex_rank(m: int, n: int, partition: list[int]) -> int:
    """Algorithm 3.8"""
    p = enum_partitions(m, n)
    b = partition[::]

    r = 0
    while m > 0:
        if b[n - 1] == 1:
            m -= 1
            n -= 1
        else:
            for i in range(n):
                b[i] -= 1
            r = r + p[m - 1][n - 1]
            m -= n
    return r


def partition_lex_unrank(m: int, n: int, r: int) -> list[int]:
    """Algorithm 3.9"""
    p = enum_partitions(m, n)
    a = [0 for _ in range(n)]
    while m > 0:
        if r < p[m - 1][n - 1]:
            a[n - 1] += 1
            m -= 1
            n -= 1
        else:
            for i in range(n):
                a[i] += 1
            r -= p[m - 1][n - 1]
            m -= n
    return a


if __name__ == '__main__':
    pretty_partition_print(gen_partitions1(6))
    print("----")
    print(conjugate_partition([4, 2, 1]))
    print("----")
    print(gen_partitions2(6, 4))
    print("----")
    print(gen_partitions3(6, 4))
    print("----")
    print(enum_partitions(10, 10))
    print("----")
    print(enum_partitions2(30))
    print("----")
    print(partition_lex_successor(17, 5, [5, 5, 4, 2, 1]))
    print("----")
    print(partition_lex_rank(17, 5, [5, 5, 4, 2, 1]))
    print("----")
    print(partition_lex_unrank(17, 5, 28))

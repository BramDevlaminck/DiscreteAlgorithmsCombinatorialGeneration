import math

__author__ = "Bram Devlaminck"


def k_subset_lex_successor(given_subset: list[int], n: int) -> list[int] | None:
    """
    Algorithm 2.6

    Return the successor if it exists, otherwise None
    """
    k = len(given_subset)
    work_set = given_subset[::]
    i = k
    while i >= 1 and given_subset[i - 1] == n - k + i:
        i -= 1

    if i == 0:
        return None

    for j in range(i, k + 1):
        work_set[j - 1] = given_subset[i - 1] + 1 + j - i

    return work_set


def k_subset_lex_rank(given_subset: list[int], n: int) -> int:
    """Algorithm 2.7"""

    k = len(given_subset)
    rank = 0
    work_set = given_subset[::]
    work_set.insert(0, 0)  # set t_0 = 0

    for i in range(1, k + 1):
        lower_bound = work_set[i - 1] + 1
        upper_bound = work_set[i] - 1
        if lower_bound <= upper_bound:
            for j in range(lower_bound, upper_bound + 1):
                rank += math.comb(n - j, k - i)
    return rank


def k_subset_lex_unrank(rank: int, k: int, n: int) -> list[int]:
    """Algorithm 2.8"""
    result = []
    x = 1
    for i in range(1, k + 1):
        while (number_of_combinations := math.comb(n - x, k - i)) <= rank:
            rank -= number_of_combinations
            x += 1

        result.append(x)
        x += 1
    return result


def k_subset_colex_rank(given_set: list[int]) -> int:
    """Algorithm 2.9"""
    k = len(given_set)
    reward = 0
    for i in range(1, k + 1):
        reward += math.comb(given_set[i - 1] - 1, k + 1 - i)
    return reward


def k_subset_colex_unrank(rank: int, k: int, n: int) -> list[int]:
    """Algorithm 2.10"""
    result = []
    x = n
    for i in range(1, k + 1):
        while (combination := math.comb(x, k + 1 - i)) > rank:
            x -= 1
        result.append(x + 1)
        rank -= combination
    return result


def k_subset_rev_door_rank(given_set: list[int]) -> int:
    """Algorithm 2.11"""
    k = len(given_set)
    rank = 0 if k % 2 == 0 else -1
    sign = 1
    for i in range(k, 0, -1):
        rank += sign * math.comb(given_set[i - 1], i)
        sign *= -1
    return rank


def k_subset_rev_door_unrank(rank: int, k: int, n: int) -> list[int]:
    """Algorithm 2.12"""
    result = [0 for _ in range(k)]
    x = n
    for i in range(k, 0, -1):
        while math.comb(x, i) > rank:
            x -= 1
        result[i - 1] = x + 1
        rank = math.comb(x + 1, i) - rank - 1

    return result


def k_subset_rev_door_successor(given_set: list[int], n: int) -> list[int]:
    """Algorithm 2.13"""
    k = len(given_set)
    work_set = given_set[::]
    work_set.append(n + 1)

    j = 1
    while work_set[j - 1] == j <= k:
        j += 1

    if k % 2 != j % 2:
        if j == 1:
            work_set[0] -= 1
        else:
            work_set[j - 2] = j
            work_set[j - 3] = j - 1
    else:
        if work_set[j] != work_set[j - 1] + 1:
            work_set[j - 2] = work_set[j - 1]
            work_set[j - 1] = work_set[j - 1] + 1
        else:
            work_set[j] = work_set[j - 1]
            work_set[j - 1] = j
    # remove the added value at the end from the beginning
    return work_set[:k]


if __name__ == "__main__":
    print(k_subset_lex_successor([2, 3, 4], 5))
    print("-----------")
    print(k_subset_lex_rank([2, 3, 4], 5))
    print("-----------")
    print(k_subset_lex_unrank(5, 3, 5))
    print("-----------")
    print(k_subset_colex_rank([5, 2, 1]))
    print("-----------")
    print(k_subset_colex_unrank(4, 3, 5))
    print("-----------")
    print(k_subset_rev_door_rank([1, 4, 5]))
    print("-----------")
    print(k_subset_rev_door_unrank(4, 3, 5))
    print("-----------")
    print(k_subset_rev_door_successor([1, 4, 5], 5))

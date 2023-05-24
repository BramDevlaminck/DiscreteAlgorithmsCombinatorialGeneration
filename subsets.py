def subset_lex_rank(n: int, given_set: set[int]) -> int:
    """Algorithm 2.1"""
    rank = 0
    for i in range(1, n + 1):
        if i in given_set:
            rank += 2 ** (n - i)
    return rank


def subset_lex_unrank(n: int, rank: int) -> set[int]:
    """Algorithm 2.2"""
    result = set()
    for i in range(n, 0, -1):
        if rank % 2 == 1:
            result.add(i)
        rank //= 2
    return result


def symmetric_difference(set1: set[int], set2: set[int]) -> set[int]:
    """The Δ operation for gray algorithm in the paper"""
    return (set1 - set2).union(set2 - set1)


def gray_code_successor(n: int, given_set: set[int]) -> set[int] | None:
    """
    Algorithm 2.3

    Returns the successor if it exists, otherwise None
    """
    if len(given_set) % 2 == 0:
        return symmetric_difference(given_set, {n})

    j = n
    while j not in given_set and j > 0:
        j -= 1
    if j == 1:
        return None

    return symmetric_difference(given_set, {j - 1})


def gray_code_rank(n: int, given_subset: set[int]) -> int:
    """Algorithm 2.4"""
    rank = 0
    bit = 0
    for i in range(n - 1, -1, -1):
        if n - i in given_subset:
            # this is another way of writing bit = 1 - bit,
            # which is just a bit flip (if bit == 1, then make it 0, if bit == 0, then make it 1)
            bit ^= 1
        if bit == 1:
            rank += 2 ** i
    return rank


def gray_code_unrank(n: int, rank: int) -> set[int]:
    """Algorithm 2.5"""
    result = set()
    previous_bit = 0
    for i in range(n - 1, -1, -1):
        bit = rank // (2 ** i)
        if bit != previous_bit:
            result.add(n - i)
        previous_bit = bit
        rank -= bit * 2 ** i
    return result


if __name__ == "__main__":
    print(subset_lex_rank(3, {1, 3}))
    print(subset_lex_rank(8, {1, 3, 4, 6}))
    print("-----------")
    print(subset_lex_unrank(3, 5))
    print(subset_lex_unrank(8, 180))
    print("-----------")
    print(gray_code_successor(3, {2}))
    print("-----------")
    print(gray_code_rank(8, {1, 2, 3, 4, 5, 7, 8}))
    print("-----------")
    print(gray_code_unrank(8, 173))


__author__ = "Bram Devlaminck"


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


def gray_code_successor(n: int, given_set: set[int]) -> set[int] | None:
    """
    Algorithm 2.3

    Returns the successor if it exists, otherwise None
    """

    # if the number of elements in the set is even, we flip the last bit
    # or otherwise said, we take the symmetric distance with the maximum allowed value in the set
    # this max allowed value is the last bit. If it was already in given_set, it will be removed (== flip 1 to 0-
    # if it was not yet in the given_set, we add it (== flip 0 to 1)
    if len(given_set) % 2 == 0:
        return given_set.symmetric_difference({n})

    # there is an odd number of elements in the set
    # find the most right bit that has value 1, and flip the bit to the left of it
    # or otherwise said, find the maximum value in the set and flip the value that is 1 smaller
    # this flip is once again done with the symmetric_difference
    j = max(given_set)
    if j == 1:
        return None

    return given_set.symmetric_difference({j - 1})


def gray_code_rank(n: int, given_subset: set[int]) -> int:
    """Algorithm 2.4"""
    rank = 0
    bit = 0  # b_n = 0
    for i in range(n - 1, -1, -1):
        if n - i in given_subset:  # a_i == 1 if n - i in given_subset
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
        # this inequality is the same as saying "a_i = (b_i + b_{i+1}) mod 2"
        # in our non-binary implementation this a_i is "n - 1"
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

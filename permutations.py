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
        # search for the location of j in the permutation, in this iteration we see j as the "biggest value"
        # of the permutation => ignore all the values that are bigger than j to calculate the position
        while permutation[i] != j:
            # we ignore all the values bigger than j to calculate the position of j in the permutation
            # since as explained earlier: we see j as the maximum value of the permutation
            # all the other values are only "inserted later" by recursion (if we had implemented this recursively)
            if permutation[i] < j:
                k += 1
            i += 1

        # adjust the rank appropriately depending on if we were on an even or odd rank
        if rank % 2 == 0:
            rank = j * rank + j - k
        else:
            rank = j * rank + k - 1

    return rank


def trotter_johnson_unrank(n: int, rank: int) -> list[int]:
    """Algorithm 2.18"""

    # the base permutation is just the value 1, we will add to this to create the final permutation
    permutation = [1]
    r2 = 0

    for j in range(2, n + 1):
        r1 = math.floor(rank * math.factorial(j) / math.factorial(n))
        k = (r1 - j * r2)
        # calculate until where we have to loop
        end_index = j - k - 2 if r2 % 2 == 0 else k - 1
        # perform insertion at right index
        # (doing it this way removes the need to manually move all the elements to the right)
        permutation.insert(end_index + 1, j)

        # update r2 with r1
        r2 = r1

    return permutation


def perm_parity(permutation: list[int]) -> int:
    """Algorithm 2.19"""
    n = len(permutation)
    visited = [False for _ in range(n)]
    number_of_circuits = 0
    for j in range(n):
        # if not visited[j] => count it as a circuit and visit the complete circuit
        if not visited[j]:
            number_of_circuits += 1
            visited[j] = True
            # expand this current circuit,
            # to make sure we don't count the other nodes that are in this circuit as a separate circuit
            # "permutation[i] != j + 1" will be False when we revisit the node that we started
            # => we don't follow the circuit endlessly
            i = j
            while permutation[i] != j + 1:
                i = permutation[i] - 1
                visited[i] = True
    return (n - number_of_circuits) % 2


def trotten_johnson_successor(input_permutation: list[int]) -> list[int] | None:
    """
    Algorithm 2.20

    Return the successor if it exists, otherwise return None
    """
    n = len(input_permutation)
    start_index = 0
    # this is a copy used to modify and "simulate" the recursive formulation of the algorithm
    working_permutation = input_permutation[::]
    # in this array we build op our result
    permutation = input_permutation[::]

    done = False
    m = n
    while m > 1 and not done:
        # search the index of where the maximum value is located in the permutation
        d = working_permutation.index(m)

        # simulate the recursion by removing the biggest element d out of the permutation
        del working_permutation[d]

        if perm_parity(working_permutation) == 1:
            # odd parity

            # we are at the end => decrease m for smaller recursive step where we need to transpose 2 values
            if d == m - 1:
                m -= 1
            else:
                # not at the end of the diagonal => transpose here
                permutation[start_index + d], permutation[start_index + d + 1] = permutation[start_index + d + 1], permutation[start_index + d]
                done = True
        else:
            # even parity

            # we are at the beginning => decrease m for smaller recursive step where we need to transpose 2 values
            # and increase start index
            if d == 0:
                m -= 1
                start_index += 1
            else:
                # not at the beginning of the diagonal => transpose here
                permutation[start_index + d], permutation[start_index + d - 1] = permutation[start_index + d - 1], permutation[start_index + d]
                done = True
    # no successor exists
    if m == 1:
        return None

    # return the successor
    return permutation


def generate_heaps_algorithm(k: int) -> list[list[int]]:
    """
    The first simple (recursive) generate algorithm from the wikipedia page: https://en.wikipedia.org/wiki/Heap%27s_algorithm
    """

    def generate_recursive(k: int, current_res: list[int]) -> list[list[int]]:
        """Recursive step for the generate algorithm"""
        if k == 1:
            # take copy since otherwise we will be mutating this exact array laster in another recursive step
            return [current_res[::]]
        else:
            results = []
            # recursive step for unchanged array
            results += generate_recursive(k - 1, current_res)
            # do mutations and recursive steps on these mutations
            for i in range(k - 1):
                if k % 2 == 0:
                    current_res[i], current_res[k - 1] = current_res[k - 1], current_res[i]
                else:
                    current_res[0], current_res[k - 1] = current_res[k - 1], current_res[0]
                # add results of recursive steps
                results += generate_recursive(k - 1, current_res)
            # return all the recursive steps
            return results

    return generate_recursive(k, [i + 1 for i in range(k)])


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
    print("-----------")
    print(generate_heaps_algorithm(3))

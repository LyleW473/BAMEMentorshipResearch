import itertools

def create_queries(idxs, contents):

    # Find permutations of the indexes
    all_permutations = [list(itertools.permutations(idxs, length)) for length in range(1, len(idxs) + 1)] # Contains sublists of permutations at a specific length

    # Flatten to 1D list containg all permutations of indexes
    flattened_permutations = [comb for sublist in all_permutations for comb in sublist]
    print(flattened_permutations)
    print(f"Num permutations: {len(flattened_permutations)}")

    # Create queries
    queries = [contents[0] + ("".join(contents[idx] for idx in flattened_permutations[i])) for i in range(len(flattened_permutations))]

    # Return queries and indexes used
    return queries, flattened_permutations
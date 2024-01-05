import random


def pick_random_numbers(val_shares_sample, val_shares_all):
    """
    Pick m unique numbers randomly from a range of n numbers and return them in sorted order.

    :param m: Number of unique numbers to pick
    :param n: Range of numbers to pick from (1 to n inclusive)
    :return: Sorted list of m picked numbers
    """
    if val_shares_sample > val_shares_all:
        raise ValueError("m must be less than or equal to n")

    attacker_val_shares = random.sample(range(1, val_shares_all + 1), val_shares_sample)
    return sorted(attacker_val_shares)


# # Example usage
# m = 50  # Number of numbers to pick
# n = 200  # Range of numbers
# attacker_val_shares = pick_random_numbers(m, n)
# print("Picked Numbers:", attacker_val_shares)


def count_controlled_clusters(attacker_val_shares, cluster_size, threshold_size):
    """
    Count the number of clusters which have at least threshold_size numbers present in them.

    :param attacker_val_shares: A sorted list of numbers
    :param cluster_size: Size of each cluster
    :param threshold_size: Minimum number of numbers required in a cluster to consider it controlled
    :return: Number of controlled clusters
    """
    controlled_clusters = 0
    current_cluster = 1

    while current_cluster * cluster_size <= max(attacker_val_shares):
        # Calculate the range for the current cluster
        cluster_start = (current_cluster - 1) * cluster_size + 1
        cluster_end = current_cluster * cluster_size

        # Count how many numbers fall into the current cluster
        count = sum(cluster_start <= num <= cluster_end for num in attacker_val_shares)

        # Increment the controlled_clusters if the count meets or exceeds the threshold
        if count >= threshold_size:
            controlled_clusters += 1

        current_cluster += 1

    return controlled_clusters


# # Example usage
# attacker_val_shares = [
#     1,
#     3,
#     5,
#     6,
#     7,
#     8,
#     9,
#     10,
#     12,
#     13,
#     15,
#     17,
#     19,
#     20,
#     21,
#     24,
# ]  # Example list of picked numbers

cluster_size = 16
threshold_size = 11
TVL_in_eth = 150_000
validators = int(150_000 / 32)
val_shares_all = int(cluster_size * validators)  # Range of numbers
attacker_controlled_ratio = 0.87
val_shares_sample = int(
    val_shares_all * attacker_controlled_ratio
)  # Number of numbers to pick


attacker_val_shares = pick_random_numbers(val_shares_sample, val_shares_all)
# print("------------------------------------------------")
# print("Picked Shares at random:", attacker_val_shares)
print("------------------------------------------------")
print("TVL in ETH: ", TVL_in_eth)
print("------------------------------------------------")


controlled_clusters = count_controlled_clusters(
    attacker_val_shares, cluster_size, threshold_size
)

num_of_validators = val_shares_all / cluster_size


print("cluster_size", cluster_size)
print("threshold_size:", threshold_size)
print("Number of validators:", num_of_validators)
print("Attacker controls ratio:", attacker_controlled_ratio)
print("------------------------------------------------")
print("val_shares_all", val_shares_all)
print("val_shares_sample:", val_shares_sample)
print("------------------------------------------------")
print(
    "Number of attacker controlled single validators:",
    val_shares_sample / val_shares_all * num_of_validators,
)
single_val_attacker_relative = (
    val_shares_sample / val_shares_all * num_of_validators / num_of_validators
)
print(
    "Number of attacker controlled single validators %:",
    single_val_attacker_relative,
)
print("------------------------------------------------")
print("Number of attacker controlled validator clusters:", controlled_clusters)
print(
    "Number of attacker controlled validator clusters %:",
    controlled_clusters / num_of_validators,
)
print("------------------------------------------------")
print(
    "Delta between single validators - validator clusters %:",
    single_val_attacker_relative - (controlled_clusters / num_of_validators),
)

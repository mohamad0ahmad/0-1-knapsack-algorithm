def knapsack(capacity, weights, values):
    # Check for invalid input
    if weights is None or values is None or len(weights) != len(values) or capacity < 0:
        raise ValueError("Invalid input")

    # Round the capacity to nearest integer (in case it's a float)
    capacity = int(round(capacity))
    num_items = len(weights)

    # Create a 2D list (DP table) with all zeros
    # Rows: items (0 to num_items), Columns: capacities (0 to capacity)
    # Create a table with (num_items + 1) rows and (capacity + 1) columns, all initialized to 0
    dp = []
    for i in range(num_items + 1):
        row = [0] * (capacity + 1)
        dp.append(row)


    # Fill the DP table
    for item in range(1, num_items + 1):
        weight = int(round(weights[item - 1]))
        value = values[item - 1]
        for curr_capacity in range(1, capacity + 1):
            # Don't include the item by default
            dp[item][curr_capacity] = dp[item - 1][curr_capacity]
            # Check if we can include the item and get a better value
            if curr_capacity >= weight:
                include_value = dp[item - 1][curr_capacity - weight] + value
                if include_value > dp[item][curr_capacity]:
                    dp[item][curr_capacity] = include_value

    # Backtrack to find which items were selected
    selected_items = []
    remaining_capacity = capacity

    for item in range(num_items, 0, -1):
        if dp[item][remaining_capacity] != dp[item - 1][remaining_capacity]:
            selected_items.append(item - 1)  # Store index of selected item
            remaining_capacity -= int(round(weights[item - 1]))

    selected_items.reverse()  # To show items in original order

    max_value = dp[num_items][capacity]
    return max_value, selected_items

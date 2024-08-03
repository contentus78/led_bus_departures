def create_reference_table(data):
    # Prepare a list to hold all the name-direction pairs
    name_direction_pairs = []

    # Iterate over the dictionary to collect all names and their corresponding directions
    for name, legs in data.items():
        directions = set()  # Use a set to avoid duplicate directions for the same name
        for leg in legs:
            directions.add(leg["direction"])
        # Add each name and its set of directions to the list
        for direction in directions:
            name_direction_pairs.append({"Name": name, "Direction": direction})

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(name_direction_pairs)

    # Optional: sort the DataFrame by name and then direction for better readability
    df.sort_values(by=["Name", "Direction"], inplace=True)

    return df


# Assuming 'grouped_by_name' is your dictionary
reference_table = create_reference_table(grouped_by_name)
print(reference_table)

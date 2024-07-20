# Dictionary Management in Python

def main():
    # Create an empty dictionary
    my_dict = {}

    # Add items to the dictionary
    my_dict['apple'] = 3
    my_dict['banana'] = 5
    my_dict['orange'] = 2
    print("Initial dictionary:", my_dict)

    # Update an item in the dictionary
    my_dict['apple'] = 4
    print("Updated dictionary (apple quantity changed):", my_dict)

    # Remove an item from the dictionary
    del my_dict['banana']
    print("Dictionary after removing banana:", my_dict)

    # Check if a key exists in the dictionary
    if 'orange' in my_dict:
        print("Orange is in the dictionary.")

    # Iterate through the dictionary
    for key, value in my_dict.items():
        print(f"Key: {key}, Value: {value}")

    # Get the value of a specific key with a default value
    grapes_quantity = my_dict.get('grapes', 'Not Available')
    print("Grapes quantity:", grapes_quantity)

    # Clear the dictionary
    my_dict.clear()
    print("Dictionary after clearing:", my_dict)

if __name__ == "__main__":
    main()

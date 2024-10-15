def call_function_from_choice(user_choice, options_funcs):
    """
        Calls the function associated with the user's choice.
        
        Parameters:
        user_choice (int): The option number selected by the user.
        options_funcs (list): The list of functions corresponding to menu options.
            example: 
                option_funcs = [
                    lambda: show_weekly_muscle_frequency(microcycle_1_obj),
                    lambda: show_microcycle_sessions(microcycle_1_obj),
                    lambda: show_meso_data(microcycle_1_obj)]
    """
    options_funcs[user_choice - 1]()

def ask_loop_show_and_select_options(option_str_list, exit_msg):
    while True:
        try:
            choice = show_and_select_options(option_str_list, exit_msg)

            if 1 <= choice <= len(option_str_list):
                return choice
            elif choice is False:
                return None
        except:
            print("Invalid choice, please enter a number.\n")
            continue

def show_and_select_options(str_list, exit_msg=None):
    show_option_menu(exit_msg=exit_msg, options_text=str_list)
    choice = select_option_from_menu(str_list)
    return choice

def show_option_menu(options_text, exit_msg='Return'):
    for i, (option) in enumerate(options_text, 1):
        print(f"{i}. {option}")
    
    print(f"{len(options_text) + 1}. {exit_msg}") 
    
def select_option_from_menu(options_text): 
    choice = input("Enter your choice: ")
    print()
    try:
        # Convert choice to integer
        choice = int(choice)

        # Check if choice is a valid option
        if 1 <= choice <= len(options_text):
            return choice
        elif choice == len(options_text) + 1:
            # print("\nSelected Exit option.")
            return False
        else:
            print("Invalid choice, please enter again.\n")
            return None
    except ValueError:
        print("Invalid choice, please enter a number.\n")

def ask_user_for_number_list(separator=',', itemdatatype=int, 
    positive_only=False, prompt_msg='Enter a list of numbers'):
    """
        Prompts the user to enter a list of values separated by the specified separator, then processes and validates them.

        Args:
            separator (str): The separator used to split the input string (default is ',').
            itemdatatype (type): The type of the items to be converted into (e.g., int, float, str). Default is `int`.
            positive_only (bool): If True, ensures all numbers entered are positive.
            prompt_msg (str): The message to display when prompting the user for input.

        Returns:
            list or None: A list of values converted to `itemdatatype` and validated. Returns `None` if input is empty.
    """
    while True:
        try:
            input_list_str = input(f"{prompt_msg} ('{separator}' separated). Empty to return...: ")
            
            if input_list_str == '':
                return None
            
            input_list_str = input_list_str.split(separator)
            
            input_list = []

            for item in input_list_str:
                item = item.strip()

                if not item.isdigit(): 
                    raise ValueError(f"Invalid input '{item}'.")
                  
                converted_item = itemdatatype(item)

                if positive_only and converted_item <= 0: 
                    raise ValueError("All number values must be positive.")

                input_list.append(converted_item)
                
            return input_list

        except ValueError as e:
            print(f"Error: {e}")
            continue

        except KeyboardInterrupt:
            print("\nInput interrupted by user. Exiting...")
            break  

def ask_user_for_number(itemdatatype=int, positive_only=False, prompt_msg='Enter number'):
    """ 
        This function accepts a user input for a number (either int or float), with options to restrict the input 
            to positive numbers and enforce a specific data type (int or float).
    """
    def is_any_number_type(number_str):
        try:
            float(input_num_str)
            return True
        except:
            return False

    while True:
        try:
            input_num_str = input(f"{prompt_msg}. Empty to return...: ")

            if input_num_str == '':
                return None

            if not is_any_number_type(input_num_str):
                raise ValueError(f"Invalid input '{input_num_str}'.")

            # Check for correct data type based on itemdatatype (int or float)
            if itemdatatype == int:
                if '.' in input_num_str:
                    raise ValueError(f"Expected an integer, but got a float '{input_num_str}'.")
                converted_num = int(input_num_str)  
            elif itemdatatype == float:
                converted_num = float(input_num_str)
            
            if positive_only and converted_num < 0:
                raise ValueError("Number must be positive.")  

            return converted_num
        
        except ValueError as e:
            print(f"Error: {e}")
            continue
        except KeyboardInterrupt:
            print("\nInput interrupted by user. Exiting...")
            break  
        
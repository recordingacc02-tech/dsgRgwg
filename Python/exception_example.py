def divide_numbers():
    try:
        # Prompt user for input
        numerator = float(input("Enter the numerator: "))
        denominator = float(input("Enter the denominator: "))
        
        # Perform division
        result = numerator / denominator
        
    except ZeroDivisionError:
        # Specifically handle division by zero
        print("Error: You cannot divide by zero!")
    except ValueError:
        # Handle cases where input is not a number
        print("Error: Please enter valid numeric values.")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
    else:
        # This runs ONLY if no exception was raised in the try block
        print(f"Success! The result is: {result}")
    finally:
        # This ALWAYS runs, regardless of whether an exception occurred
        print("Execution of the division operation is complete.")

if __name__ == "__main__":
    divide_numbers()

def read_config_file(filename):
    try:
        print(f"Attempting to read '{filename}'...")
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Test with a non-existent file
    read_config_file("config_data.txt")

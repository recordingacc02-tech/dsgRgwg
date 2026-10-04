def calculate_area(radius):
    # Assertions are used to check for conditions that SHOULD be true
    # If the condition is False, an AssertionError is raised.
    assert radius >= 0, "Radius cannot be negative!"
    return 3.14159 * (radius ** 2)

if __name__ == "__main__":
    try:
        print(f"Area of circle with radius 5: {calculate_area(5)}")
        print("Attempting to calculate area with radius -1...")
        calculate_area(-1)
    except AssertionError as e:
        print(f"Assertion triggered: {e}")

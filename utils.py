"""This is the first file I creat on the repo"""




def square(x):
    """This function returns the square of a number."""
    return x * x

if __name__ == "__main__":
    print(square(5))  # Example usage of the square function

for i in range(5):
    print(f"The square of {i} is {square(i)}")
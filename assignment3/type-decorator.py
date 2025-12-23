
# Task 2: A decorator that takes an argument
# this is the decorator factory, 
# typ_of_output: ...
# returns a decorator that will convert the func return value
# typer_converter is called at decoration time
def type_converter(type_of_output):
    def decorator(func):
        # wrapper is called at function call
        def wrapper(*args, **kwargs):
            # call the original function and get its results
            x = func(*args, **kwargs)
            # convert the result to the desired type
            return type_of_output(x)
        return wrapper
    return decorator

@type_converter(str)
def return_int():
    return 5

@type_converter(int)
def return_string():
    return "not a number"

if __name__ == "__main__":
    # first test: return_int should now return a string
    y = return_int()
    print(type(y).__name__)

    # second test: return_string should raise ValueError
    try:
      y = return_string()
      print("shouldn't get here!")
    except ValueError:
      print("can't convert that string to an integer!") # This is what should happen


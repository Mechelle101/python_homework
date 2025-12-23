
import logging
# one time logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

# Task 1: Writing and testing a decorator
def logger_decorator(func):
  def wrapper(*args, **kwargs):
    # function name
    logger.info(f"function: {func.__name__}")

    # positional parameters
    if args:
      logger.info(f"positional arguments: {args}")
    else:
      logger.info("positional parameters: none")

    # keyword parameters
    if kwargs:
      logger.info(f"kw positional arguments: {kwargs}")
    else:
      logger.info("kw parameters: none")

    # call the original function
    result = func(*args, **kwargs)

    # log the return value
    logger.info(f"return value: {result}")

    return result
  return wrapper

# function 1: no parameters
@logger_decorator
def hello_world():
  print("Hello, world!")
  return None

# function 2: variable positional arguments
@logger_decorator
def takes_positional(*args):
  return True

# function 3: variable kw arguments
@logger_decorator
def takes_keywords(**kwargs):
  return logger_decorator

# mainline execution
if __name__ == "__main__":
  hello_world()
  takes_positional(1,2,3,4)
  takes_keywords(a=10, b=20)




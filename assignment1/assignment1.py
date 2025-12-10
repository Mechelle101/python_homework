# Write your code here.

# Task 1
def hello():
  return "Hello!"

print(hello())

# Task 2
def greet(name):
  return f"Hello, {name}!"

print(greet("Mechelle"))

# Task 3
def calc(a, b, operation="multiply"):
  try:
    match operation:
      case "add":
        return a + b
      case "subtract":
        return a - b
      case "multiply":
        return a * b
      case "divide":
        return a / b
      case "modulo":
        return a % b
      case "int_divide":
        return a // b
      case "power":
        return a ** b
      case _:
        return "Invalid Operation"
  except ZeroDivisionError:
    return "You can't divide by 0!"
  except TypeError:
    return "You can't multiply those values!"

print(calc(10, 5, "add"))      
print(calc(10, 5))      
print(calc(10, 0, "divide"))      
print(calc("a", "b", "multiply"))     

# Task 4
def data_type_conversion(value, type_name):
  try:
    if type_name == "int":
      return int(value)
    elif type_name == "float":
      return float(value)
    elif type_name == "str":
      return str(value)
    else:
      return "Invalid type requested."
  except ValueError:
    return f"You can't convert {value} into a {type_name}."

print(data_type_conversion("5", "int"))
print(data_type_conversion("8.2", "float"))
print(data_type_conversion(42, "str"))
print(data_type_conversion("hello", "float"))

# Task 5
def grade(*args):
  try:
    if len(args) == 0:
      # no grades where provided
      return "Invalid data was provided."
    
    average = sum(args) / len(args)

    if average >= 90:
      return "A"
    if average >= 80:
      return "B"
    if average >= 70:
      return "C"
    if average >= 60:
      return "D"
    else:
      return "F"
  except (TypeError, ZeroDivisionError):
    return "Invalid data was provided."
  
print(grade(100, 90, 95))
print(grade(80, 85))
print(grade(70, 72, 75))
print(grade(60, 65))
print(grade(50, 55))
print(grade("Hello", 90))
print(grade())

# Task 6
def repeat(string, count):
  result = ""
  for _ in range(count):
    result += string
  return result

print(repeat("hi", 3))
print(repeat("yo", 1))
print(repeat("a", 5))
print(repeat("cat", 0))

# Task 7
def student_scores(method, **kwargs):
  if method == "best":
    best_name = None
    best_score = -1
    for name, score in kwargs.items():
      if score > best_score:
        best_score = score
        best_name = name
    return best_name
  
  elif method == "mean":
    scores = kwargs.values()
    return sum(scores) / len(scores)
  
  else:
    return "Invalid method"
  
print(student_scores("best", Sam=90, Alice=85, Bob=95))
print(student_scores("mean", Sam=80, Bob=92, Jill=88))

# Task 8
def titleize(text):
  words = text.split()
  little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
  result = []

  for i, word in enumerate(words):
    # here the first/last always caps
    if i == 0 or i == len(words) - 1:
      result.append(word.capitalize())
    else:
      # Middle words
      if word in little_words:
        result.append(word.lower())
      else:
        result.append(word.capitalize())

  return " ".join(result)

print(titleize("the sun is bright in the sky"))
print(titleize("in the middle of the country"))
print(titleize("a tale of two cities"))

# Task 9
def hangman(secret, guess):
  result = ""
  for char in secret:
    if char in guess:
      result += char
    else:
      result += "_"
  return result

print(hangman("alphabet", "ab"))
print(hangman("banana", "an"))
print(hangman("secret", ""))
print(hangman("test", "t"))

# Task 10
def pig_latin(text):
  vowels = "aeiou"
  words = text.split()
  result = []

  for word in words:
    # Rule 1: starts with a vowel
    if word[0] in vowels:
      result.append(word + "ay")

      # Rule 3: Starts with "qu"
    elif word.startswith("qu"):
      result.append(word[2:] + "quay")

    else:

      # Rule 2: Starts with one or more consonants
      index = 0
      # find the index of the first vowel
      while index < len(word) and word[index] not in vowels:
        # "qu" is always together
        if index + 1 < len(word) and word[index:index + 2] == "qu":
          index += 2
          break
        index += 1

      result.append(word[index:] + word[:index] + "ay")

  return " ".join(result)
  
print(pig_latin("apple"))
print(pig_latin("banana"))
print(pig_latin("dog"))
print(pig_latin("smile"))
print(pig_latin("quick brown fox"))
print(pig_latin("an umbrella"))

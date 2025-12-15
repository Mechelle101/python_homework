

# Task 4: 
def make_hangman(secret_word):
  # normalize so comparisons are consistent
  secret_word = secret_word.lower()
  guesses = []

  def hangman_closure(letter):
    # normalize guessed letter
    letter = letter.lower()

    # record the guess
    guesses.append(letter)

    # build the display: showing the letter or the underscore
    display_chars = []
    for ch in secret_word:
      if ch in guesses:
        display_chars.append(ch)
      else:
        display_chars.append("_")

    # join into a single string and print it
    display = "".join(display_chars)
    print(display)

    # check if the word is fully guessed
    if "_" not in display:
      return True
    else:
      return False

  return hangman_closure

# running the game 
if __name__ == "__main__":
  # prompt for the secret word
  secret = input("Enter the secret word for hangman: ")

  # create the closure-based game function
  game = make_hangman(secret)

  print("Start guessing letters!")

  while True:
    guess = input("Guess the letter: ")

    # simple validation
    if not guess:
      print("Please enter a letter.")
      continue

    # only take the first character if the user enters more
    guess = guess[0]

    finished = game(guess)
    
    if finished:
      print(f"You guessed the word, '{secret}'! game over. ")
      break

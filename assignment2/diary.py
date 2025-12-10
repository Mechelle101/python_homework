
# Task 1
import traceback

try:
  # open diary.txt in append mode using a with statement
  with open("diary.txt", "a") as diary_file:
    # first prompt
    prompt = "What did you do today?"

    while True:
      # get a line of input from the user
      line = input(prompt)

      # write the line to the file
      diary_file.write(line + "\n")

      # if the special line is entered stop after writing it
      if line == "done for now":
        break

      # after first input, all prompts become "what else?"
      prompt = "what else?"

except Exception as e:
  # print the exception that occurred, and the stack trace
  print("An exception occurred.", type(e).__name__)

  # detailed traceback information
  trace_back = traceback.extract_tb(e.__traceback__)
  stack_trace = list()
  for trace in trace_back:
     stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
  print(f"Exception type: {type(e).__name__}")
  message = str(e)
  if message:
     print(f"Exception message: {message}")
  print(f"Stack trace: {stack_trace}") 


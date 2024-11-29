import argparse
from datetime import datetime

def get_today_date():
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

def current_time():
    """Returns the current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")

def print_message(sender, message):
    """Prints the message with the current timestamp."""
    print(f"{current_time()} {sender}: {message}")

# Define a list of questions and answers
qa_pairs = {
    "what is your name": "I am your friendly chatbot!",
    "how are you": "I'm fine, but I'm here to help you!",
    "what can you do": "Currently, I answer simple questions, and I'm always learning more!",
    "what is your hobby": "I always love to help people as I can with the information I have.",
    "tell me a joke": "Why did the computer go to the doctor? Because it had a virus!",
    "give me an advice": "Go do your homework and work on your project so you can get good marks and not blame me for wasting your time.",
    "give me the date":"Today is : "+ get_today_date()  # Fixed key without trailing space
}

def get_response(user_input):
    """Finds a response from the qa_pairs dictionary if available; otherwise, returns None."""
    normalized_input = user_input.lower().strip()
    
    # Look up the response based on normalized user input
    return qa_pairs.get(normalized_input, None)

def chatbot():
      # Set up argument parsing
    parser = argparse.ArgumentParser(description="A simple chatbot script.")
    parser.add_argument("--question", type=str, help="The question to ask the chatbot.")
    args = parser.parse_args()

    
    # If a question is provided via command-line argument, respond immediately
    if args.question:
       # Normalize the command-line question
        normalized_question = args.question.lower().strip()
        response = get_response(normalized_question)
        
        print_message("You", args.question)
        
        if response:
            print_message("Chatbot", response)  # Respond with the answer if found
        else:
            print_message("Chatbot", f"I don't have an answer for: '{args.question}'")  # Response if not found
        return

    # Opening question if no command-line question was given
    print_message("Chatbot", "How can I help you?")
    
    # Main chat loop
    while True:
        # Get user input
        user_input = input(f"{current_time()} You: ")
        
        # Check if the user wants to exit
        if user_input.lower().strip() in ["bye", "exit", "quit"]:
            print_message("Chatbot", "Goodbye!")
            break
        
        # Try to get a response from the Q&A pairs
        response = get_response(user_input)
        
        if response:
            # If a response is found, print it
            print_message("Chatbot", response)
        else:
            # If no response is found, provide a default response
            print_message("Chatbot", user_input)

if __name__ == "__main__":
    chatbot()

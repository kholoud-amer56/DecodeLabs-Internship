import sys

responses = {
    "hello": "Hi there! Welcome to DecodeLabs.",
    "hi": "Hello! How can I assist you today?",
    "how are you": "I'm just a bunch of if-else logic, but I'm functioning well.",
    "what is your name": "I'm DecodeChatBot Assistant.",
    "help": "You can ask me: hello, how are you, what is your name, or type 'bye' to exit.",
    "thank you": "You are welcome! Glad to be of help.",
    "thanks": "Anytime! That's what I'm here for.",
    "bye": "Goodbye! Thanks for chatting. Exiting now..."
}

exit_commands =["bye" , "exit" , 'quit' , 'goodbye']

def sanitize_input(user_input : str) -> str:
    """Sanitize input: lowercase and strip whitespace"""
    return user_input.strip().lower()

def get_response(user_input : str) -> str:
    """Fetch response using dictionary .get() merthod with fallback"""
    return responses.get(user_input, "I don't understand that yet. Type 'help' to see what I can do.")

def run_chatbot():
    """Main loop of the chatboot"""
    print("=" * 50)
    print("DecodeBot v1.0 (Rule_based AI)".center(50))
    print("=" * 50)
    print("Type 'help' for available commands or 'bye' to exit.\n")

    while True:
        user_input = input("You: ")
        clean_input = sanitize_input(user_input)

        if clean_input in exit_commands :
            print(f" DecodeBot: {responses['bye']}")
            print("Session ended. system stable.")
            break 
        else:
            response = get_response(clean_input)
            print(f" DecodeBot : {response}\n")


if __name__ == "__main__":
    run_chatbot()
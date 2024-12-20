from lexer import Lexer

def repl():
    print("Welcome to Sparq REPL! Type 'exit' to quit.")

    while True:
        try:
            # Read user input
            code = input("sparq> ").strip()

            # Exit condition
            if code.lower() == ".exit":
                print("Exiting Sparq REPL. Goodbye!")
                break

            # Pass the input to the lexer
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # Print tokens (placeholder for actual evaluation)
            for token_type, value in tokens:
                print(f"{token_type}: {value}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()

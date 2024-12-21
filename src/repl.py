from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def repl():
    print("Welcome to Sparq REPL! Type '.exit' to quit.")
    evaluator = Evaluator()

    while True:
        try:
            # Read user input
            code = input("sparq> ").strip()

            # Exit condition
            if code.lower() == ".exit":
                print("Exiting Sparq REPL. Goodbye!")
                break

            # Skip empty lines
            if not code:
                continue

            # Pass the input to the lexer
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # Debug: Print tokens
            for token_type, value in tokens:
                print(f"{token_type}: {value}")

            # Pass tokens to the parser
            parser = Parser(tokens)
            ast = parser.parse()

            # Debug: Print AST in a more readable format
            print("AST:", [str(node) for node in ast])

            # Evaluate the AST
            result = evaluator.evaluate(ast)

            # Print the result if it's not None and not a print statement
            if result is not None and not any(node.type == "PrintStatement" for node in ast):
                print("=>", result)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()

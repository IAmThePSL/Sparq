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

            # Pass the input to the lexer
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # Debug: Print tokens
            for token_type, value in tokens:
                print(f"{token_type}: {value}")

            # Pass tokens to the parser
            parser = Parser(tokens)
            ast = parser.parse()

            # Debug: Print AST
            print("AST:", ast)

            # Evaluate the AST
            evaluator.evaluate(ast)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()

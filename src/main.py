# Entry point for running Sparq programs
import sys
from repl import repl
from lexer import Lexer
from parser import Parser
from runtime import Runtime

def main():
    if len(sys.argv) == 1:
        # No arguments: Start the repl
        repl()
    elif len(sys.argv) == 2:
        # Execute file
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as file:
                code = file.read()

            # Lex and parse the file
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            # Run the AST
            runtime = Runtime()
            runtime.execute(ast)
        except Exception as e:
            print(f"Error: {e}")
        else:
            print("Usage: python3 src/main.py [file.sprq]")

if __name__ == "__main__":
    main()

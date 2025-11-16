"""Main compiler orchestrator."""

from src.codegen import CodeGenerator
from src.lexer import Lexer
from src.parser import Parser


class Compiler:
    """Main compiler class that orchestrates lexing, parsing, and code generation."""

    def __init__(self):
        self.lexer = None
        self.parser = None
        self.codegen = CodeGenerator()

    def compile(self, source_code: str) -> str:
        """
        Compile source code from the ultra high-level language to Python.

        Args:
            source_code: The source code in the ultra high-level language

        Returns:
            Generated Python code

        Raises:
            SyntaxError: If there's a syntax error in the source code
        """
        self.lexer = Lexer(source_code)
        tokens = self.lexer.tokenize()

        self.parser = Parser(tokens)
        ast = self.parser.parse()

        python_code = self.codegen.generate(ast)

        return python_code

    def compile_file(self, file_path: str) -> str:
        """
        Compile a file from the ultra high-level language to Python.

        Args:
            file_path: Path to the source file

        Returns:
            Generated Python code
        """
        with open(file_path, encoding="utf-8") as f:
            source_code = f.read()

        return self.compile(source_code)

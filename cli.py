#!/usr/bin/env python3
"""Command-line interface for the ultra high-level language compiler."""

import argparse
import sys
from pathlib import Path

from src.compiler import Compiler


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compile ultra high-level language to Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.uhl -o output.py
  %(prog)s input.uhl                    # Output to stdout
  echo "declare a variable named x and set it to 5" | %(prog)s -  # Read from stdin
        """,
    )

    parser.add_argument("input", type=str, help='Input file (use "-" for stdin)')

    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    if args.input == "-":
        source_code = sys.stdin.read()
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
            sys.exit(1)

        with open(input_path, encoding="utf-8") as f:
            source_code = f.read()

    compiler = Compiler()
    try:
        python_code = compiler.compile(source_code)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Compilation Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"Compiled successfully: {args.input} -> {args.output}", file=sys.stderr)
    else:
        print(python_code)


if __name__ == "__main__":
    main()

# Ultra High-Level Language (UHL) Compiler

> **Write code in natural English. Compile to Python.**

UHL is an **ultra high-level programming language** that allows you to write code using natural English syntax, organized in paragraphs and long sentences. The compiler transforms your human-readable code into clean, executable Python.

## Features

- **Natural Language Syntax**: Write code using natural English sentences and paragraphs
- **Type-Safe Variables**: Declare variables with optional type hints (`integer`, `string`, `number`, `boolean`, `list`)
- **Comprehensive Loop Support**: `for each`, `while`, and `repeat` loops with intuitive syntax
- **Rich Operator Set**: Natural language operators (`add`, `subtract`, `multiply by`, `divide by`) or traditional symbols
- **Paragraph-Based Structure**: Organize code naturally in paragraphs and long sentences
- **Clean Python Output**: Generates readable, well-formatted Python code
- **Extensible Architecture**: Easy to extend with new statements, operators, and features

## Installation

### From Source

```bash
git clone <repository-url>
cd high-level
pip install -e .
```

### Direct Usage

No installation required! Use the CLI directly:

```bash
python cli.py input.uhl -o output.py
```

## Quick Start

### Example 1: Basic Variable Declarations

**Input** (`examples/basic.uhl`):
```uhl
Let me start by create a variable called x and set it to 5. This will be our starting point.

Now I want to create a variable called name as a string and set it to "Hello, World!" so we can greet the user properly.

We also need to track whether something is active, so let us create a variable called is_active as a boolean and set it to true.

Later on, we will need to update x, so let us make x become 10.

And finally, let us update the name so that name is now "Python".
```

**Compiled Output**:
```python
x = 5.0
name: str = 'Hello, World!'
is_active: bool = True
x = 10.0
name = 'Python'
```

### Example 2: Loops and Control Flow

**Input** (`examples/loops.uhl`):
```uhl
Let us start by create a variable called numbers and set it to [1, 2, 3, 4, 5]. This list contains the numbers we want to work with.

Now, for each number in numbers do
    Let us create a variable called squared and set it to number times number, which will calculate the square of each number. Then we will update squared so that squared becomes squared plus 1, adding one to the result.

After processing all the numbers, we need to set up a counter. Let us create a variable called counter and set it to 0.

Now we will use a while loop. While counter is less than 10 do
    counter becomes counter plus 1 each time through the loop.

Finally, repeat 5 times do
    create a variable called message and set it to "Iteration"
    message is now message
```

**Compiled Output**:
```python
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    squared = number * number
    squared = squared + 1
    counter = 0.0
    while counter < 10:
        counter = counter + 1
        for _ in range(5):
            message = 'Iteration'
            message = message
```

### Example 3: Operators and Expressions

**Input** (`examples/operators.uhl`):
```uhl
First, let us create a variable called a and set it to 10. Then we will create another variable called b and set it to 5.

Now we can perform some calculations. Let us create a variable called sum and set it to a plus b, which will give us the total of both numbers.

We can also multiply them together, so let us create a variable called product and set it to a times b.

For subtraction, we will create a variable called difference and set it to a minus b.

And for division, let us create a variable called quotient and set it to a divided by b.

We can also compare values. Let us create a variable called is_greater and set it to a is greater than b, which will tell us if a is larger.

Similarly, we can check equality by creating a variable called is_equal and set it to a is equal to b.

We can combine operations too. Let us create a variable called result and set it to a plus b times 2, which will calculate the sum first and then multiply by two.

Finally, we can use logical operations. Let us create a variable called condition and set it to a is greater than 5 and b is less than 10, which will be true only if both conditions are met.
```

**Compiled Output**:
```python
a = 10.0
b = 5.0
sum = a + b
product = a * b
difference = a - b
quotient = a / b
is_greater = a > b
it = a == b
result = a + b * 2
condition = a > 5 and b < 10
```

### Example 4: Complete Program

**Input** (`examples/complete.uhl`):
```uhl
Let us build a program that calculates statistics from a list of numbers. First, we will create a variable called total as an integer and set it to 0, which will hold our running sum.

Next, we need the numbers to work with, so let us create a variable called numbers as a list and set it to [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]. These are the values we will be processing.

Now we will iterate through each number. For each number in numbers, we want to add it to our total, so total becomes total plus number. This will accumulate the sum of all numbers in the list.

Once we have added up all the numbers, we can calculate the average. Let us create a variable called average and set it to total divided by 10, which gives us the mean value.

Now let us set up a counter for another task. We will create a variable called count and set it to 0.

We will use a while loop to count up. While count is less than 5, we will increment the counter so that count becomes count plus 1. During each iteration, we will also create a variable called message and set it to "Count is". Then we will update it so that message is now message.

After the while loop, we will do something a few times. Let us repeat 3 times, and each time we will create a variable called iteration and set it to "Processing". Then we will update it so that iteration is now iteration.

We can also check conditions. Let us create a variable called is_done as a boolean and set it to total is greater than 50, which will tell us if we have reached our threshold.

Finally, let us calculate a final result. We will create a variable called final_result and set it to average times 2 plus 10, which applies some transformation to our average value.
```

**Compiled Output**:
```python
total: int = 0
numbers: list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for number in numbers:
    total = total + number
    average = total / 10
    count = 0.0
    while count < 5:
        count = count + 1.0
        message = 'Count is'
        message = message
        for _ in range(3):
            iteration = 'Processing'
            iteration = iteration
            is_done: bool = total > 50
            final_result = average * 2 + 10
```

## Language Documentation

### Variable Declarations

Declare variables with natural language syntax:

```
declare a variable named <name> [as <type>] and set it to <expression>
create a variable called <name> [as <type>] and set it to <expression>
```

**Supported Types**:
- `integer` → `int`
- `string` → `str`
- `number` → `float`
- `boolean` → `bool`
- `list` → `list`

**Examples**:
```uhl
declare a variable named x and set it to 5
create a variable called name as string and set it to "Hello"
declare a variable named is_active as boolean and set it to true
```

### Variable Assignments

Update existing variables using natural language:

```
set <name> to <expression>
<name> becomes <expression>
<name> is now <expression>
make <name> become <expression>
```

**Examples**:
```uhl
set x to 10
counter becomes counter plus 1
name is now "Python"
```

### For Each Loop

Iterate over collections:

```
for each <item> in <iterable>, do
    <statements>

for each <item> in <iterable> do
    <statements>
```

**Example**:
```uhl
for each number in numbers, do
    declare a variable named squared and set it to number multiply by number
```

### While Loop

Conditional iteration:

```
while <condition> [is true], do
    <statements>

while <condition> do
    <statements>
```

**Example**:
```uhl
while counter is less than 10, do
    set counter to counter add 1
```

### Repeat Loop

Fixed iteration count:

```
repeat <count> times, do
    <statements>

repeat <count> times do
    <statements>
```

**Example**:
```uhl
repeat 5 times, do
    declare a variable named message and set it to "Iteration"
```

### Operators

UHL supports both natural language and traditional operators:

#### Arithmetic Operators

| Natural Language | Symbol | Example |
|-----------------|--------|---------|
| `add` / `plus` | `+` | `a add b` or `a + b` |
| `subtract` / `minus` | `-` | `a subtract b` or `a - b` |
| `multiply by` / `times` | `*` | `a multiply by b` or `a * b` |
| `divide by` / `divided by` | `/` | `a divide by b` or `a / b` |

#### Comparison Operators

| Natural Language | Symbol | Example |
|-----------------|--------|---------|
| `greater than` | `>` | `a greater than b` or `a > b` |
| `less than` | `<` | `a less than b` or `a < b` |
| `equal to` | `==` | `a equal to b` or `a == b` |
| `not equal to` | `!=` | `a not equal to b` or `a != b` |
| `greater than or equal to` | `>=` | `a >= b` |
| `less than or equal to` | `<=` | `a <= b` |

#### Logical Operators

| Natural Language | Symbol | Example |
|-----------------|--------|---------|
| `and` | `and` | `a > 5 and b < 10` |
| `or` | `or` | `a > 5 or b < 10` |
| `not` | `not` | `not is_active` |

### Expressions

Expressions can include:
- **Literals**: numbers, strings, booleans, lists
- **Identifiers**: variable names
- **Binary operations**: arithmetic, comparison, logical
- **Unary operations**: `not`
- **Parenthesized expressions**: `(a + b) * 2`

## Testing

The compiler includes comprehensive test coverage. Run the test suite:

```bash
pytest tests/
```

### Test Examples

The test suite validates that example programs compile to expected Python output:

```python
def test_basic_uhl():
    """Test that basic.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "basic.uhl"))
    
    expected = """x = 5.0
name: str = 'Hello, World!'
is_active: bool = True
x = 10.0
name = 'Python'"""
    
    assert actual.strip() == expected.strip()
```

All example files in the `examples/` directory are tested to ensure they produce the correct Python output.

## Usage

### Command Line Interface

Compile a file to Python:

```bash
python cli.py input.uhl -o output.py
```

Output to stdout:

```bash
python cli.py input.uhl
```

Read from stdin:

```bash
echo "declare a variable named x and set it to 5" | python cli.py -
```

### Programmatic API

Use the compiler in your Python code:

```python
from src.compiler import Compiler

compiler = Compiler()

# Compile from string
source_code = """
declare a variable named x and set it to 5
declare a variable named y and set it to x add 10
"""
python_code = compiler.compile(source_code)
print(python_code)

# Compile from file
python_code = compiler.compile_file("examples/basic.uhl")
print(python_code)
```

### API Reference

#### `Compiler`

Main compiler class that orchestrates lexing, parsing, and code generation.

**Methods**:

- `compile(source_code: str) -> str`
  - Compile source code from UHL to Python
  - **Parameters**: `source_code` - The source code in UHL
  - **Returns**: Generated Python code
  - **Raises**: `SyntaxError` if there's a syntax error

- `compile_file(file_path: str) -> str`
  - Compile a file from UHL to Python
  - **Parameters**: `file_path` - Path to the source file
  - **Returns**: Generated Python code

## Project Structure

```
.
├── src/
│   ├── ast.py          # Abstract Syntax Tree node definitions
│   ├── lexer.py        # Tokenizer (lexical analysis)
│   ├── parser.py       # Parser (syntax analysis)
│   ├── codegen.py      # Python code generator
│   └── compiler.py     # Main compiler orchestrator
├── examples/           # Example UHL programs
│   ├── basic.uhl       # Basic variable declarations
│   ├── loops.uhl       # Loop examples
│   ├── operators.uhl   # Operator examples
│   └── complete.uhl    # Complete example program
├── tests/              # Unit tests
│   └── test_examples.py # Tests for example programs
├── cli.py              # Command-line interface
├── setup.py            # Package setup
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Extensibility

The compiler is designed for easy extensibility. You can add new features by extending the parser, AST, and code generator.

### Adding a New Statement Type

1. **Add AST Node** (`src/ast.py`):
```python
class PrintStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)
```

2. **Add Parser Pattern** (`src/parser.py`):
```python
def parse_print_statement(self) -> PrintStatement:
    self.expect(TokenType.KEYWORD, 'print')
    expr = self.parse_expression()
    return PrintStatement(expr)
```

3. **Add Code Generation** (`src/codegen.py`):
```python
def visit_print_statement(self, node: PrintStatement) -> str:
    expr_code = self.generate(node.expression)
    return f"print({expr_code})"
```

### Adding New Operators

Extend the expression parsing in `src/parser.py` to recognize new operator patterns and map them to appropriate AST nodes.

## Examples

All example programs are located in the `examples/` directory:

- **`basic.uhl`** - Basic variable declarations and assignments
- **`loops.uhl`** - Demonstrates `for each`, `while`, and `repeat` loops
- **`operators.uhl`** - Shows arithmetic, comparison, and logical operators
- **`complete.uhl`** - A complete example combining all language features

Compile any example:

```bash
python cli.py examples/basic.uhl
```
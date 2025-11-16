"""Parser for natural language constructs."""

from typing import List, Optional

from src.ast import (
    Assignment,
    BinaryOp,
    Expression,
    ForLoop,
    Identifier,
    ListLiteral,
    Literal,
    Program,
    RepeatLoop,
    Statement,
    UnaryOp,
    VariableDeclaration,
    WhileLoop,
)
from src.lexer import Token, TokenType


class Parser:
    """Parses tokens into an Abstract Syntax Tree."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def error(self, message: str):
        """Raise a parser error with position information."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            raise SyntaxError(
                f"Parser error at line {token.line}, column {token.column}: {message}"
            )
        else:
            raise SyntaxError(f"Parser error at end of input: {message}")

    def current_token(self) -> Optional[Token]:
        """Get the current token."""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at a token ahead."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def advance(self):
        """Move to the next token."""
        if self.pos < len(self.tokens):
            self.pos += 1

    def expect(self, token_type: TokenType, value: Optional[str] = None):
        """Expect a specific token type and optionally value."""
        token = self.current_token()
        if token is None or token.type != token_type:
            expected = f"{token_type.name}" + (f" with value {value!r}" if value else "")
            self.error(f"Expected {expected}, got {token.type.name if token else 'EOF'}")
        if value is not None and token.value.lower() != value.lower():
            self.error(f"Expected {value!r}, got {token.value!r}")
        self.advance()
        return token

    def skip_optional(self, token_type: TokenType, value: Optional[str] = None):
        """Skip a token if it matches, otherwise do nothing."""
        token = self.current_token()
        if token and token.type == token_type:
            if value is None or token.value.lower() == value.lower():
                self.advance()
                return True
        return False

    def skip_optional_keyword_or_identifier(self, value: str):
        """Skip a token if it matches the value, whether it's a keyword or identifier."""
        token = self.current_token()
        if token and token.value.lower() == value.lower():
            if token.type in (TokenType.KEYWORD, TokenType.IDENTIFIER):
                self.advance()
                return True
        return False

    def skip_paragraph_breaks(self):
        """Skip paragraph break tokens."""
        while self.current_token() and self.current_token().type == TokenType.PARAGRAPH_BREAK:
            self.advance()

    def skip_narrative_words(self):
        """Skip common narrative/introductory words that don't affect meaning."""
        # Keywords that start actual statements
        statement_starters = {"declare", "create", "set", "for", "while", "repeat", "if", "else"}
        # Keywords that are part of statements (should not be skipped)
        # Note: "now", "to", "is", "and", and "each" are not included here because they can be narrative (handled separately)
        statement_keywords = {
            "variable",
            "named",
            "called",
            "as",
            "it",
            "or",
            "not",
            "in",
            "do",
            "true",
            "false",
            "times",
            "equals",
            "becomes",
            "become",
            "plus",
            "minus",
            "divided",
            "greater",
            "than",
            "less",
            "equal",
        }

        base_narrative_words = {
            "let",
            "me",
            "start",
            "by",
            "now",
            "first",
            "then",
            "next",
            "also",
            "we",
            "want",
            "need",
            "will",
            "can",
            "should",
            "shall",
            "must",
            "after",
            "before",
            "during",
            "finally",
            "later",
            "on",
            "once",
            "this",
            "that",
            "these",
            "those",
            "so",
            "which",
            "who",
            "what",
            "when",
            "where",
            "why",
            "how",
            "whether",
            "some",
            "any",
            "every",
            "all",
            "both",
            "either",
            "neither",
            "another",
            "other",
            "such",
            "same",
            "different",
            "new",
            "old",
            "last",
            "be",
            "our",
            "their",
            "my",
            "your",
            "his",
            "her",
            "its",
            "us",
            "them",
            "they",
            "he",
            "she",
            "it",
            "i",
            "make",
            "makes",
            "made",
            "point",
            "way",
            "thing",
            "things",
            "one",
            "ones",
            "here",
            "there",
            "up",
            "down",
            "out",
            "in",
            "off",
            "over",
            "under",
            "through",
            "the",
            "track",
            "something",
            "active",
            "greet",
            "user",
            "properly",
            "update",
            "and",
            "list",
            "contains",
            "numbers",
            "work",
            "with",
            "do",
            "of",
            "each",
            "calculate",
            "square",
            "adding",
            "result",
            "processing",
            "set",
            "counter",
            "increment",
            "time",
            "loop",
            "specific",
            "times",
            "iteration",
            "change",
            "demonstrates",
            "assignment",
            "number",
            "variable",
            "called",
            "perform",
            "calculations",
            "multiply",
            "together",
            "subtraction",
            "division",
            "compare",
            "values",
            "larger",
            "similarly",
            "check",
            "equality",
            "combine",
            "operations",
            "logical",
            "met",
            "build",
            "program",
            "calculates",
            "statistics",
            "from",
            "hold",
            "running",
            "sum",
            "iterate",
            "accumulate",
            "added",
            "add",
            "average",
            "mean",
            "value",
            "task",
            "count",
            "conditions",
            "reached",
            "threshold",
            "transformation",
            "use",
        }

        def is_narrative_word(word):
            """Check if a word is a narrative word, including verb forms."""
            word_lower = word.lower()
            if word_lower in base_narrative_words:
                return True
            # Don't skip exact statement starters - they're needed for matching
            if word_lower in statement_starters:
                return False
            # Check verb forms of narrative words (but not statement starters)
            for base in base_narrative_words:
                if word_lower.startswith(base) and len(word_lower) > len(base):
                    return True
            return False

        skipped_any = False

        while self.current_token():
            token = self.current_token()
            word = token.value.lower() if token.value else ""

            # Special case: "a" can be narrative (like "a counter", "a while loop")
            # Check this BEFORE checking statement starters, so we can skip "a" even if followed by statement starters
            if token.type == TokenType.KEYWORD and word == "a":
                peek = self.peek_token()
                # Check if "a" is preceded by narrative words (like "from", "to", "with", etc.)
                # If so, it's likely narrative even if followed by type keywords
                is_preceded_by_narrative = False
                if self.pos > 0:
                    prev_token = self.tokens[self.pos - 1]
                    if prev_token:
                        prev_word = prev_token.value.lower() if prev_token.value else ""
                        narrative_preceders = {
                            "from",
                            "to",
                            "with",
                            "in",
                            "on",
                            "at",
                            "for",
                            "of",
                            "by",
                            "about",
                            "into",
                            "onto",
                            "upon",
                        }
                        if prev_word in narrative_preceders or (
                            prev_token.type in (TokenType.IDENTIFIER, TokenType.KEYWORD)
                            and prev_word in base_narrative_words
                        ):
                            is_preceded_by_narrative = True

                # If "a" is followed by narrative words, identifiers, or certain keywords, it's probably narrative
                if peek:
                    # Check if it's a known statement pattern like "a variable"
                    if peek.type == TokenType.IDENTIFIER:
                        if (
                            peek.value.lower()
                            not in ("variable", "list", "string", "integer", "number", "boolean")
                            or is_preceded_by_narrative
                        ):
                            self.advance()
                            skipped_any = True
                            continue
                    elif peek.type == TokenType.KEYWORD:
                        # "a" followed by keywords like "while" (in "a while loop") is narrative
                        # But "a variable" is a statement pattern, so check for that
                        # However, if preceded by narrative words, skip it anyway
                        if (
                            peek.value.lower()
                            not in ("variable", "list", "string", "integer", "number", "boolean")
                            or is_preceded_by_narrative
                        ):
                            self.advance()
                            skipped_any = True
                            continue

            # If we hit a statement starter exactly, stop skipping
            # But "while" can be narrative (like "use a while loop"), so check context
            if token.type == TokenType.KEYWORD and word in statement_starters:
                # Special case: "while" in "a while loop" is narrative
                if word == "while":
                    peek = self.peek_token()
                    # If "while" is followed by "loop" (identifier), it's narrative
                    if peek and peek.type == TokenType.IDENTIFIER and peek.value.lower() == "loop":
                        self.advance()
                        skipped_any = True
                        continue
                break
            if token.type == TokenType.IDENTIFIER and word in statement_starters:
                break

            # If we hit a statement keyword (like "variable"), stop skipping
            # Exception: "it" can be narrative (like "add it to") or part of a statement (like "set it to")
            # Only stop skipping "it" if it's followed by "to" and preceded by "set"
            if token.type == TokenType.KEYWORD and word in statement_keywords:
                if word == "it":
                    # Check if "it" is part of "set it to" pattern
                    peek = self.peek_token()
                    if peek and peek.value.lower() == "to":
                        # Check if "set" appears recently before "it"
                        is_set_it_to = False
                        for i in range(max(0, self.pos - 5), self.pos):
                            if i < len(self.tokens) and self.tokens[i].value.lower() == "set":
                                is_set_it_to = True
                                break
                        if is_set_it_to:
                            break
                        self.advance()
                        skipped_any = True
                        continue
                else:
                    break

            # Check if "each" is part of "for each" (statement) vs narrative (like "of each number")
            if token.type == TokenType.KEYWORD and word == "each":
                if self.pos > 0:
                    prev_token = self.tokens[self.pos - 1]
                    if prev_token and prev_token.value.lower() == "for":
                        break
                self.advance()
                skipped_any = True
                continue

            # Check if this might be an identifier starting an assignment (x becomes, x equals, etc.)
            if token.type == TokenType.IDENTIFIER:
                peek = self.peek_token()
                if peek and peek.value.lower() in ("equals", "=", "becomes", "become"):
                    break
                # Only break for "is now" pattern (assignment), not just "is" (which could be comparison)
                if peek and peek.value.lower() == "is":
                    peek2 = self.peek_token(2)
                    if peek2 and peek2.value.lower() == "now":
                        break

            # Skip narrative words and punctuation
            # Also skip "to" if it's part of narrative (like "want to", "need to")
            # But don't skip "now" if it's part of "is now" assignment pattern
            # Don't skip "and" if it's part of "and set it to" pattern
            is_now_in_assignment = False
            if word == "now":
                if self.pos > 0:
                    prev_token = self.tokens[self.pos - 1]
                    if prev_token and prev_token.value.lower() == "is":
                        is_now_in_assignment = True
                    for i in range(max(0, self.pos - 3), self.pos):
                        if i < len(self.tokens) and self.tokens[i].value.lower() == "is":
                            has_keyword_between = False
                            for j in range(i + 1, self.pos):
                                if j < len(self.tokens):
                                    tok_val = self.tokens[j].value.lower()
                                    if tok_val in statement_starters:
                                        has_keyword_between = True
                                        break
                            if not has_keyword_between:
                                is_now_in_assignment = True
                                break

            is_and_in_statement = False
            if word == "and":
                peek = self.peek_token()
                if peek and peek.value.lower() == "set":
                    is_and_in_statement = True

            is_do_in_loop = False
            if word == "do":
                for i in range(max(0, self.pos - 5), self.pos):
                    if i < len(self.tokens):
                        tok_val = self.tokens[i].value.lower()
                        if tok_val in ("for", "while", "repeat", "each"):
                            is_do_in_loop = True
                            break

            if (
                (
                    token.type in (TokenType.IDENTIFIER, TokenType.KEYWORD)
                    and is_narrative_word(word)
                    and not is_now_in_assignment
                    and not is_and_in_statement
                    and not is_do_in_loop
                )
                or (token.type == TokenType.KEYWORD and word == "to" and skipped_any)
                or (token.type == TokenType.PUNCTUATION and token.value in (",", ".", ";", ":"))
            ):
                self.advance()
                skipped_any = True
            elif skipped_any and token.type == TokenType.IDENTIFIER:
                peek = self.peek_token()
                if peek and peek.value.lower() in ("equals", "=", "becomes", "become", "is"):
                    break
                self.advance()
                skipped_any = True
            else:
                if not skipped_any:
                    break
                break

    def parse(self) -> Program:
        """Parse the tokens into a Program AST node."""
        statements = []

        while self.current_token() and self.current_token().type != TokenType.EOF:
            self.skip_paragraph_breaks()
            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)

        return Program(statements)

    def parse_statement(self) -> Optional[Statement]:
        """Parse a statement."""
        self.skip_paragraph_breaks()
        self.skip_narrative_words()

        token = self.current_token()
        if token and token.value.lower() == "set":
            peek = self.peek_token()
            if peek and peek.value.lower() == "up":
                self.advance()
                self.advance()
                token_after_up = self.current_token()
                if token_after_up and token_after_up.value.lower() == "a":
                    self.advance()
                    token_after_a = self.current_token()
                    if token_after_a and token_after_a.type == TokenType.IDENTIFIER:
                        self.advance()
                self.skip_narrative_words()
                return self.parse_statement()

        token = self.current_token()

        if not token or token.type in (TokenType.EOF, TokenType.PARAGRAPH_BREAK):
            return None

        token_value = token.value.lower() if token.value else ""
        saved_pos = self.pos

        if token_value.startswith("declare"):
            if token_value != "declare":
                self.advance()
            if self.match_keyword_sequence(["a", "variable", "named"]):
                self.pos = saved_pos
                if self.match_keyword_sequence(["declare", "a", "variable", "named"]):
                    return self.parse_variable_declaration()
                self.pos = saved_pos

        if token_value.startswith("create"):
            return self.parse_variable_declaration()

        if self.match_keyword_sequence(["declare", "a", "variable", "named"]):
            return self.parse_variable_declaration()

        if token.value.lower() == "set":
            if self.match_keyword_sequence(["set"]):
                return self.parse_assignment()

        if self.match_keyword_sequence(["for", "each"]):
            return self.parse_for_loop()

        if self.match_keyword_sequence(["while"]):
            return self.parse_while_loop()

        if self.match_keyword_sequence(["repeat"]):
            return self.parse_repeat_loop()

        if token.type == TokenType.IDENTIFIER:
            peek = self.peek_token()
            if peek:
                if peek.value.lower() in ("equals", "=", "becomes", "become"):
                    return self.parse_assignment()
                elif peek.value.lower() == "is":
                    peek2 = self.peek_token(2)
                    if peek2 and peek2.value.lower() == "now":
                        return self.parse_assignment()

        if token:
            self.advance()
        return None

    def match_keyword_sequence(self, keywords: List[str]) -> bool:
        """Check if the next tokens match a sequence of keywords, handling verb forms."""
        saved_pos = self.pos

        for i, keyword in enumerate(keywords):
            token = self.current_token()
            if not token:
                self.pos = saved_pos
                return False

            token_value = token.value.lower() if token.value else ""
            keyword_lower = keyword.lower()

            if (
                token.type == TokenType.KEYWORD or token.type == TokenType.IDENTIFIER
            ) and token_value == keyword_lower:
                self.advance()
                continue

            if (
                i == 0
                and token_value.startswith(keyword_lower)
                and len(token_value) > len(keyword_lower)
            ):
                self.advance()
                continue

            self.pos = saved_pos
            return False

        self.pos = saved_pos
        return True

    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse: declare a variable named X [as TYPE] and set it to Y
        or: create a variable called X [as TYPE] and set it to Y
        Can also be called after advancing past verb forms like "creating"."""
        token = self.current_token()
        if not token:
            self.error("Unexpected end of input in variable declaration")
        token_value = token.value.lower() if token.value else ""

        if token_value == "a":
            peek = self.peek_token(1)
            if peek and peek.value.lower() == "variable":
                peek2 = self.peek_token(2)
                if peek2 and peek2.value.lower() == "named":
                    self.skip_optional(TokenType.KEYWORD, "a")
                    self.expect(TokenType.KEYWORD, "variable")
                    self.expect(TokenType.KEYWORD, "named")
                elif peek2 and peek2.value.lower() == "called":
                    self.skip_optional(TokenType.KEYWORD, "a")
                    self.expect(TokenType.KEYWORD, "variable")
                    self.expect(TokenType.KEYWORD, "called")
                else:
                    self.error("Expected 'named' or 'called' after 'variable'")
            else:
                self.error("Expected 'variable' after 'a'")
        elif token_value == "declare" or (
            token_value.startswith("declare") and len(token_value) > len("declare")
        ):
            if token.type == TokenType.KEYWORD:
                self.expect(TokenType.KEYWORD, "declare")
            else:
                self.advance()
            self.skip_optional(TokenType.KEYWORD, "a")
            self.expect(TokenType.KEYWORD, "variable")
            self.expect(TokenType.KEYWORD, "named")
        elif token_value == "create" or (
            token_value.startswith("create") and len(token_value) > len("create")
        ):
            if token.type == TokenType.KEYWORD:
                self.expect(TokenType.KEYWORD, "create")
            else:
                self.advance()
            self.skip_narrative_words()
            self.skip_optional(TokenType.KEYWORD, "a")
            self.expect(TokenType.KEYWORD, "variable")
            self.expect(TokenType.KEYWORD, "called")
        else:
            self.error("Expected 'declare' or 'create' for variable declaration")

        token = self.current_token()
        if token.type == TokenType.IDENTIFIER:
            name_token = self.expect(TokenType.IDENTIFIER)
            name = name_token.value
        elif token.type == TokenType.KEYWORD:
            name_token = self.expect(TokenType.KEYWORD)
            name = name_token.value
        else:
            self.error(f"Expected identifier for variable name, got {token.type.name}")
            name = ""

        var_type = None
        if self.skip_optional(TokenType.KEYWORD, "as"):
            self.skip_optional(TokenType.KEYWORD, "a")
            self.skip_optional(TokenType.KEYWORD, "an")
            type_token = self.expect(TokenType.KEYWORD)
            var_type = type_token.value

        if self.skip_optional(TokenType.KEYWORD, "and"):
            self.expect(TokenType.KEYWORD, "set")
            self.skip_optional(TokenType.KEYWORD, "it")
            self.expect(TokenType.KEYWORD, "to")
        else:
            self.expect(TokenType.KEYWORD, "to")

        value = self.parse_expression()

        return VariableDeclaration(name, value, var_type)

    def parse_assignment(self) -> Assignment:
        """Parse: set X to Y or X equals Y or X becomes Y or X is now Y"""
        token = self.current_token()

        if token.value.lower() == "set":
            self.expect(TokenType.KEYWORD, "set")
            name_token = self.current_token()
            if name_token and (
                name_token.type == TokenType.IDENTIFIER
                or (name_token.type == TokenType.KEYWORD and name_token.value.lower() == "it")
            ):
                self.advance()
            else:
                self.error(
                    f"Expected identifier for variable name, got {name_token.type.name if name_token else 'EOF'}"
                )
            self.expect(TokenType.KEYWORD, "to")
            value = self.parse_expression()
            return Assignment(name_token.value, value)
        else:
            name_token = self.expect(TokenType.IDENTIFIER)
            if (
                self.skip_optional(TokenType.KEYWORD, "equals")
                or self.skip_optional(TokenType.OPERATOR, "=")
                or self.skip_optional(TokenType.KEYWORD, "becomes")
                or self.skip_optional(TokenType.KEYWORD, "become")
            ):
                value = self.parse_expression()
                return Assignment(name_token.value, value)
            elif self.skip_optional(TokenType.KEYWORD, "is"):
                if self.skip_optional(TokenType.KEYWORD, "now"):
                    value = self.parse_expression()
                    return Assignment(name_token.value, value)
                else:
                    self.error("Expected 'now' after 'is' in assignment")
            else:
                self.error(
                    "Expected 'equals', '=', 'become', 'becomes', or 'is now' after identifier"
                )

    def parse_for_loop(self) -> ForLoop:
        """Parse: for each X in Y, do ..."""
        self.expect(TokenType.KEYWORD, "for")
        self.expect(TokenType.KEYWORD, "each")

        token = self.current_token()
        if token.type == TokenType.IDENTIFIER:
            item_token = self.expect(TokenType.IDENTIFIER)
            item_var = item_token.value
        elif token.type == TokenType.KEYWORD:
            item_token = self.expect(TokenType.KEYWORD)
            item_var = item_token.value
        else:
            self.error(f"Expected identifier for loop variable, got {token.type.name}")
            item_var = ""

        self.expect(TokenType.KEYWORD, "in")

        iterable = self.parse_expression()

        self.skip_optional(TokenType.PUNCTUATION, ",")

        self.skip_narrative_words()

        self.skip_optional(TokenType.KEYWORD, "do")

        body = self.parse_block()

        return ForLoop(item_var, iterable, body)

    def parse_while_loop(self) -> WhileLoop:
        """Parse: while X is true, do ... or while X, do ..."""
        self.expect(TokenType.KEYWORD, "while")

        condition = self.parse_expression()

        if (
            self.current_token()
            and self.current_token().type == TokenType.KEYWORD
            and self.current_token().value.lower() == "is"
        ):
            self.advance()
            if (
                self.current_token()
                and self.current_token().type == TokenType.KEYWORD
                and self.current_token().value.lower() == "true"
            ):
                self.advance()

        self.skip_optional(TokenType.PUNCTUATION, ",")

        self.skip_narrative_words()

        self.skip_optional(TokenType.KEYWORD, "do")

        body = self.parse_block()

        return WhileLoop(condition, body)

    def parse_repeat_loop(self) -> RepeatLoop:
        """Parse: repeat N times, do ..."""
        self.expect(TokenType.KEYWORD, "repeat")

        count = self.parse_primary()

        self.expect(TokenType.KEYWORD, "times")

        self.skip_optional(TokenType.PUNCTUATION, ",")

        self.skip_narrative_words()

        self.skip_optional(TokenType.KEYWORD, "do")

        body = self.parse_block()

        return RepeatLoop(count, body)

    def parse_block(self) -> List[Statement]:
        """Parse a block of statements."""
        body = []

        self.skip_paragraph_breaks()

        while True:
            token = self.current_token()
            if not token or token.type == TokenType.EOF or token.type == TokenType.PARAGRAPH_BREAK:
                break

            saved_pos = self.pos
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            elif self.pos == saved_pos:
                break

            self.skip_paragraph_breaks()

        return body

    def parse_expression(self) -> Expression:
        """Parse an expression."""
        token = self.current_token()
        if token:
            statement_keywords = {
                "create",
                "declare",
                "set",
                "for",
                "while",
                "repeat",
                "if",
                "then",
                "else",
                "each",
            }
            if (token.type == TokenType.KEYWORD and token.value.lower() in statement_keywords) or (
                token.type == TokenType.IDENTIFIER and token.value.lower() in statement_keywords
            ):
                self.error(f"Unexpected statement keyword '{token.value}' - expression expected")
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expression:
        """Parse logical OR expression."""
        left = self.parse_logical_and()

        statement_keywords = {
            "create",
            "declare",
            "set",
            "for",
            "while",
            "repeat",
            "if",
            "then",
            "else",
            "each",
        }

        while self.current_token() and self.current_token().value.lower() == "or":
            peek = self.peek_token()
            if peek and (
                (peek.type == TokenType.KEYWORD and peek.value.lower() in statement_keywords)
                or (peek.type == TokenType.IDENTIFIER and peek.value.lower() in statement_keywords)
            ):
                break
            op_token = self.expect(TokenType.KEYWORD, "or")
            right = self.parse_logical_and()
            left = BinaryOp(left, "or", right)

        return left

    def parse_logical_and(self) -> Expression:
        """Parse logical AND expression."""
        left = self.parse_comparison()

        statement_keywords = {
            "create",
            "declare",
            "set",
            "for",
            "while",
            "repeat",
            "if",
            "then",
            "else",
            "each",
        }
        narrative_after_and = {
            "finally",
            "then",
            "next",
            "also",
            "so",
            "let",
            "us",
            "we",
            "create",
            "declare",
            "set",
            "for",
            "while",
            "repeat",
            "each",
        }

        while self.current_token() and self.current_token().value.lower() == "and":
            peek = self.peek_token()
            if peek and (
                peek.value.lower() in narrative_after_and
                or (peek.type == TokenType.KEYWORD and peek.value.lower() in statement_keywords)
                or (peek.type == TokenType.IDENTIFIER and peek.value.lower() in statement_keywords)
            ):
                break
            op_token = self.expect(TokenType.KEYWORD, "and")
            right = self.parse_comparison()
            left = BinaryOp(left, "and", right)

        return left

    def parse_comparison(self) -> Expression:
        """Parse comparison expression."""
        left = self.parse_additive()

        while self.current_token():
            token = self.current_token()

            if token.type == TokenType.KEYWORD:
                if token.value.lower() == "is":
                    self.advance()
                    token = self.current_token()
                    if token and token.type == TokenType.KEYWORD:
                        if token.value.lower() == "greater":
                            self.advance()
                            token = self.current_token()
                            if token and token.value.lower() == "than":
                                self.advance()
                            else:
                                self.error("Expected 'than' after 'is greater'")
                            right = self.parse_additive()
                            left = BinaryOp(left, ">", right)
                            continue
                        elif token.value.lower() == "less":
                            self.advance()
                            token = self.current_token()
                            if token and token.value.lower() == "than":
                                self.advance()
                            else:
                                self.error("Expected 'than' after 'is less'")
                            right = self.parse_additive()
                            left = BinaryOp(left, "<", right)
                            continue
                        elif token.value.lower() == "equal":
                            self.advance()
                            self.skip_optional(TokenType.KEYWORD, "to")
                            right = self.parse_additive()
                            left = BinaryOp(left, "==", right)
                            continue
                    # If 'is' is not followed by a comparison keyword, backtrack
                    self.pos -= 1
                    break
                elif token.value.lower() == "greater":
                    self.advance()
                    token = self.current_token()
                    if token and token.value.lower() == "than":
                        self.advance()
                    else:
                        self.error("Expected 'than' after 'greater'")
                    right = self.parse_additive()
                    left = BinaryOp(left, ">", right)
                    continue
                elif token.value.lower() == "less":
                    self.advance()
                    token = self.current_token()
                    if token and token.value.lower() == "than":
                        self.advance()
                    else:
                        self.error("Expected 'than' after 'less'")
                    right = self.parse_additive()
                    left = BinaryOp(left, "<", right)
                    continue
                elif token.value.lower() == "equal":
                    self.advance()
                    self.skip_optional(TokenType.KEYWORD, "to")
                    right = self.parse_additive()
                    left = BinaryOp(left, "==", right)
                    continue

            if token.type == TokenType.OPERATOR and token.value in (
                "==",
                "!=",
                "<=",
                ">=",
                "<",
                ">",
            ):
                op = token.value
                self.advance()
                right = self.parse_additive()
                left = BinaryOp(left, op, right)
                continue

            break

        return left

    def parse_additive(self) -> Expression:
        """Parse additive expression (+, -)."""
        left = self.parse_multiplicative()

        while self.current_token():
            token = self.current_token()

            if token.type == TokenType.KEYWORD:
                if token.value.lower() == "add":
                    self.advance()
                    self.skip_optional(TokenType.KEYWORD, "to")
                    right = self.parse_multiplicative()
                    left = BinaryOp(left, "+", right)
                    continue
                elif token.value.lower() == "plus":
                    self.advance()
                    right = self.parse_multiplicative()
                    left = BinaryOp(left, "+", right)
                    continue
                elif token.value.lower() == "subtract":
                    self.advance()
                    self.skip_optional(TokenType.KEYWORD, "from")
                    right = self.parse_multiplicative()
                    left = BinaryOp(left, "-", right)
                    continue
                elif token.value.lower() == "minus":
                    self.advance()
                    right = self.parse_multiplicative()
                    left = BinaryOp(left, "-", right)
                    continue

            if token.type == TokenType.OPERATOR and token.value in ("+", "-"):
                op = token.value
                self.advance()
                right = self.parse_multiplicative()
                left = BinaryOp(left, op, right)
                continue

            break

        return left

    def parse_multiplicative(self) -> Expression:
        """Parse multiplicative expression (*, /)."""
        left = self.parse_unary()

        while self.current_token():
            token = self.current_token()

            if token.type == TokenType.KEYWORD:
                if token.value.lower() == "multiply":
                    self.advance()
                    self.skip_optional_keyword_or_identifier("by")
                    right = self.parse_unary()
                    left = BinaryOp(left, "*", right)
                    continue
                elif token.value.lower() == "times":
                    self.advance()
                    right = self.parse_unary()
                    left = BinaryOp(left, "*", right)
                    continue
                elif token.value.lower() == "divide" or token.value.lower() == "divided":
                    self.advance()
                    self.skip_optional_keyword_or_identifier("by")
                    right = self.parse_unary()
                    left = BinaryOp(left, "/", right)
                    continue

            if token.type == TokenType.OPERATOR and token.value in ("*", "/"):
                op = token.value
                self.advance()
                right = self.parse_unary()
                left = BinaryOp(left, op, right)
                continue

            break

        return left

    def parse_unary(self) -> Expression:
        """Parse unary expression."""
        token = self.current_token()

        if token and token.type == TokenType.KEYWORD and token.value.lower() == "not":
            self.advance()
            operand = self.parse_unary()
            return UnaryOp("not", operand)

        if token and token.type == TokenType.OPERATOR and token.value == "-":
            self.advance()
            operand = self.parse_unary()
            return UnaryOp("-", operand)

        return self.parse_primary()

    def parse_primary(self) -> Expression:
        """Parse primary expression (literals, identifiers, parenthesized)."""
        token = self.current_token()

        if not token:
            self.error("Unexpected end of input")

        statement_keywords = {
            "create",
            "declare",
            "set",
            "for",
            "while",
            "repeat",
            "if",
            "then",
            "else",
            "each",
        }

        if token.type == TokenType.KEYWORD and token.value.lower() in statement_keywords:
            self.error(f"Unexpected statement keyword '{token.value}' in expression")

        if token.type == TokenType.NUMBER:
            self.advance()
            value = float(token.value) if "." in token.value else int(token.value)
            return Literal(value)

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type == TokenType.KEYWORD and token.value.lower() in ("true", "false"):
            self.advance()
            return Literal(token.value.lower() == "true")

        if token.type == TokenType.IDENTIFIER:
            if token.value.lower() in statement_keywords:
                self.error(f"Unexpected statement keyword '{token.value}' in expression")
            self.advance()
            return Identifier(token.value)

        if token.type == TokenType.KEYWORD:
            if token.value.lower() not in (
                "true",
                "false",
                "and",
                "or",
                "not",
                "in",
                "is",
                "do",
                "to",
                "from",
                "by",
                "than",
                "equals",
                "plus",
                "minus",
                "times",
                "divided",
                "becomes",
                "called",
                "create",
                "now",
            ):
                self.advance()
                return Identifier(token.value)

        if token.type == TokenType.PUNCTUATION and token.value == "[":
            return self.parse_list_literal()

        if token.type == TokenType.PUNCTUATION and token.value == "(":
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.PUNCTUATION, ")")
            return expr

        self.error(f"Unexpected token in expression: {token.value!r}")

    def parse_list_literal(self) -> Expression:
        """Parse a list literal: [expr1, expr2, ...]"""
        self.expect(TokenType.PUNCTUATION, "[")

        elements = []

        if self.current_token() and self.current_token().value == "]":
            self.advance()
            return ListLiteral([])

        elements.append(self.parse_expression())

        while self.current_token() and self.current_token().value == ",":
            self.advance()
            elements.append(self.parse_expression())

        self.expect(TokenType.PUNCTUATION, "]")

        return ListLiteral(elements)

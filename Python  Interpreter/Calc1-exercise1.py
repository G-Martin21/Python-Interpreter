# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
#INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

# Note to myself: dunder methods (double underscore method) -> https://dbader.org/blog/python-dunder-methods
# The methods __str__ and __repr__ -> https://dbader.org/blog/python-repr-vs-str
# https://www.pythontutorial.net/python-oop/python-__repr__/


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens (a token has a type and a value)
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token  # Note to myself: we use __str__ and __repr__ in the class Token to control
            # which representation we got from the class. If we do not add that __repr__ calls to __str__
            # this 'return' will give us a representation of a class <class '__main__.Token'> and not a str Token(INTEGER, 3

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        elif current_char == "-":
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # evaluate if there are more digits
        left_total = left.value
        while self.current_token.type == "INTEGER":
            left = self.current_token
            self.eat(INTEGER)
            # concatenate the different int tokens
            left_total = int(str(left_total)+str(left.value))

        # we expect the current token to be a '+' token
        # or a '-' token
        op = self.current_token
        if op.type == "PLUS":
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input

        right_total = right.value
        while self.current_token.type == "INTEGER":
            right = self.current_token
            self.eat(INTEGER)
            right_total = int(str(right_total)+str(right.value))
        #result = left.value + right.value
        if op.type == "PLUS":
            result = left_total + right_total
        elif op.type == "MINUS":
            result = left_total - right_total

        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text.replace(
            " ", ""))  # trim all white spaces
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()

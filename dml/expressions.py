
import re
from inspect import isclass


# Don't change or delete get_expressions function and Expression
# class if you don't know what you are doing

def get_expressions():
    vars = globals().values()
    classes = filter(isclass, vars)
    expressions = list(filter(
        lambda x: issubclass(x, Expression) and not x.__name__ == 'Expression',
        classes))
    for index, expression in enumerate(expressions):
        expression.type = index
        expression.regexp = re.compile(expression.regexp)
    return expressions


class Expression:
    regexp = ''

    def generator(self, block, function, functions):
        pass

    def build(self, line, function, fname, functions, inner_func=None):
        return function, functions


class Response:
    def __init__(self, type, **kwargs):
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)


# Write your expressions here. See docs/Dev/Expressions.md for more info

class Phrase(Expression):
    regexp = '^.*:.*$'

    def generator(self, block, function, functions):
        # If there's code
        if block[2].startswith('{'):
            return ['eval', block[2][1:-1]]
        response = Response('phrase', author=block[1], text=block[2])
        return ['return', response]

    def process_response(self, block, function, functions, response):
        response = Response('phrase', author=block[1], text=response)
        return response

    def build(self, line, function, fname, functions):
        name, phrase = line.split(':', 1)

        function.append([self.type, name, phrase])
        return function, functions


class Function(Expression):
    regexp = '^fn .*$'

    def build(self, line, function, fname, functions, inner_func=None):
        if not inner_func:
            return function, functions
        # Renaming the function to the name specified in line
        inner_function = functions.pop(inner_func)
        func_name = line.replace('fn', '').strip()
        functions[func_name] = inner_function
        return function, functions


class FunctiuonCall(Expression):
    regexp = r'^.*\(\)$'

    def generator(self, block, function, functions):
        return ['call', block[1]]

    def build(self, line, function, fname, functions):
        function.append([self.type, line[:-2].strip()])
        return function, functions


class IfElifElse(Expression):
    regexp = r'^(if|elif|else).*$'

    def generator(self, block, function, functions):
        self.condition_index = 1
        return ['eval', block[1][2]]

    def process_response(self, block, function, functions, response):
        if response:
            return ['call', block[self.condition_index][1]]
        else:
            # Processing the next condition (elif or else)
            self.condition_index += 1
            try:
                condition = block[self.condition_index]
            except IndexError:
                return None
            if condition[0] == 'elif':
                return ['eval', condition[2]]
            elif condition[0] == 'else':
                return ['call', condition[1]]

    def build(self, line, function, fname, functions, inner_func=None):
        if line.startswith('if'):
            function.append([self.type, ['if', inner_func, line[2:].strip()]])
        elif line.startswith('elif'):
            function[-1].append(['elif', inner_func, line[4:].strip()])
        else:
            function[-1].append(['else', inner_func])
        return function, functions


class Branch(Expression):
    regexp = '^[>|>>].*$'

    def generator(self, block, function, functions):
        response = Response('question', variants=[i[0] for i in block[1:]])
        return ['get_response', response]

    def process_response(self, block, function, functions, response):
        if response.isdecimal():
            func = block[1:][int(response)][1]
        else:
            func = list(filter(lambda x: x[0] == response, block[1:]))[0][1]
        return ['call', func]

    def build(self, line, function, fname, functions, inner_func=None):
        if line.startswith('>>'):
            line = line.replace('>', '').strip()
            function[-1].append([line, inner_func])
        else:
            line = line.replace('>', '').strip()
            function.append([self.type, [line, inner_func]])
        return function, functions


class PythonCode(Expression):
    regexp = r'^\{.*\}$'

    def generator(self, block, function, functions):
        return ['exec', block[1]]

    def build(self, line, function, fname, functions):
        line = line[1:-1].strip()
        function.append([self.type, line])
        return function, functions

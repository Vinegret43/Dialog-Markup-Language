
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


# Write your expressions here. See docs/Dev/Expressions.md for more info

class Phrase(Expression):
    regexp = '^.*:.*$'

    def generator(self, block, function, functions):
        responce = [block[1], block[2]]
        return ['return', ['phrase', *responce]]

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


class IfElifElse(Expression):
    # TODO: cmplete this expression
    regexp = r'^[>|>>][\[.*\]|_]'

    def generator(self, block, function, functions):
        self.condition_index = 0
        return ['eval', block[0][0]]

    def process_responce(self, block, function, functions, responce):
        if responce:
            return ['call', block[self.condition_index][1]]
        # Trying to process the next condition (elif or else)
        else:
            if len(block) == self.condition_index:
                return None
            self.condition_index += 1
            return ''

    def build(self, line, function, fname, functions, inner_func=None):
        type = line.count('>')
        line = line.replace('>', '')[1:-1].strip()
        # TODO: complete code processing
        code = ...  # Compiling and processing the code
        if type == 1:
            function[-1].append([code, inner_func])
        elif type == 2:
            function.append([self.type, [code, inner_func]])
        return function, functions


class Branch(Expression):
    regexp = '^[>|>>].*$'

    def generator(self, block, function, functions):
        return ['get_responce', ['question', [i[0] for i in block[1:]]]]

    def process_responce(self, block, function, functions, responce):
        if responce.isdecimal():
            func = block[1:][int(responce)][1]
        else:
            func = list(filter(lambda x: x[0] == responce, block[1:]))[0][1]
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
        function.append([self.type, compile(line, '', 'exec')])
        return function, functions


class Interpreter:
    '''This is a wrapper for "interpreter" generator. It
    handles StopIteration exception, so you don't  need to
    write try/except in your code, and also it's easier to
    handle vars when using this class'''
    def __init__(self, expressions, dialog, vars=None):
        self.expressions = [i() for i in expressions]
        self.generator = interpreter(self.expressions, dialog, vars)

    def next(self):
        try:
            response = next(self.generator)
        except StopIteration as e:
            self.vars = e
            response = None
        return response

    def send(self, argument):
        self.generator.send(argument)


def interpreter(expressions, dialog, vars=None):
    '''
    This funciton is a generator that iterates through code and
    returns responses from it. Every response is
    a list where first element represents type of response, all
    other elements are body of the response. Type depends on which
    expression block refers to. If you're using stock version
    of DML, you can find documentation for all types in
    docs/Dev/Expressions.md
    '''
    cursor = Cursor('main', dialog)
    while 1:
        block = cursor.next_element()
        if not block:
            return vars
        expression = [i for i in expressions if i.type == block[0]][0]
        response = expression.generator(block, cursor.funcname(), dialog)
        while 1:
            if not response:
                break
            elif response[0] == 'return':
                yield response[1]
                break
            elif response[0] == 'exec':
                exec(response[1])
                break
            elif response[0] == 'call':
                cursor.call(response[1])
                break
            elif response[0] == 'eval':
                result = eval(response[1])
            elif response[0] == 'get_response':
                result = yield response[1]
                yield
            response = expression.process_response(block,
                                                   cursor.funcname(),
                                                   dialog, result)


class Cursor:
    def __init__(self, funcname, functions):
        self.cursor = [[funcname, -1]]
        self.functions = functions

    def funcname(self):
        return self.cursor[-1][0]

    def next(self):
        self.cursor[-1][1] += 1
        return self.cursor[-1]

    def go_up(self):
        self.cursor.pop()

    def call(self, funcname):
        self.cursor.append([funcname, -1])

    def next_element(self):
        cursor = self.next()
        element = None
        while not element:
            try:
                element = self.functions[cursor[0]][cursor[1]]
            except (IndexError, KeyError):
                self.go_up()
                if not self.cursor:
                    return None
                cursor = self.next()
        return element

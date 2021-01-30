
def interpreter(expressions, dialog, vars=None):
    '''
    This funciton is a generator that iterates through code and
    returns responces from it. Every responce is
    a list where first element represents type of responce, all
    other elements are body of the responce. Type depends on which
    expression block refers to. If you're using stock version
    of DML, you can find documentation for all types in
    docs/BuiltInExpressions.md
    '''
    cursor = Cursor('main', dialog)
    while 1:
        block = cursor.next_element()
        if not block:
            return
        expression = [i for i in expressions if i.type == block[0]][0]
        responce = expression.generator(block, cursor.funcname(), dialog)
        while 1:
            if not responce:
                break
            elif responce[0] == 'return':
                yield responce[1]
                break
            elif responce[0] == 'exec':
                exec(responce[1])
                break
            elif responce[0] == 'call':
                cursor.call(responce[1])
                break
            elif responce[0] == 'eval':
                result = eval(responce[1])
            elif responce[0] == 'get_responce':
                result = yield responce[1]
                yield
            responce = expression.process_responce(block,
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

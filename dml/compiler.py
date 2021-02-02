
import os
import re


class Compiler:
    def __init__(self, expressions):
        self.expressions = [i() for i in expressions]

    def build(self, path):
        path = os.path.abspath(path)
        with open(path) as file:
            text = file.read()

        # Removing comments
        text = self.remove_comments(text)
        lines = text.splitlines()

        # Removing empty lines
        lines = list(filter(None, lines))

        # Indenting each line, or [index, text_of_line]
        lines = list(map(self.count_indent, lines))

        # Getting all functions. Result is a dict where keys
        # are function names and values are lists:
        # [text_of_line] or [text_of_line, function_name]
        functions = self.split_on_functions(lines)

        # Compiling every function and line into ready-to-use expressions
        functions = self.process_expressions(functions)

        return functions

    def remove_comments(self, text):
        return re.sub('#.*', '', text)

    def count_indent(self, line):
        return [line.count('|'),
                line.replace('|', '').strip()]

    # This function finds all indented blocks and moves them
    # in a separate function, linking the function name with
    # previous line which indent is 0
    def split_on_functions(self, lines, findex=0):
        # This is the main function (All lines with indent of 0)
        main_func = []
        functions = {}
        # Every line with index 1 or bigger will be added to this list
        # and then added to a funciton when indented block ends
        block = []
        for line in lines:
            # If there's no indentation
            if line[0] == 0:
                if block:
                    fname = '_f' + str(findex)
                    functions[fname] = block
                    # Linking this function with previous 0 indent line
                    main_func[-1].append(fname)
                    findex += 1
                main_func.append(line[1:])
                block = []
            # Line with 1 or more indentation
            else:
                block.append([line[0] - 1, line[1]])
        if block:
            fname = '_f{}'.format(findex)
            functions[fname] = block
            main_func[-1].append(fname)

        # Processing just created functions the same way
        for name, code in functions.items():
            # Getting all subfunctions from this function
            subfuncs = self.split_on_functions(code, findex + 1)
            findexes = [int(i[2:])
                        for i in subfuncs.keys() if i.startswith('_f')]
            if findexes:
                findex = max(findexes)
            # Renaming returned 'main' function
            functions[name] = subfuncs.pop('main')
            functions = {**functions, **subfuncs}
        functions['main'] = main_func
        return functions

    # You can edit expressions in ./expressions.py
    def process_expressions(self, functions):
        processed_functions = {}
        while 1:
            unprocessed_funcs = [i for i in functions
                                 if i not in processed_functions]
            if not unprocessed_funcs:
                break
            # This is the function that it will process
            funcname = unprocessed_funcs[0]
            raw_function = functions[funcname]
            function = []
            for line in raw_function:
                for expression in self.expressions:
                    if expression.regexp.match(line[0]):
                        if len(line) == 2:
                            function, functions = expression.build(
                                     line[0], function, funcname,
                                     functions, line[1]
                            )
                        else:
                            function, functions = expression.build(
                                     line[0], function, funcname, functions
                            )
                        break
                processed_functions[funcname] = function
        return processed_functions

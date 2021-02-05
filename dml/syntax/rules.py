
import re


# Checking for opening/closing brackets and quotes

brackets_stack = {'quote': None,
                  'normal': [],
                  'curly': []}

def brackets_rule(line, indent, index, lines):
    global brackets_stack
    for char_index, char in enumerate(line):
        if char == '"':
            if brackets_stack['quote']:
                brackets_stack['quote'] = None
            else:
                brackets_stack['quote'] = (index, char_index)

        # Checking for brackets
        if not (brackets_stack['quote']
                or brackets_stack['quote']):
            if char == '(':
                brackets_stack['normal'].append((index, char_index))
            elif char == ')':
                if len(brackets_stack['normal']) == 0:
                    text = "Closing bracket doesn't match any opening bracket"
                    return ((index, char_index), line, text)
                else:
                    brackets_stack['normal'].pop()
            if char == '{':
                brackets_stack['curly'].append((index, char_index))
            elif char == '}':
                if len(brackets_stack['curly']) == 0:
                    text = "Closing bracket doesn't match any opening bracket"
                    return ((index, char_index), line, text)
                else:
                    brackets_stack['curly'].pop()

# In the end it checks if some bracket/quote is opened but not closed
def count_brackets_end(lines):
    for type, pos in brackets_stack.items():
        if pos:
            if type == 'quote':
                text = "Quote is opened but not closed"
                return (pos, lines[pos[0]][1], text)
            else:
                text = 'Bracket is opened but not closed'
                return (pos[0], lines[pos[0][0]][1], text)


# Checking for if/elif/else statements

indents = []

def ifelifelse_rule(line, indent, index, lines):
    global indents
    if line.startswith('if'):
        indents.append(indent)
        if not line[2:].strip():
            text = 'Statement not specified after "if"'
            return (index, line, text)
    elif line.startswith('elif'):
        if indent not in indents:
            text = '"elif" is specified, but no "if" specified'
            return (index, line, text)
        if not line[4:].strip():
            text = 'Statement not specified after "elif"'
            return (index, line, text)
    elif line.startswith('else'):
        if indent not in indents:
            text = '"else" is specified, but no "if" specified'
            return (index, line, text)
        if line[4:].strip():
            text = 'Junk after "else" (On the same line)'
            return (index, line, text)
    else:
        indents = list(filter(lambda x: x < indent, indents))


# Checking for branches

branch_indents = []

def branching_rule(line, indent, index, lines):
    global branch_indents
    if line.startswith('>>'):
        if not line[2:].strip():
            text = 'Please specify branch name'
            return (index, line, text)
        if indent not in branch_indents:
            text = 'Branch is outside its block'
            return (index, line, text)
        branch_indents = list(filter(lambda x: x < indent, branch_indents))
    elif line.startswith('>'):
        branch_indents.append(indent)
        if not line[1:].strip():
            text = 'Please specify branch name'
            return (index, line, text)
    else:
        branch_indents = list(filter(lambda x: x < indent, branch_indents))


# Processing functions

functions = []
func_calls = []

def functions_rule(line, indent, index, lines):
    global functions, func_calls
    if line.startswith('fn'):
        fname = line[2:].strip()
        words = len(line.split(' '))
        if indent != 0:
            text = 'Do not specify functions inside other blocks'
            return ((index, 0), line, text)
        elif words == 3:
            text = 'Junk after name of the function'
            return (index, line, text)
        elif words == 1:
            text = 'Please specify name of the function'
            return (index, line, text)
        elif fname in functions:
            text = 'Two functions with the same name'
            return (index, line, text)
        else:
            functions.append(fname)
    elif line.endswith('()') and ':' not in line:
        func_calls.append((index, line[:-2]))

def check_functions_names_end(lines):
    global func_calls, functions
    for line_index, funcname in func_calls:
        if funcname not in functions:
            text = 'There is no function with name {}'.format(funcname)
            return (line_index, lines[line_index][1], text)


# Processing indentation

zero_indent_line = None
previous_indent = 0
regexps = [
    re.compile('^[>|>>].*$'),
    re.compile(r'^(if|elif|else).*$'),
    re.compile('^fn .*$')
]

def indentation_rule(line, indent, index, lines):
    global zero_indent_line, previous_indent, regexps
    if indent == 0:
        zero_indent_line = line
    else:
        if abs(previous_indent - indent) not in (0, 1):
            text = 'Unexpected indented block'
            return (index, line, text)
        if not zero_indent_line:
            text = 'Unexpected indented block'
            return (index, line, text)
        # Checking if indented block is expected
        if not list(filter(lambda r: r.match(zero_indent_line), regexps)):
            text = 'Unexpected indented block'
            return (index, line, text)
    previous_indent = indent


def phrases_rule(line, indent, index, lines):
    if ':' in line:
        colon_index = line.index(':')
        if colon_index == 0:
            text = 'Please specify author of the phrase'
            return ((index, 0), line, text)
        elif colon_index == len(line) - 1:  # If line ends with this colon
            text = 'Please specify the phrase'
            return ((index, colon_index), line, text)

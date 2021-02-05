
from . import rules as rules_module
from .exception import DmlSyntaxError


rules = [getattr(rules_module, i)
         for i in dir(rules_module)
         if i.endswith('_rule')]

end_funcs = [getattr(rules_module, i)
             for i in dir(rules_module)
             if i.endswith('_end')]


# This function recieves splitted lines with indent counted
def check_syntax(lines, filename):
    for index, line in enumerate(lines):
        if not line:  # If line is empty we don't process it
            continue
        for rule in rules:
            error = rule(line[1], line[0], index, lines)
            if error:
                return DmlSyntaxError(filename, *error)
    # Processing end functions
    for func in end_funcs:
        error = func(lines)
        if error:
            return DmlSyntaxError(filename, *error)


from dml import Dml

# Getting an instance of DML
dml = Dml()
# Getting interpreter for the dialog

dialog = dml.get_dialog('examples/example1.dml')

try:
    while 1:
        responce = next(dialog)
        if responce.type == 'question':
            print(responce.variants)
            # Input could be a string with this variant or its index in list
            dialog.send(input())
        elif responce.type == 'phrase':
            print("{}: {}".format(responce.author, responce.text))

# When dialog ends, it will throw StopIteration
except StopIteration:
    print('Dialog Ended!')

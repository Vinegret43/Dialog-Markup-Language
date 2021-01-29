
from dml import Dml
# Getting an instance of DML
dml = Dml()
# Getting interpreter for the dialog

dialog = dml.get_dialog('examples/example1.dml')

try:
    while 1:
        responce = next(dialog)
        if responce[0] == 'question':
            print(responce[1])
            # Input could be a string with this variant or its index in list
            dialog.send(input())
        elif responce[0] == 'phrase':
            print("{}: {}".format(responce[1], responce[2]))

# When dialog ends, it will throw StopIteration
except StopIteration:
    print('Dialog Ended!')

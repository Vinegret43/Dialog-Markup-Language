
from dml import Dml

# Getting an instance of DML
dml = Dml()

# Building all dialogues
dml.build('examples/')

# Getting an interpreter for the dialog
dialog = dml.get_dialog('examples/example1.dml')

# Parsing through the dialog
while 1:
    response = dialog.next()
    # If responce is None, it means that dialog is ended
    if not response:
        break
    if response.type == 'phrase':
        # If it's a phrase, just printing it out
        print("{}: {}".format(response.author, response.text))
    elif response.type == 'question':
        print(response.variants)
        # Input can be a string with this variant or its index in list
        chosen_variant = input()
        dialog.send(chosen_variant)

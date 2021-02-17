
import sys
from dml import Dml

# Getting an instance of DML
dml = Dml()

if len(sys.argv) <= 1:
    exit('Please specify path to the .dml file as an argument')

# Getting an interpreter for the dialog
dialog = dml.get_dialog(sys.argv[1])

# Parsing through the dialog
while 1:
    response = dialog.next()
    # If responce is None, it means that dialog is ended
    if not response:
        break
    if response.type == 'phrase':
        # If it's a phrase, just printing it out
        print("{}: {}".format(response.author, response.text))
        # Waiting for user to hit enter
        input()
    elif response.type == 'question':
        print(response.variants)
        # Input can be a string with this variant or its index in list
        chosen_variant = input()
        dialog.send(chosen_variant)

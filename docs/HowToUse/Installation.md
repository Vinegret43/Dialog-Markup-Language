
# How to integrate DML with your project

You'll need to use dml module. You can get it from [github][0]. Clone the repo
and you'll find dml folder inside the root directory of the repository. This is
the module you're looking for. Copy it to your game directory or in any place
where it can be imported from.
After that create a directory where you will store all your dialogues, i
usually prefer to name it 'dialogues'.

After that you'll need to make ability to compile all dialogues when your
game loads, instead of doing it right before getting the dialog,
entirely stopping your game (This may happen if file is very large)

So before the game actually starts you need to write:

```
from dml import Dml
Dml.build('dialogues/') # Path to directory with your dialogues
```

This will compile all files in this folder and write them to cache, so
when you call ```Dml.get_dialog``` it won't need to compile it,
and it will respond really fast, not freezing your game at all.

After that just import Dml when you need and use it. Create your dialog
files in 'dialogues' directory. You also can create sub folders in this
directory for sorting your dialogues.

To see how to use Dml, dialogues, and Dml.get_dialog method,
see DmlInterface.md doc

[0]: https://github.com/Vinegret43/Dialog-Markup-Language

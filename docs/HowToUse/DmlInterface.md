
# How to use Dml and Interpreter class

P.s. You can see run_from_command_line.py file in root directory of this
repo, it explains everything pretty well.

*****

## Dml (dml.Dml)
This is the main iterface you will be working with. It automatically
imports all expressions, creates a compiler, and etc.

##### \_\_init__(self, vars=None:dict) -> Dml
> **Optional arguments**: vars. vars is a dictionary, and it's made
to be able to access some variables from your dml file. For
example you can type {vars['Some value']} in your dml file.

##### build(self, path:str, recompile=False) -> None
> **Required arguments**: path. This argument specifies path to a file or
folder that you need to compile. If file is specified, it will compile
it if it's not in cache, or do nothing if it's already in cache.
If path to a folder specified, it will recursively compile all
files from it which are not in cache.
**Optional arguments**: recompile. If this argument is True,
it will recompile all dialogues even if they are already in cache.

##### build_file(self, path:str, recompile=False) -> dict(Compiled dialog)
> **Required arguments**: path. This argument specifies path to a file
that you need to compile. It will compile the file if it's not in cache
or get it from cache if it's already there.
**Optional arguments**: recompile. If this argument is True,
it will recompile dialog even if it's already in cache.
**Returns**: Compiled dialog. Compiled dialog is a dictionary. You probably
won't need to use output of this method, so just use build()

##### get_dialog(self, path:str) -> Interpreter
> This is the same as creating an interpreter object from compiled
code and expressions, but this method automates compiling and
importing expressions.
**Required arguments**: path. This argument specifies path to the file
that you need to get interpreter object from. If this file is not
is cache, it will automatically compile it, write to cache and return
and Interpreter object. If it's in cache it'll just get it from there
and return an Interpreter object.
**Returns**: An instance of Interpreter (See doc for this class below)

*****

## Interpreter (dml.interpreter.Interpreter)
This class executes compiled Dml. It processes python code that is written
there, and also returns phrases and questions when it's time to do it.

##### \_\_init__(self, expressions, dialog, vars=None) -> Interpreter
> Dml class from dml.dialog.Dml automatically handles all arguments when
using get_dialog() method, and it's better to use Dml class instead of directly
managing everything.

##### next(self) -> dml.expressions.Response or None
> Get the next element from the dialog. It can be either phrase or a question.
Every response is made from *Response* class. Every response has a
type, all other attributes can change depending on type of the response.
Also this method can return None, it means end of the dialog.
You'll need to process this response in your code, and for example, draw it
on the screen, or ask a question to the player. See more about Response class
below in this file.

##### send(self, argument) -> None
> If there's branch in a dialog, interpreter will send you response with
variants of branches. You can send the branch you choose via this method.
This can be an integer representing number of branch in the list, or you
can send string with name of the branch. After that you need to call
*next()* method to get the next element (phrase/branch).

*****

## Response (dml.expressions.Response)
Every response has a **type**, all other attributes can change depending of
which type it is.
In stock Dml there are two types of responses: 'phrase' and 'question'

##### \_\_init__(self, type:string, **kwargs) -> Response
(Info about this function is useful for developers)
Type is just a type of response, it can be any string. In stock Dml there are
two types: 'phrase' and 'question'. Kwargs are the attributes of response
that you create

### Response(type='phrase')
This type represents a phrase, said by someone. Attributes are:
##### author
> This attribute is a string with the author of the phrase (e.g. who said it)

##### text
> This is the text of the phrase

### Response(type='question')
This type represents a question to a player (e.g. branch in a dialog).
Attributes:
##### variants
>This is list with all available answers. You'll need to send one of those
variants (Or just its index in list) to the interpreter using its *send()*
method, and it will change the dialog depending on what you've sent.

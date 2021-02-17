
# Syntax of the language


## Snippet for programmers:
```yaml
# Comments

# Phrases
Bob: Are You okay?

# Branching
> Yes
  Bob: Good
>> No
  Bob: Why?
  > ...
    ...
  >> ...
    ...

# Python code
{import random}

# if/elif/else statements
if False
  Python: This line will never be executed
elif random.random() > 0.5
  Python: This line will be executed in 50% cases
else
  Python: This line will be executed in other 50% cases

# Functions
fn SayHello
  Player: Hello!

# Function calls
SayHello()
```


## Detail explanation:

### Comments:
```yaml
# Comment
... # Inline comment
```
Sometimes you will probably edit your dialog files, and sometimes
you won't understand what they're about. That's why comments are here. You can
use them to explain something in your dialog for people who will edit it.
This won't affect the actual dialog in your game at all, all comments are
deleted before compilation (Deleted not from your file, but from local copy
  that compiler made)

### Phrases:
```yaml
Author of the phrase: Actual phrase
```
In first part you specify the name of who/what said the phrase, in second part
(Separated by a colon) you specify what he/she/it said, it can be
any text until a newline

### Dialog branching
```yaml
# First block
> First variant
  ... # Here you can write any code
  > 1 # And other branches as well
    ...
  >> 2
    ...
>> Second variant
  ...
>> Third variant
  ...
# Second block
> First variant # Every new block starts with '>' sign
  ...
>> Second variant # All other variants start with '>>'
  ...
```
In other games you've seen that NPC's can ask you some questions, and after that
dialog will change depending on what you've answered. Dialog branching allows
you to do the same thing in your games.

Every new branches block starts with '>' sign. All other branches in this block
start with '>>'. You can write variant of answer after '>' sign (On the same line).
To specify the code that will be in this branch, write it under the branch and start
it with a tab or two spaces. If you have another branch inside a branch, you need to
start code inside it with two tabs (Or four spaces), and etc.

### Python code in your dialog

```yaml
# Code should be inside curly brackets
{ foo = 'bar' }
{ print(foo) }
Python: {'The value of foo is ' + foo }
```

This code executes inside 'interpreter' generator. You can specify variables,
func calls, and etc. There's no variable scope, you can create any variable in
any function of your dialog and access it from anywhere in your dialog. This
type of code is executed with built-in exec() function, not with eval().

You can also use Python code in text of phrase. Code will be executed with eval
and the text of the phrase will be replaced with what your code returned.

### If/Elif/Else statements

```yaml
if some_condition()
  Python: some_conidtion is True
elif another_condition()
  Python: another condition is True, some_condition if False
else
  Python: Both conditions are False
```

This is the same as branching, but it checks conditions automatically, it doesn't
need to ask player for something. While every branch starts with '>' sign, this
expression starts with 'if' or 'elif' or 'else'. After the keyword you can write
any Python expression. It will be executed with eval() function, and if it
returns True, code under this expression will be executed.

'elif' checks for another conditon, if condition that was specified before
returned False. If previous condition returned True, next 'elif' won't be
executed at all.

Code inside 'else' will be executed only if all previous 'if'/'elif' conditions
returned False. You need to write 'else' in the end, after all 'if' and 'elif'
conditions.

You can specify any amount of 'elif' conditions, or don't specify them at all.
'else' is not required too, but you can specify only 1 'else' in each block.

### Funtions

```yaml
# Defining the function
fn myFunc
  Dev: write here whatever you want

# Calling the function
myFunc()

# This will output:
# "Dev: write here whatever you want"
```

Functions are made to organize your code and make it more clear. Every function
starts with 'fn' keyword, and after that keyword you need to specify the name of
the function. Under the function you can write your code (Indenting it with two
spaces or tab). To call the  function write name of the function and brackets after it.

How you can use it:
For example there are two indetical blocks of code in your dialog, and it's not good
when code is repeating twice. So you can make a function, cut and paste this code
in this function, and then replace those blocks of code with just function calls.

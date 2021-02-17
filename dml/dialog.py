
import os
import pickle
from . import expressions
from .compiler import Compiler
from .interpreter import Interpreter
from .caching import write_file, get_file


class Dml:
    def __init__(self, vars=None):
        if vars is None:
            vars = {}
        self.expressions = expressions.get_expressions()
        self.compiler = Compiler(self.expressions)
        self.workdir = None

    # Build the file and write it to cache. You can use this
    # to build everything while your game is loading instead
    # of stopping your game at runtime to build a dialog
    def build(self, path, recompile=False):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        if os.path.isdir(path):
            for path_to_file in os.scandir(path):
                if os.path.isfile(path_to_file):
                    self.build_file(path_to_file, recompile)
                else:
                    self.build(path_to_file, recompile)
        else:
            self.build_file(path, recompile)

    # This method compiles a single file, while 'build' method
    # can compile all files in a folder. However, this method
    # returns compiled result
    def build_file(self, path, recompile=False):
        if self.workdir:
            path = os.path.join(self.workdir, path)
        dialog = get_file(path)
        if dialog is None or recompile:
            dialog = self.compiler.build(path)
            # Saving file to cache
            write_file(path, pickle.dumps(dialog))
        return dialog

    # This function returns an interpreter object for file
    # specified in path. If this object is not in cache,
    # it will automatically build it
    def get_dialog(self, path, vars=None):
        if self.workdir:
            path = os.path.join(self.workdir, path)
        dialog = get_file(path)
        if dialog is None:  # If it's not in cache
            dialog = self.build_file(path)
        else:
            dialog = pickle.loads(dialog)
        return Interpreter(self.expressions, dialog, vars=vars)

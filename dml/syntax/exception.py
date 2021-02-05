
class DmlSyntaxError:
    def __init__(self, filename, position, line, message):
        # Getting line and character from position
        if type(position) is int:
            # Lines counting starts with 0, while most of editors
            # start counting lines from 1. The same with char
            line_number = position + 1
            char = None
        else:
            line_number = position[0] + 1
            char = position[1] + 1
        # Setting attributes
        self._type = 'DmlSyntaxError'
        self._filename = filename
        self._line_number = line_number
        self._char = char
        self._line = line
        self._message = message
        # Making a traceback message
        lines = []
        lines.append('  File {}, line {}'.format(filename, line_number))
        lines.append('    ' + line)
        if char is not None:
            lines.append('    ' + ' ' * (char - 1) + '^')
        lines.append(self._type + ': ' + message)
        self._traceback = '\n'.join(lines)

    @property
    def type(self):
        return type._filename

    @property
    def filename(self):
        return self._filename

    @property
    def position(self):
        if self._char:
            return (self._line_number, self._char)
        else:
            return self._line_number

    @property
    def message(self):
        return self._message

    @property
    def traceback(self):
        return self._traceback

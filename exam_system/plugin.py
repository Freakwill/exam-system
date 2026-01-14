#!/usr/local/bin python3

import re


class Plugin:

    def __init__(self, *functions):
        self.functions = functions

    def __imatmul__(self, cls):
        def t(obj):
            for f in self.functions:
                obj.convert(f)
                obj.template_convert(f)
            return obj

        _old = cls.read_yaml
        def _read_yaml(*args, **kwargs):
            return [t(p) for p in _old(*args, **kwargs)]

        cls.read_yaml = _read_yaml
        return cls

    def __matmul__(self, cls):
        return self.__imatmul__(cls)

    def __rmatmul__(self, cls):
        return self.__matmul__(cls)

    def __iadd__(self, other):
        if isinstance(other, Plugin):
            self.functions += other.functions
        else:
            self.functions += (other,)
        return self

    def __add__(self, other):
        import copy
        self += other
        return copy.deepcopy(self)


def keep(f):

    def _f(text):
        if isinstance(text, str):
            return f(text)
        else:
            return text
    return _f


@Plugin
@keep
def replace_backticks_with_verb(text):
    # Use regular expression to find substrings surrounded by backticks
    pattern = r'`([^`]*)`'
    replaced_text = re.sub(pattern, r'\\verb|\1|', text)
    return replaced_text

@Plugin
@keep
def replace_backticks_with_listing(text):

    # pattern = r"```(\w+)?\n(.*?)\n```"
    pattern = r"```(\w+)?\n((?:.*?\n)*?)```"

    # Define the replacement function
    def replace(match):
        language = match.group(1) or ""
        code = match.group(2)
        if language:
            return f"\\begin{{lstlisting}}[language={language}]\n{code}\n\\end{{lstlisting}}"
        else:
            return f"\\begin{{lstlisting}}\n{code}\n\\end{{lstlisting}}"

    # Perform the regex replacement
    new_text = re.sub(pattern, replace, text)
    return new_text


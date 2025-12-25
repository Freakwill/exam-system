#!/usr/local/bin python3

import re


def keep(f):

    def _f(text):
        if isinstance(text, str):
            return f(text)
        else:
            return text
    return _f


@keep
def replace_backticks_with_verb(text):
    # Use regular expression to find substrings surrounded by backticks
    pattern = r'`([^`]*)`'
    replaced_text = re.sub(pattern, r'\\verb|\1|', text)
    return replaced_text

@keep
def replace_backticks_with_listing(text):

    pattern = r"```(\w+)?\n(.*?)\n```"

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



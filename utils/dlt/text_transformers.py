import re


def sub_hex_numeric(text, rep):
    """
    Substitute all hexadecimal and numeric values following {':', ']'}

    Args:
        text (str): The target text.
        rep (str): The replacement token.

    Returns:
        str: text after substitution
    """
    group_marker = r'((:|])\s)'
    group_match_val = r'\b((0x)?[0-9A-Fa-f]+\b)'
    pattern = group_marker + group_match_val

    return re.sub(pattern, fr'\1{rep}', text)


def sub_perf_counter(text, rep):
    """
    Substitute all performance monitoring values. e.g. 'timeout 1000 ms' 

    Args:
        text (str): The target text.
        rep (str): The replacement token.

    Returns:
        str: text after substitution
    """
    time_units  = ['µs', 'microsecond', 'ms', 'millisecond', 's', 'second', 'times']

    group_match_timer = r'(\d+)'
    group_spaces = r'(\s*)'
    group_time_unit = r'(' + '|'.join(time_units) + r')'
    pattern = group_match_timer + group_spaces + group_time_unit

    return re.sub(pattern, fr'{rep}\2\3', text, flags=re.IGNORECASE)
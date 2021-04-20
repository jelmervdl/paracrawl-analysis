import html
from typing import Generator
from itertools import chain


def first(it, default=None):
    return next(iter(it), default)


def peek(iterable):
    try:
        first = next(iterable)
        return first, chain([first], iterable)
    except StopIteration:
        return None, iter([])

def isgenerator(iterable):
    return hasattr(iterable, '__iter__') and not hasattr(iterable, '__len__')

def isiterable(iterable):
    return hasattr(iterable, '__iter__')

class table:
    def __init__(self, data, *, headers=None, title=None):
        self.data = data
        self.headers = headers
        self.title = title
    
    def _repr_html_val(self, val, headers=None, title=None):
        if val is None:
            return '<em>None</em>'
        elif hasattr(val, '_repr_html_'):
            return val._repr_html_()
        elif isinstance(val, str):
            return html.escape(val)
        elif isinstance(val, (int, float)):
            return str(val)
        elif isiterable(val):
            first_row, rows = peek(iter(val))
            
            if isinstance(first_row, (str, float)):
                rows = map(lambda row: [row], rows)
            
            if headers is None and isinstance(first_row, dict):
                headers = list(first_row.keys())
            
            if headers:
                html_head = ('<th>{}</th>'.format(self._repr_html_val(header)) for header in headers)
            else:
                html_head = ''

            html_rows = (
                '<tr>{}</tr>'.format(''.join(
                    '<td>{}</td>'.format(self._repr_html_val(val))
                    for val in (row.values() if isinstance(row, dict) else row)
                )) for row in rows
            )

            return '<table>{caption}<thead>{head}</thead><tbody>{rows}</tbody></table>'.format(
                caption='<caption>{}</caption>'.format(title) if title else '',
                head='<tr>{}</tr>'.format(''.join(html_head)) if html_head else '',
                rows='\n'.join(html_rows))
        else:
            return html.escape(repr(val))
    
    def _repr_html_(self):
        return self._repr_html_val(self.data, headers=self.headers, title=self.title)
            
        
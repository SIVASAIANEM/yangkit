"""
 import_test_printer.py 
 
 YANG model driven API, python emitter.
"""

import abc
from yang_generator.api_model import Class


class _Stack:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return not self.items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class FilePrinter(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self._start_tab = _Stack()

    def _start_tab_leak_check(self):
        self._start_tab.push(self.ctx.lvl)

    def _check_tab_leak(self):
        end_tab = self.ctx.lvl
        if self._start_tab.pop() != end_tab:
            raise Exception('Tab leak !!!')

    def print_output(self, packages):
        self._start_tab_leak_check()
        self.print_header(packages)
        self.print_body(packages)
        self.print_trailer(packages)
        self._check_tab_leak()

    def print_header(self,packages):
        pass

    @abc.abstractmethod
    def print_body(self, packages):
        pass

    def print_trailer(self, packages):
        pass

    def is_derived_identity(self, package, identity):
        for ne in package.owned_elements:
            if isinstance(ne, Class) and ne.is_identity():
                for ext in ne.extends:
                    if ext == identity:
                        return True
        return False

    def _print_include_guard_header(self, include_guard):
        self.ctx.writeln('#ifndef {0}'.format(include_guard))
        self.ctx.writeln('#define {0}'.format(include_guard))
        self.ctx.bline()

    def _print_include_guard_trailer(self, include_guard):
        self.ctx.bline()
        self.ctx.writeln('#endif /* {0} */'.format(include_guard))

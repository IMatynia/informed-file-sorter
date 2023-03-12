import logging
from copy import deepcopy
from typing import Callable


class ActionHistory:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def add_action_done(self, action: Callable, action_args: list, counter_action: Callable, counter_args: list):
        self._undo_stack.append(
            ((action, deepcopy(action_args)), (counter_action, deepcopy(counter_args)))
        )
        self._redo_stack = []

    def undo_action(self):
        if len(self._undo_stack) == 0:
            logging.info("Nothing to undo")
            return
        action_tuple, counter_tuple = self._undo_stack[-1]
        self._redo_stack.append(self._undo_stack[-1])
        self._undo_stack.pop()
        action_func, action_args = action_tuple
        action_func(*action_args)

    def redo_action(self):
        if len(self._redo_stack) == 0:
            logging.info("Nothing to redo")
            return
        action_tuple, counter_tuple = self._redo_stack[-1]
        self._undo_stack.append(self._redo_stack[-1])
        self._redo_stack.pop()
        counter_func, counter_args = counter_tuple
        counter_func(*counter_args)

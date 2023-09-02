# -*- coding: utf-8 -*-
class DataDiff:
    """DataDiff class."""

    def __init__(self, initial: dict, minus: dict):
        """Initialize DataDiff object."""
        self.initial = initial
        self.minus = minus
        self.diff = self._get_diff(self.initial, self.minus)

    def to_dict(self) -> dict:
        """Convert data difference to dict."""
        return self.diff

    def _get_diff(self, initial, minus) -> dict | list:
        if isinstance(initial, dict):
            return self._get_dict_diff(initial, minus)
        if isinstance(initial, list):
            return self._get_list_diff(initial, minus)

        raise Exception("Only dict and list supported")

    def _get_dict_diff(self, initial: dict, minus: dict) -> dict:
        keys1 = initial.keys()
        items2 = minus.items()
        missing_keys = {i[0]: i[1] for i in items2 if i[0] not in keys1}

        for key, val in initial.items():
            if not isinstance(val, dict | list):
                continue
            diff = self._get_diff(initial.get(key), minus.get(key))
            if not diff:
                continue
            missing_keys[key] = diff

        return missing_keys

    def _get_list_diff(self, initial: list, minus: list) -> list:
        return minus

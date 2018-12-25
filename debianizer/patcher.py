from importlib import import_module
from sys import path
from typing import Dict

__all__ = [
    'SetupMonkeyPatcher',
]


class SetupMonkeyPatcher:
    """
    Patch setuptools.setup to get data as variables.
    """

    def __init__(self, ctx: Dict = None):
        self._context = ctx or {}

    def _get_setup_data(self, **data):
        for key, value in data.items():
            self._context[key] = value

    def _monkeypatch_setuptools(self):
        import setuptools
        setuptools.setup = self._get_setup_data

    def __call__(self, module_path):
        path.append(module_path)
        self._monkeypatch_setuptools()
        import_module('setup')
        return self._context

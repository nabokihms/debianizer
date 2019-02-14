from datetime import datetime
from importlib import import_module
from sys import path, version_info
from typing import Dict

__all__ = [
    'ContextExporter',
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


class ContextExporter:
    """Export variables from setup.py context"""

    def __init__(self, context, venvs_path, message):
        """
        :param context: Dictionary with kwargs from setuptools.setup function
        :param venvs_path: package virtual environment system path
        """
        self._context = context
        self._venvs_path = venvs_path
        self._python_version = 'python{}.{}'.format(*version_info[:2])
        self._snake = '/usr/bin/' + self._python_version
        self._message = message

    @classmethod
    def with_patching(cls, workdir, venvs_path, message):
        patcher = SetupMonkeyPatcher()
        return cls(patcher(workdir), venvs_path, message)

    @property
    def entry_points(self):
        entry_points = self._context.get('entry_points')

        if not entry_points:
            return []

        return [
            script.split(' =')[0]
            for script in entry_points.get('console_scripts', [])
        ]

    @property
    def package_name(self):
        return self._context.get('name', 'Unknown package')

    @property
    def package_version(self):
        return self._context.get('version', '0.0.1')

    @property
    def author(self):
        context = self._context
        return (
            context.get('author')
            or context.get('maintainer')
            or 'Unknown author'
        )

    @property
    def email(self):
        context = self._context
        return (
            context.get('maintainer_email')
            or context.get('author_email')
            or 'uknown@uknown.unknown'
        )

    @property
    def date(self):
        return datetime.now().strftime("%a, %d %b %Y %I:%M:%S")

    @property
    def description(self):
        return self._context.get('description', 'This do something.')

    @property
    def url(self):
        return self._context.get('url', 'no-url.com')

    @property
    def python_version(self):
        return self._python_version

    @property
    def snake(self):
        return self._snake

    @property
    def venvs_path(self):
        return self._venvs_path

    @property
    def message(self):
        return (
            self._message
            or "* Initial release of %s." % self.package_name
        )

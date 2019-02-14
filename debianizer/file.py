from os.path import join

from jinja2 import Environment, PackageLoader, select_autoescape

__all__ = [
    'DebianConfigFactory',
]

_TEMPLATE_PATTERN = '{}.j2'


class DebianConfigFactory:

    def __init__(self, environ, data, dest_path, logger):
        self._environ = environ
        self._data = data
        self._dest_path = dest_path
        self._logger = logger

    @classmethod
    def with_environ(cls, data, dest_path, logger, autoescape=None):
        if autoescape is None:
            autoescape = ['j2']

        return cls(
            Environment(
                loader=PackageLoader('debianizer', 'templates'),
                autoescape=select_autoescape(autoescape),
                keep_trailing_newline=True,
            ),
            data,
            dest_path,
            logger,
        )

    def _write_file(self, path, content):
        with open(path, 'w+') as f:
            f.write(content)
        self._logger.debug(content)
        self._logger.info('File "{}" created.'.format(path))

    def render_template(self, *, source, dest=None):
        if not dest:
            dest = source
        template = self._environ.get_template(_TEMPLATE_PATTERN.format(source))

        self._write_file(
            join(self._dest_path, dest),
            template.render(data=self._data),
        )

    def render_plain_file(self, *, text, dest):
        path = join(self._dest_path, dest)
        self._write_file(path, text)

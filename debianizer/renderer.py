from os import makedirs
from os.path import join, exists, isfile

from debianizer.const import OPTIONS_CONTENT, COMPAT_CONTENT
from debianizer.exc import SetupPyDoesNotFoundError, PathDoesNotExistsError, \
    PathAlreadyExistsError
from debianizer.file import DebianConfigFactory


__all__ = [
    'TemplateRenderer',
]

_BASIC_TEMPLATE_NAMES = ('changelog', 'control', 'rules', 'postinst')


class TemplateRenderer:

    def __init__(self, context_exporter, workdir, venvdir):
        self._workdir = workdir
        self._venvdir = venvdir
        self._context_exporter = context_exporter

    @classmethod
    def with_dir_validation(cls, context_exporter, workdir, venvdir):
        if not exists(workdir):
            raise PathDoesNotExistsError(workdir)

        if not isfile(join(workdir, 'setup.py')):
            raise SetupPyDoesNotFoundError(workdir)

        debian_path = join(workdir, 'debian')
        if exists(debian_path):
            raise PathAlreadyExistsError(debian_path)

        return cls(context_exporter, workdir, venvdir)

    @property
    def _debian_path(self):
        return join(self._workdir, 'debian')

    @property
    def _source_path(self):
        return join(self._debian_path, 'source')

    def _get_config_factory(self, logger):
        return DebianConfigFactory.with_environ(
            self._context_exporter,
            self._debian_path,
            logger
        )

    def __call__(self, update, logger):
        makedirs(self._debian_path, exist_ok=update)
        logger.info('debian folder created.')

        makedirs(self._source_path, exist_ok=update)
        logger.info('debian/source folder created.')

        config_factory = self._get_config_factory(logger)

        for template in _BASIC_TEMPLATE_NAMES:
            config_factory.render_template(source=template)

        config_factory.render_template(
            source='project.triggers',
            dest=self._context_exporter.package_name + '.triggers'
        )

        config_factory.render_plain_file(
            dest='compat',
            text=COMPAT_CONTENT
        )
        config_factory.render_plain_file(
            dest=join('source', 'options'),
            text=OPTIONS_CONTENT
        )

from datetime import datetime
from os import makedirs
from os.path import join, exists, isfile
from sys import version_info

from debianizer.const import OPTIONS_CONTENT, COMPAT_CONTENT
from debianizer.exc import SetupPyDoesNotFoundError, PathDoesNotExistsError, \
    PathAlreadyExistsError
from debianizer.file import DebianConfigFactory
from debianizer.patcher import SetupMonkeyPatcher


__all__ = [
    'export_context',
    'create_debian_folder',
]

_BASIC_TEMPLATE_NAMES = ('changelog', 'control', 'rules', 'postinst')


def export_context(context, venvs_path):
    python_version = 'python{}.{}'.format(*version_info[:2])
    snake = '/usr/bin/' + python_version

    entry_points = context.get('entry_points')
    scripts = []
    if entry_points:
        console_scripts = entry_points.get('console_scripts', '')
        for script in console_scripts:
            scripts.append(script.split(' =')[0])
    return {
        'package_name': context.get('name', 'Unknown package'),
        'package_version': context.get('version', '0.0.1'),
        'author': (
                context.get('author')
                or context.get('maintainer')
                or 'Unknown author'
        ),
        'email': (
                context.get('maintainer_email')
                or context.get('author_email')
                or 'uknown@uknown.unknown'
        ),
        'date': datetime.now().strftime("%a, %d %b %Y %I:%M:%S"),
        'description': context.get('description', 'This do something.'),
        'url': context.get('url', 'no-url.com'),
        'scripts': scripts,
        'python_version': python_version,
        'venvs_path': venvs_path,
        'snake': snake,
    }


def create_debian_folder(workdir, venvdir, logger):
    if not exists(workdir):
        raise PathDoesNotExistsError(workdir)

    if not isfile(join(workdir, 'setup.py')):
        raise SetupPyDoesNotFoundError(workdir)

    debian_path = join(workdir, 'debian')
    if exists(debian_path):
        raise PathAlreadyExistsError(debian_path)

    data = export_context(
        SetupMonkeyPatcher()(workdir),
        venvdir
    )
    logger.info('setup.py data successfully exported.')
    logger.debug(data)

    source_path = join(debian_path, 'source')
    makedirs(debian_path)
    logger.info('debian folder created.')
    makedirs(source_path)
    logger.info('debian/source folder created.')

    config_factory = DebianConfigFactory(data, debian_path, logger)

    for template in _BASIC_TEMPLATE_NAMES:
        config_factory.render_template(source=template)

    config_factory.render_template(source='project.triggers',
                                   dest=data['package_name'] + '.triggers')

    config_factory.render_plain_file(
        dest='compat',
        text=COMPAT_CONTENT
    )
    config_factory.render_plain_file(
        dest=join('source', 'options'),
        text=OPTIONS_CONTENT
    )

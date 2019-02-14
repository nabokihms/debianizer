from logging import basicConfig, getLogger
from os import getcwd

from click import option, command, Choice
from debianizer.patcher import ContextExporter
from debianizer.renderer import TemplateRenderer

__all__ = [
    'run',
]


def _main(workdir, venvdir, update, message, logger):
    context_exporter = ContextExporter.with_patching(
        workdir, venvdir, message
    )
    if not update:
        renderer = TemplateRenderer.with_dir_validation(
            context_exporter, workdir, venvdir
        )
    else:
        renderer = TemplateRenderer(
            context_exporter, workdir, venvdir
        )

    renderer(update, logger)


@command()
@option('-w', '--workdir', default=getcwd(), show_default=True,
        help='Your project directory with setup.py file inside.')
@option('-v', '--venvdir', default='/opt/venvs/',
        help='Directory to save your package virtual environment.')
@option('-u', '--update', show_default=True, is_flag=True,
        help='Update directory files.')
@option('-m', '--message', help='Changelog message.', default=None)
@option('-l', '--loglevel',
        help='Set log level.',
        type=Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
        default='ERROR',
        show_default=True)
def run(workdir, venvdir, update, message, loglevel):
    """
    Command line interface.
    """
    basicConfig(
        level=loglevel,
        format='%(asctime)s : %(levelname)s -- %(message)s'
    )
    logger = getLogger('')

    try:
        _main(workdir, venvdir, update, message, logger)
    except Exception as err:
        logger.exception(err)

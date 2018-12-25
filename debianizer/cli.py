from logging import basicConfig, getLogger
from os import getcwd

from click import option, command, Choice

from debianizer.main import create_debian_folder


@command()
@option('-w', '--workdir', default=getcwd(), show_default=True,
        help='Your project directory with setup.py file inside.')
@option('-v', '--venvdir', default='/opt/venvs/',
        help='Directory to save your package virtual environment.')
@option('-l', '--loglevel',
        help='Set log level.',
        type=Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
        default='ERROR',
        show_default=True)
def run(workdir, venvdir, loglevel):
    """
    Command line interface.
    """
    basicConfig(
        level=loglevel,
        format='%(asctime)s : %(levelname)s -- %(message)s'
    )
    logger = getLogger('')
    try:
        create_debian_folder(workdir, venvdir, logger)
    except Exception as err:
        logger.exception(err)

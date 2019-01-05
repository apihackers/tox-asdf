import logging
import os
import subprocess
import tox


class AsdfError(Exception):
    '''Base ASDF error.'''
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.msg.format(*self.args, **self.kwargs)


class AsdfMissing(AsdfError, RuntimeError):
    '''The asdf program is not installed.'''


class AsdfPluginMissing(AsdfError, RuntimeError):
    '''The asdf python plugin is not installed.'''


class Config(object):
    def __init__(self):
        self.verbose = False
        self.debug = False
        self.no_fallback = False
        self.install = False


CFG = Config()


class ToxLogger:
    def __init__(self, logger):
        self.logger = logger

    def format(self, msg, args, kwargs):
        return 'ASDF: {}'.format(str(msg).format(*args, **kwargs))

    def debug(self, msg, *args, **kwargs):
        if CFG.debug:
            print(self.format(msg, args, kwargs))

    def info(self, msg, *args, **kwargs):
        if CFG.verbose:
            print(self.format(msg, args, kwargs))

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(self.format(msg, args, kwargs))

    def error(self, msg, *args, **kwargs):
        self.logger.error(self.format(msg, args, kwargs))


LOG = ToxLogger(logging.getLogger(__name__))


@tox.hookimpl
def tox_addoption(parser):
    group = parser.argparser.add_argument_group(
        title='tox-asdf plugin options'
    )
    group.add_argument(
        '--asdf-no-fallback',
        dest='asdf_no_fallback',
        default=False,
        action='store_true',
        help=('If `asdf where {basepython}` exits non-zero when looking '
              'up the python executable, do not allow fallback to tox\'s '
              'built-in default logic.')
    )
    group.add_argument(
        '--asdf-install',
        dest='asdf_install',
        default=False,
        action='store_true',
        help=('If `asdf where {basepython}` exits non-zero when looking '
              'up the python executable, do not allow fallback to tox\'s '
              'built-in default logic.')
    )


@tox.hookimpl
def tox_configure(config):
    CFG.verbose = config.option.verbose_level > 0
    CFG.debug = config.option.verbose_level > 1
    CFG.no_fallback = config.option.asdf_no_fallback
    CFG.install = config.option.asdf_install


def best_version(version, versions):
    '''Find the best (latest stable) release matching version'''
    compatibles = (v for v in versions if v.startswith(version))
    return next(iter(sorted(compatibles, reverse=True)), None)


def handle_asdf_error(error):
    if error.returncode == 127:
        raise AsdfMissing('asdf is not installed')
    elif error.returncode == 1 and error.output.startswith('No such plugin:'):
        msg = 'python plugin is missing. Install it with `asdf plugin-add python`'
        raise AsdfPluginMissing(msg)
    if error.output:
        msg = "`{}` failed with code {} and output: \n{}"
    else:
        msg = "`{}` failed with code {}"
    raise AsdfError(msg, error.cmd, error.returncode, (error.output or '').strip())


def asdf_get_installed(version):
    '''Get the best matching installed version'''
    try:
        output = subprocess.check_output('asdf list python',
                                         shell=True,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        handle_asdf_error(e)

    versions = (s.strip() for s in output.splitlines())
    return best_version(version, versions)


def asdf_install(version):
    '''Install the best matching version'''
    try:
        output = subprocess.check_output('asdf list-all python',
                                         shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        handle_asdf_error(e)

    versions = (s.strip() for s in output.splitlines())
    version = best_version(version, versions)

    try:
        subprocess.check_call('asdf install python {}'.format(version), shell=True)
    except subprocess.CalledProcessError as e:
        handle_asdf_error(e)
    return version


def asdf_which(version):
    '''Get the python binary path for a given installed version'''
    try:
        cmd = 'asdf where python {}'.format(version)
        python_home = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT,
                                              universal_newlines=True).strip()
    except subprocess.CalledProcessError as e:
        handle_asdf_error(e)
    return os.path.join(python_home, 'bin', 'python')


@tox.hookimpl
def tox_get_python_executable(envconfig):
    '''
    Return a python executable for the given python base name.

    The first plugin/hook which returns an executable path will determine it.

    ``envconfig`` is the testenv configuration which contains
    per-testenv configuration, notably the ``.envname`` and ``.basepython``
    setting.
    '''
    if envconfig.basepython.startswith('python'):
        expected = envconfig.basepython.replace('python', '', 1)
    elif envconfig.basepython == 'pypy':
        expected = 'pypy2.7'
    elif envconfig.basepython == 'pypy3':
        expected = 'pypy3.5'
    else:
        return

    try:
        version = asdf_get_installed(expected)
    except AsdfError as e:
        LOG.error(e)
        if CFG.no_fallback:
            raise
        return

    if version is None:
        if not CFG.install:
            if CFG.no_fallback:
                raise AsdfError('No candidate version found')
            return
        version = asdf_install(expected)

    if version is None:
        if CFG.no_fallback:
            raise AsdfError('No candidate version to install found')
        return

    try:
        python = asdf_which(version)
    except AsdfError as e:
        LOG.error(e)
        if CFG.no_fallback:
            raise
        return
    else:
        LOG.info('Using {}', python)
    return python

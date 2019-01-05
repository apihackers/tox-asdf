from __future__ import print_function

import pytest

from tox_asdf import plugin


class EnvConfig(object):
    '''A mock envconfig'''
    def __init__(self, basepython='python3.6'):
        self.basepython = basepython


class TestToxGetPythonExecutable:
    @pytest.mark.asdf_missing
    def test_asdf_missing(self, asdf, LOG):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python is None
        LOG.error.assert_called_once()

    @pytest.mark.asdf_python_missing
    def test_asdf_python_plugin_missing(self, asdf, LOG):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python is None
        LOG.error.assert_called_once()

    @pytest.mark.asdf_error(42, 'Unknown error')
    def test_asdf_unknown_error(self, asdf, LOG):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python is None
        LOG.error.assert_called_once()

    @pytest.mark.asdf_error('list', 42, 'Unknown error')
    def test_asdf_list_error(self, asdf, LOG):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python is None
        LOG.error.assert_called_once()

    @pytest.mark.pythons('3.6.0')
    @pytest.mark.asdf_error('where', 42, 'Unknown error')
    def test_asdf_where_error(self, asdf, LOG):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python is None
        LOG.error.assert_called_once()

    def test_basepython_is_not_python(self):
        envconfig = EnvConfig('*TEST*')
        python = plugin.tox_get_python_executable(envconfig)
        assert python is None

    def test_return_none_if_no_python(self, asdf):
        assert plugin.tox_get_python_executable(EnvConfig()) is None

    @pytest.mark.all_pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_install_python_if_no_python_but_flag(self, asdf, CFG):
        CFG.install = True
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python == asdf.python_bin('3.6.0')

    @pytest.mark.all_pythons('2.7.15', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_install_python_but_return_none_if_no_match(self, asdf, CFG):
        CFG.install = True
        assert plugin.tox_get_python_executable(EnvConfig()) is None

    @pytest.mark.pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_return_python_binary_path(self, asdf):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python == asdf.python_bin('3.6.0')

    @pytest.mark.pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_return_pypy_python_binary_path(self, asdf):
        envconfig = EnvConfig('pypy')
        python = plugin.tox_get_python_executable(envconfig)
        assert python == asdf.python_bin('pypy2.7-6.0.0')

    @pytest.mark.pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_return_pypy3_python_binary_path(self, asdf):
        envconfig = EnvConfig('pypy3')
        python = plugin.tox_get_python_executable(envconfig)
        assert python == asdf.python_bin('pypy3.5-6.0.0')


class TestToxGetPythonExecutableNoFallback:
    @pytest.fixture(autouse=True)
    def set_no_fallback(self, CFG):
        CFG.no_fallback = True

    @pytest.mark.asdf_missing
    def test_asdf_missing(self, asdf, LOG):
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())
        LOG.error.assert_called_once()

    @pytest.mark.asdf_python_missing
    def test_asdf_python_plugin_missing(self, asdf, LOG):
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())
        LOG.error.assert_called_once()

    @pytest.mark.asdf_error(42, 'Unknown error')
    def test_asdf_unknown_error(self, asdf, LOG):
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())
        LOG.error.assert_called_once()

    @pytest.mark.asdf_error('list', 42, 'Unknown error')
    def test_asdf_list_error(self, asdf, LOG):
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())
        LOG.error.assert_called_once()

    @pytest.mark.pythons('3.6.0')
    @pytest.mark.asdf_error('where', 42, 'Unknown error')
    def test_asdf_which_error(self, asdf, LOG):
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())
        LOG.error.assert_called_once()

    def test_basepython_is_not_python(self):
        envconfig = EnvConfig('*TEST*')
        assert plugin.tox_get_python_executable(envconfig) is None

    def test_raise_if_no_python(self, asdf):
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())

    @pytest.mark.all_pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_install_python_if_no_python_but_flag(self, asdf, CFG):
        CFG.install = True
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python == asdf.python_bin('3.6.0')

    @pytest.mark.all_pythons('2.7.15', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_install_python_but_raise_if_no_match(self, asdf, CFG):
        CFG.install = True
        with pytest.raises(plugin.AsdfError):
            plugin.tox_get_python_executable(EnvConfig())

    @pytest.mark.pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_return_python_binary_path(self, asdf):
        python = plugin.tox_get_python_executable(EnvConfig())
        assert python == asdf.python_bin('3.6.0')

    @pytest.mark.pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_return_pypy_python_binary_path(self, asdf):
        envconfig = EnvConfig('pypy')
        python = plugin.tox_get_python_executable(envconfig)
        assert python == asdf.python_bin('pypy2.7-6.0.0')

    @pytest.mark.pythons('2.7.15', '3.6.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0')
    def test_return_pypy3_python_binary_path(self, asdf):
        envconfig = EnvConfig('pypy3')
        python = plugin.tox_get_python_executable(envconfig)
        assert python == asdf.python_bin('pypy3.5-6.0.0')

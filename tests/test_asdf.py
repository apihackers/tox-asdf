from __future__ import print_function

import pytest

from tox_asdf import plugin


class TestAsdfGetInstalled:
    @pytest.mark.asdf_missing
    def test_asdf_missing(self, asdf):
        with pytest.raises(plugin.AsdfMissing):
            plugin.asdf_get_installed("3.6")

    @pytest.mark.asdf_python_missing
    def test_asdf_python_plugin_missing(self, asdf):
        with pytest.raises(plugin.AsdfPluginMissing):
            plugin.asdf_get_installed("3.6")

    @pytest.mark.asdf_error(42, "Unknown error")
    def test_unknown_error(self, asdf):
        with pytest.raises(plugin.AsdfError):
            plugin.asdf_get_installed("3.6")

    @pytest.mark.pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_return_python_binary_path(self, asdf):
        assert plugin.asdf_get_installed("3.6") == "3.6.0"

    @pytest.mark.pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_return_pypy_python_binary_path(self, asdf):
        assert plugin.asdf_get_installed("pypy2.7") == "pypy2.7-6.0.0"

    @pytest.mark.pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.5-6.0.0", "pypy3.8-7.0.0")
    def test_return_pypy3_5_python_binary_path(self, asdf):
        assert plugin.asdf_get_installed("pypy3.5") == "pypy3.5-6.0.0"

    @pytest.mark.pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_return_pypy3_python_binary_path(self, asdf):
        assert plugin.asdf_get_installed("pypy3.8") == "pypy3.8-7.0.0"

    @pytest.mark.pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_rely_on_best_version(self, asdf, mocker):
        best_version = mocker.patch.object(plugin, "best_version", return_value="result")
        assert plugin.asdf_get_installed("3.6") == "result"
        best_version.assert_called_once_with("3.6", mocker.ANY)

    def test_return_none_if_no_python(self, asdf):
        assert plugin.asdf_get_installed("3.6") is None


class TestAsdfWhich:
    def test_matching_version(self, asdf):
        assert plugin.asdf_which("3.6.0") == asdf.python_bin("3.6.0")

    @pytest.mark.asdf_error(42, "Unknown error")
    def test_error(self, asdf):
        with pytest.raises(plugin.AsdfError):
            plugin.asdf_which("3.6.0")


class TestAsdfInstall:
    @pytest.mark.asdf_error("list-all", 42, "Unknown error")
    def test_list_all_error(self, asdf):
        with pytest.raises(plugin.AsdfError):
            plugin.asdf_install("3.6")

    @pytest.mark.asdf_error("install", 42, "Unknown error")
    def test_install_error(self, asdf):
        with pytest.raises(plugin.AsdfError):
            plugin.asdf_install("3.6")

    @pytest.mark.all_pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_install_python(self, asdf):
        assert plugin.asdf_install("3.6") == "3.6.0"

    @pytest.mark.all_pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_install_pypy(self, asdf):
        assert plugin.asdf_install("pypy2.7") == "pypy2.7-6.0.0"

    @pytest.mark.all_pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_install_pypy3(self, asdf):
        assert plugin.asdf_install("pypy3") == "pypy3.8-7.0.0"

    @pytest.mark.all_pythons("2.7.15", "3.6.0", "pypy2.7-6.0.0", "pypy3.8-7.0.0")
    def test_rely_on_best_version(self, asdf, mocker):
        best_version = mocker.patch.object(plugin, "best_version", return_value="result")
        assert plugin.asdf_install("3.6") == "result"
        best_version.assert_called_once_with("3.6", mocker.ANY)

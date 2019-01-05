import pytest

from tox_asdf import plugin


def test_only_one_minor():
    versions = '2.7.0', '3.5.0', '3.6.0', '3.7.0'
    version = plugin.best_version('3.6', versions)
    assert version == '3.6.0'


def test_best_patch():
    versions = '2.7.0', '3.5.0', '3.6.0', '3.6.1', '3.6.2', '3.6.3', '3.7.0'
    version = plugin.best_version('3.6', versions)
    assert version == '3.6.3'


def test_multiple_digits():
    versions = '2.7.0', '3.5.0', '3.6.0', '3.6.1', '3.6.10', '3.6.11', '3.7.0'
    version = plugin.best_version('3.6', versions)
    assert version == '3.6.11'


def test_dev_suffix():
    versions = '2.7.0', '3.5.0', '3.6-dev', '3.6.0', '3.7.0'
    version = plugin.best_version('3.6', versions)
    assert version == '3.6.0'


def test_dev_only():
    versions = '2.7.0', '3.5.0', '3.6-dev'
    version = plugin.best_version('3.6', versions)
    assert version == '3.6-dev'


@pytest.mark.parametrize('version', ['2.6', '3.4', '3.8'])
def test_not_found(version):
    versions = '2.7.0', '3.5.0', '3.6.0', '3.6.1', '3.6.2', '3.6.3', '3.7.0'
    assert plugin.best_version('2.6', versions) is None


def test_pypy():
    versions = '2.7.0', '3.6.0', '3.7.0', 'pypy2.7-5.0.0', 'pypy2.7-6.0.0', 'pypy3.5-6.0.0'
    version = plugin.best_version('pypy2.7', versions)
    assert version == 'pypy2.7-6.0.0'


def test_pypy_not_found():
    versions = '2.7.0', '3.6.0', '3.7.0', 'pypy3.5-6.0.0'
    assert plugin.best_version('pypy2.7', versions) is None


def test_pypy3():
    versions = '2.7.0', '3.6.0', '3.7.0', 'pypy2.7-6.0.0', 'pypy3.5-5.0.0', 'pypy3.5-6.0.0'
    version = plugin.best_version('pypy3.5', versions)
    assert version == 'pypy3.5-6.0.0'


def test_pypy3_not_found():
    versions = '2.7.0', '3.6.0', '3.7.0', 'pypy2.7-6.0.0'
    assert plugin.best_version('pypy3.5', versions) is None

import warnings

import pytest

from tox_asdf import plugin


def test_only_one_minor():
    versions = "2.7.0", "3.5.0", "3.6.0", "3.7.0"
    version = plugin.best_version("3.6", versions)
    assert version == "3.6.0"


def test_best_patch():
    versions = "2.7.0", "3.5.0", "3.6.0", "3.6.1", "3.6.2", "3.6.3", "3.7.0"
    version = plugin.best_version("3.6", versions)
    assert version == "3.6.3"


def test_best_patch_not_alphabetical():
    versions = "2.7.9", "2.7.17"
    version = plugin.best_version("2.7", versions)
    assert version == "2.7.17"


def test_multiple_digits():
    versions = "2.7.0", "3.5.0", "3.6.0", "3.6.1", "3.6.10", "3.6.11", "3.7.0"
    version = plugin.best_version("3.6", versions)
    assert version == "3.6.11"


def test_dev_suffix():
    versions = "2.7.0", "3.5.0", "3.6-dev", "3.6.0", "3.7.0"
    version = plugin.best_version("3.6", versions)
    assert version == "3.6.0"


def test_dev_only():
    versions = "2.7.0", "3.5.0", "3.6-dev", "3.7.0", "3.8.0", "3.9.0", "3.10.0", "3.11-dev"
    assert plugin.best_version("3.6", versions) == "3.6-dev"
    assert plugin.best_version("3.11", versions) == "3.11-dev"


@pytest.mark.parametrize("version", ["2.6", "3.4", "3.8"])
def test_not_found(version):
    versions = "2.7.0", "3.5.0", "3.6.0", "3.6.1", "3.6.2", "3.6.3", "3.7.0"
    assert plugin.best_version("2.6", versions) is None


@pytest.mark.parametrize("flavour", plugin.KNOWN_FLAVOURS)
def test_known_flavours(flavour: str):
    best_version = f"{flavour}-3.10.5"
    versions = (
        "2.7.0",
        "3.6.0",
        "3.7.0",
        f"{flavour}-3.1.0",
        f"{flavour}-3.10.0",
        best_version,
    )
    with warnings.catch_warnings():  # Do not rely on LegacyVersion
        warnings.simplefilter("error")
        version = plugin.best_version(flavour, versions)
    assert version == best_version


def test_pypy():
    versions = (
        "2.7.0",
        "3.6.0",
        "3.7.0",
        "pypy2.7-5.0.0",
        "pypy2.7-6.0.0",
        "pypy3.8-7.0.0",
    )
    version = plugin.best_version("pypy2.7", versions)
    assert version == "pypy2.7-6.0.0"


def test_pypy_not_found():
    versions = "2.7.0", "3.6.0", "3.7.0", "pypy3.8-7.0.0"
    assert plugin.best_version("pypy2.7", versions) is None


@pytest.mark.parametrize(
    "version, match",
    [
        ("pypy3", "pypy3.8-7.0.0"),
        ("pypy3.8", "pypy3.8-7.0.0"),
        ("pypy3.5", "pypy3.5-6.0.0"),
    ],
)
def test_pypy3(version, match):
    versions = (
        "2.7.0",
        "3.6.0",
        "3.7.0",
        "pypy2.7-6.0.0",
        "pypy3.5-6.0.0",
        "pypy3.8-6.0.0",
        "pypy3.8-7.0.0",
    )
    best = plugin.best_version(version, versions)
    assert best == match


def test_pypy3_not_found():
    versions = "2.7.0", "3.6.0", "3.7.0", "pypy2.7-6.0.0"
    assert plugin.best_version("pypy3.5", versions) is None

from __future__ import print_function

import tox.session


def init(args):
    config = tox.session.load_config(args)
    return tox.session.build_session(config)


class TestToxOptions:
    def test_default_options(self, CFG):
        init([])
        assert CFG.verbose is False
        assert CFG.debug is False
        assert CFG.install is False
        assert CFG.no_fallback is False

    def test_asdf_no_fallback(self, CFG):
        init(['--asdf-no-fallback'])
        assert CFG.verbose is False
        assert CFG.debug is False
        assert CFG.install is False
        assert CFG.no_fallback is True

    def test_asdf_install(self, CFG):
        init(['--asdf-install'])
        assert CFG.verbose is False
        assert CFG.debug is False
        assert CFG.install is True
        assert CFG.no_fallback is False

    def test_verbose(self, CFG):
        init(['-v'])
        assert CFG.verbose is True
        assert CFG.debug is False
        assert CFG.install is False
        assert CFG.no_fallback is False

    def test_debug(self, CFG):
        init(['-vv'])
        assert CFG.verbose is True
        assert CFG.debug is True
        assert CFG.install is False
        assert CFG.no_fallback is False

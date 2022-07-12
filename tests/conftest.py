import os
import subprocess

import pytest


class MockPopen(object):
    def __init__(self, args):
        self.args = args
        self.returncode = 0
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.pid = None
        self.encoding = None
        self.errors = None

    def communicate(self, input=None):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return self.returncode


class Asdf:
    installs = "/path/to/installs"
    installed = True
    plugin_installed = True
    error_cmd = None
    error_code = None
    error_text = None

    def __init__(self, mocker, pythons, all_pythons=None):
        self.mocker = mocker
        self.pythons = pythons
        self.all_pythons = all_pythons
        self.commands = {
            "list": self.list_python,
            "list-all": self.list_all_python,
            "where": self.where_python,
            "install": self.install_python,
        }

    def python_home(self, python):
        return os.path.join(self.installs, "python", python)

    def python_bin(self, python):
        return os.path.join(self.python_home(python), "bin", "python")

    def popen(self, *args, **kwargs):
        cmd = args[0]
        popen = MockPopen(cmd)
        stdout, stderr, code = "", "", -1

        if isinstance(cmd, str):
            cmd = [p.strip() for p in cmd.split()]
        cmd, args = cmd[0], cmd[1:]

        if self.error_code and self.error_cmd is None:
            code = self.error_code
            stderr = self.error_text
        elif cmd == "asdf" and not self.installed:
            code = 127
        elif cmd == "asdf" and len(args):
            action = args[0]
            command = self.commands.get(action)
            if self.error_cmd and self.error_cmd == action:
                code = self.error_code
                stderr = self.error_text
            elif command:
                stdout, stderr, code = command(*args)
        popen.returncode = code
        if kwargs.get("stderr", None) is subprocess.STDOUT:
            stdout = stdout + stderr
            stderr = None
        popen.communicate = self.mocker.Mock(return_value=(stdout, stderr))
        return popen

    def _asdf_call(self, args, length, output):
        if len(args) < 2:
            return self.invalid_command(*args)
        elif len(args) != length or args[1] != "python":
            return self.invalid_command(*args)
        elif not self.plugin_installed:
            return "", "No such plugin: python", 1
        return output(args), "", 0

    def invalid_command(self, *args):
        cmd = "asdf {}".format(" ".join(args))
        return "", "Invalid asdf command syntax: {}".format(cmd), -1

    def list_python(self, *args):
        return self._asdf_call(args, 2, lambda a: "\n".join(self.pythons))

    def list_all_python(self, *args):
        return self._asdf_call(args, 2, lambda a: "\n".join(self.all_pythons))

    def where_python(self, *args):
        return self._asdf_call(args, 3, lambda a: self.python_home(a[2]))

    def install_python(self, *args):
        return self._asdf_call(args, 3, lambda a: self.python_home(a[2]))


@pytest.fixture(name="asdf")
def mock_asdf(request, mocker):
    marker = request.node.get_closest_marker("pythons")
    pythons = set(marker.args if marker and marker.args else [])

    marker = request.node.get_closest_marker("all_pythons")
    all_pythons = set(marker.args if marker and marker.args else [])

    asdf = Asdf(mocker, pythons, all_pythons)

    marker = request.node.get_closest_marker("asdf_error")
    if marker and marker.args:
        if len(marker.args) == 3:
            asdf.error_cmd, asdf.error_code, asdf.error_text = marker.args
        elif len(marker.args) == 2:
            asdf.error_code, asdf.error_text = marker.args
        elif len(marker.args) == 1:
            asdf.error_code = marker.args[0]
        else:
            msg = "Unknown marker signature asdf_error({})"
            raise ValueError(msg.format(", ".join(marker.args)))
    if request.node.get_closest_marker("asdf_missing"):
        asdf.installed = False
    if request.node.get_closest_marker("asdf_python_missing"):
        asdf.plugin_installed = False
    subprocess.Popen = asdf.popen

    return asdf


@pytest.fixture(name="LOG")
def mock_log(mocker):
    from tox_asdf import plugin

    LOG = mocker.patch.object(plugin, "LOG")
    return LOG


@pytest.fixture(name="CFG")
def mock_cfg(mocker):
    from tox_asdf import plugin

    backup = plugin.CFG
    plugin.CFG = plugin.Config()
    yield plugin.CFG
    plugin.CFG = backup

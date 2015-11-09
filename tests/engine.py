from os import path, system, chdir
from subprocess import check_call, call, PIPE, CalledProcessError
import hitchpython
import hitchtest
import hitchcli


# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class ExecutionEngine(hitchtest.ExecutionEngine):
    """Python engine for running tests."""

    def set_up(self):
        """Set up your applications and the test environment."""
        chdir(PROJECT_DIRECTORY)
        self.cli_steps = hitchcli.CommandLineStepLibrary()

        self.run = self.cli_steps.run
        self.expect = self.cli_steps.expect
        self.send_control = self.cli_steps.send_control
        self.send_line = self.cli_steps.send_line
        self.finish = self.cli_steps.finish

        self.python_package = hitchpython.PythonPackage(
            self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        # Uninstall and reinstall
        call([self.python_package.pip, "uninstall", "dumbyaml", "-y"], stdout=PIPE)
        check_call([self.python_package.python, "setup.py", "install"], stdout=PIPE)

        self.start_python_interpreter()
        self.python_command("import dumbyaml")
        self.python_command("import yaml")


    def start_python_interpreter(self):
        self.run(self.python_package.python)
        self.expect(">>>")

    def python_command(self, command=None, expect=None):
        self.send_line(command)
        if expect is not None:
            self.expect(expect)
        self.expect(">>>")

    def assert_true(self, command):
        self.python_command(command, expect="True")

    def end_python_interpreter(self):
        self.send_control("D")
        self.finish()


    def flake8(self, directory):
        # Silently install flake8
        check_call([self.python_package.pip, "install", "flake8"], stdout=PIPE)
        try:
            check_call([
                path.join(self.python_package.bin_directory, "flake8"),
                directory
            ])
        except CalledProcessError:
            raise RuntimeError("flake8 failure")

    def run_unit_tests(self, directory):
        try:
            check_call([
                path.join(self.python_package.bin_directory, "py.test"),
                "--maxfail=1",
                "-s",
                directory
            ])
        except CalledProcessError:
            raise RuntimeError("py.test failure")

    def tear_down(self):
        try:
            self.end_python_interpreter()
        except:
            pass

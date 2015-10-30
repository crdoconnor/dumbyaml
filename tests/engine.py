from os import path, system, chdir
from subprocess import check_call, call, PIPE, CalledProcessError
import hitchpython
import hitchtest


# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class ExecutionEngine(hitchtest.ExecutionEngine):
    """Python engine for running tests."""

    def set_up(self):
        """Set up your applications and the test environment."""
        self.python_package = hitchpython.PythonPackage(
            self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        chdir(PROJECT_DIRECTORY)

        # Silently install py.test, ipython and flake8
        check_call([self.python_package.pip, "install", "pytest"], stdout=PIPE)
        check_call([self.python_package.pip, "install", "ipython"], stdout=PIPE)
        check_call([self.python_package.pip, "install", "flake8"], stdout=PIPE)

        # Uninstall and reinstall
        call([self.python_package.pip, "uninstall", "dumbyaml", "-y"], stdout=PIPE)
        check_call([self.python_package.python, "setup.py", "install"], stdout=PIPE)

    def flake8(self, directory):
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

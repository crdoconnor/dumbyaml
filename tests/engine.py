from subprocess import check_call, call, PIPE, CalledProcessError
from os import path, system, chdir
import hitchpython
import hitchserve
import hitchtest
import hitchcli
import signal

class IPythonResponse(object):
    """Represent a response from a python command sent to IPython."""
    def __init__(self, returnval=None, text=None, error=None):
        self.returnval = returnval
        self.text = text
        self.error = error

class IPythonStepLibrary(object):
    """Common steps to run commands against embedded IPython."""
    def startup_connection(self, ipykernel_filename):
        import jupyter_client
        self.kernel_manager = jupyter_client.KernelManager(
            connection_file=jupyter_client.find_connection_file(
                ipykernel_filename,
                path=[".", "/run/user/1000/jupyter", "~/.ipython/profile_default/security/", ],
            )
        )
        self.kernel_manager.load_connection_file()
        self.client = self.kernel_manager.blocking_client()
        self.client.start_channels()
        reply = self.client.get_shell_msg()
        
    def run(self, command, silent=False, swallow_exception=False):
        import sys
        if not silent:
            sys.stdout.write(">>> {}".format(command).encode('utf8'))
        self.client.execute(command)
        reply = self.client.get_shell_msg()
        response = IPythonResponse()
        if reply['content']['status'] == 'ok':
            for iopub in self.client.iopub_channel.get_msgs():
                content = iopub['content']
                if "text" in content:
                    if not silent:
                        sys.stdout.write(str(content['text']).encode('utf8'))
                    response.text = content['text']
                if "data" in content:
                    if "text/plain" in content['data']:
                        response.returnval = content['data']['text/plain']
                        if not silent:
                            sys.stdout.write(str("{}\n".format(content['data']['text/plain'])).encode('utf8'))
        elif reply['content']['status'] == 'error':
            response.error = "\n".join(reply['content']['traceback'])
            if not swallow_exception:
                raise RuntimeError("\n".join(reply['content']['traceback']))
            else:
                sys.stderr.write("\n".join(reply['content']['traceback']).encode('utf8'))
        return response
    
    def assert_true(self, command):
        assert self.run(command).returnval == "True"
        
    def assert_result(self, command, result=None):
        assert self.run(command).returnval == result
        
    def assert_output(self, command=None, output=None):
        assert output in self.run(command).error
        
    def assert_exception(self, command=None, exception=None):
        assert exception in self.run(command, swallow_exception=True).error
        
        
    def shutdown_connection(self):
        self.client.shutdown()
        reply = client.get_shell_msg()
        if reply['content']['status'] == 'error':
            raise RuntimeError("Ipython kernel shutdown error")


class PythonService(hitchserve.Service):
    
    def __init__(self, python, module, args, log_line_ready_checker, **kwargs):
        kwargs['command'] = [python, "-u", "-m", module] + args
        kwargs['log_line_ready_checker'] = log_line_ready_checker
        super(PythonService, self).__init__(**kwargs)
        
    def wait_and_get_ipykernel_filename(self, timeout=10):
        kernel_line = self.logs.tail.until(
            lambda line: "--existing" in line[1], timeout=timeout, lines_back=5
        )
        return kernel_line.replace("--existing", "").strip()


class IPythonKernelService(hitchserve.Service):
    """Run an IPython kernel as a service."""
    stop_signal = signal.SIGTERM
    
    def __init__(self, python_package, **kwargs):
        # Check if python < 3.3 and if so, don't run.
        if path.exists(path.join(python_package.bin_directory, "ipython3")):
            ipython = path.join(python_package.bin_directory, "ipython3")
        elif path.join(python_package.bin_directory, "ipython"):
            ipython = path.join(python_package.bin_directory, "ipython")
        else:
            raise RuntimeError("ipython not found in python package")
        kwargs['command'] = [ipython, "kernel", ]
        kwargs['log_line_ready_checker'] = lambda line: "existing" in line
        super(IPythonKernelService, self).__init__(**kwargs)
        
    def wait_and_get_ipykernel_filename(self, timeout=10):
        kernel_line = self.logs.tail.until(
            lambda line: "--existing" in line[1], timeout=timeout, lines_back=5
        )
        return kernel_line.replace("--existing", "").strip()
    

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
        call([self.python_package.pip, "install", "ipython==1.2.1", ], stdout=PIPE)
        call([self.python_package.pip, "install", "pyzmq", ], stdout=PIPE)
        call([self.python_package.pip, "uninstall", "dumbyaml", "-y"], stdout=PIPE)
        check_call([self.python_package.python, "setup.py", "install"], stdout=PIPE)
        
        self.services = hitchserve.ServiceBundle(
            PROJECT_DIRECTORY,
            startup_timeout=8.0,
            shutdown_timeout=1.0
        )
        
        self.services['IPython'] = IPythonKernelService(self.python_package)
        
        self.services.startup(interactive=False)
        self.ipython_kernel_filename = self.services['IPython'].wait_and_get_ipykernel_filename()
        self.ipython_step_library = IPythonStepLibrary()
        self.ipython_step_library.startup_connection(self.ipython_kernel_filename)
        
        self.run_command = self.ipython_step_library.run
        self.assert_true = self.ipython_step_library.assert_true
        self.assert_exception = self.ipython_step_library.assert_exception
        self.shutdown_connection = self.ipython_step_library.shutdown_connection
        self.run_command("import dumbyaml")
        self.run_command("import yaml")

    def on_failure(self):
        if self.settings.get("pause_on_failure", True):
            import sys
            self.services.log(message=self.stacktrace.to_template())
            self.services.start_interactive_mode()
            if path.exists(path.join(
                path.expanduser("~"), ".ipython/profile_default/security/",
                self.ipython_kernel_filename)
            ):
                call([
                        sys.executable, "-m", "IPython", "console",
                        "--existing",
                        path.join(
                            path.expanduser("~"),
                            ".ipython/profile_default/security/",
                            self.ipython_kernel_filename
                        )
                    ])
            else:
                call([
                    sys.executable, "-m", "IPython", "console",
                    "--existing", self.ipython_kernel_filename
                ])
            self.services.stop_interactive_mode()


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
        if hasattr(self, 'services'):
            self.services.shutdown()
        try:
            self.end_python_interpreter()
        except:
            pass

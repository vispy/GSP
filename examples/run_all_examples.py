"""
Run example scripts in this directory sequentially.
It helps testing that all examples run without errors.
"""

from posixpath import basename
import subprocess
import sys
import os
from time import sleep

__dirname__ = os.path.dirname(os.path.abspath(__file__))

def launch_example(cmdline_args: list[str]) -> bool:
    """
    Launches the example script with the given command line arguments.

    Arguments:
        cmdline_args: List of command line arguments to pass to the script.

    Returns:
        True if the script ran successfully, False otherwise.
    """
    try:
        # Add a environment variable to disable interactive mode in the example
        env = dict(**os.environ, GSP_SC_INTERACTIVE="False")

        result = subprocess.run(
            cmdline_args,
            check=True,  # Raises CalledProcessError if script fails
            capture_output=True,
            text=True,  # Capture output as string instead of bytes
            env=env,
        )
        run_success = True if result.returncode == 0 else False

    except subprocess.CalledProcessError as e:
        run_success = False

    return run_success


###############################################################################
# Main script logic
#

def main()->None:
    # NOTE: after launcher.py is merged, this list will be generated automatically
    script_paths = [
        f"{__dirname__}/io_saveload.py",
        f"{__dirname__}/canvas-save.py",
    ]

    for script_path in script_paths:
        # display the basename of the script without new line, and flush the output
        basename_script = basename(script_path)
        print(f"Running {basename_script} ... ", end="", flush=True)

        # launch the example script
        run_success = launch_example([sys.executable, script_path])

        # display X in red if failed, or a check in green if successful
        if run_success:
            print("\033[92mOK\033[0m")  # Green "OK"
        else:
            print("\033[91mFailed\033[0m")  # Red "Failed"

        if not run_success:
            sys.exit(1)


if __name__ == "__main__":
    main()

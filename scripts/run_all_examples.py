"""
Run example scripts in this directory sequentially.
It helps testing that all examples run without errors.
"""

import argparse
import subprocess
import sys
import os

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

def split_argv():
    if '--' not in sys.argv:
        local_args = sys.argv[1:]
        launcher_args = []
    else:
        separator_index = sys.argv.index('--')
        local_args = sys.argv[1:separator_index]
        launcher_args = sys.argv[separator_index + 1:]
    return local_args, launcher_args

def main()->None:
    # Split local args and launcher.py args
    local_args, launcher_args = split_argv()


    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run all example scripts in `./examples` sequentially.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script is useful to check that all example scripts run without exceptions.
        
Usage:
    python scripts/run_all_examples.py [-- <args for example scripts>]

Example:
    # To run all the examples doing a commands cycle of each of them: aka serialize in commands, then deserialize and save the resulting canvas
    python scripts/run_all_examples.py -- commands -cyc

    # To run all the examples to save the canvas to a file in ./examples/output folder 
    python scripts/run_all_examples.py -- matplotlib_image

    # To run all the examples and stop on first error
    python scripts/run_all_examples.py --stop-on-error
    """,
    )
    parser.add_argument("--stop-on-error", action="store_true", help="Stop execution on first error.")
    args = parser.parse_args(local_args)

    examples_folder = f"{__dirname__}/../examples"

    # List all .py files in the examples folder
    basenames = os.listdir(examples_folder)
    basenames = [b for b in basenames if b.endswith(".py")]
    basenames.sort()

    # Construct full paths
    script_paths = [f"{examples_folder}/{basename}" for basename in basenames]

    print(f"Running {len(script_paths)} examples to check if they run without exception...")

    for script_path in script_paths:
        # display the basename of the script without new line, and flush the output
        basename_script = os.path.basename(script_path)
        print(f"Running {basename_script}... ", end="", flush=True)

        # launch the example script
        run_success = launch_example([sys.executable, script_path, *launcher_args])

        # display X in red if failed, or a check in green if successful
        if run_success:
            print("\033[92mOK\033[0m")  # Green "OK"
        else:
            print("\033[91mFailed\033[0m")  # Red "Failed"

        # honor the --stop-on-error flag
        if not run_success and args.stop_on_error:
            sys.exit(1)


if __name__ == "__main__":
    main()

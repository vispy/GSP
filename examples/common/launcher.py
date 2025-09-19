import os
import argparse
import sys

import gsp
import gsp_matplotlib

from .camera import Camera
from gsp.visual.visual import Visual
from typing import Callable


class _ExampleLauncher:

    @staticmethod
    def parse_args(example_description: str | None = None) -> tuple[gsp.core, gsp.visual]:  # type: ignore
        """
        Parse command line arguments and return the appropriate gsp core and visual modules.
        It depends if the user wants to generate a command file or use matplotlib for rendering.

        Args:
            example_description (str | None): Description of the example to show in the inline help message.

        Returns:
            tuple[gsp.core, gsp.visual]: The gsp core and visual modules.
        """

        args = _ExampleLauncher.__parse_args(example_description=example_description)

        if args.command == "commands":
            gsp_core = gsp.core
            gsp_visual = gsp.visual
        elif args.command == "matplotlib_image" or args.command == "matplotlib_camera":
            gsp_core = gsp_matplotlib.core
            gsp_visual = gsp_matplotlib.visual
        else:
            raise ValueError(f"Unknown command: {args.command}")

        # set logging level if specified
        if args.log_level is not None:
            gsp.log.setLevel(args.log_level)

        return gsp_core, gsp_visual

    @staticmethod
    def render(
        canvas: gsp.core.viewport.Canvas,
        viewport: gsp.core.viewport.Viewport|None,
        visuals: list[Visual],
    ) -> None:
        """
        Show the result of the example. Depending on the command line arguments, it can either generate a command file,
        show the image using matplotlib, or use a matplotlib camera to navigate the scene.

        Args:
            canvas (gsp.core.viewport.Canvas): The canvas to show.
            viewport (gsp.core.viewport.Viewport): The viewport to show.
            visuals (list[Visual]): The list of visuals to render.
        """

        args = _ExampleLauncher.__parse_args()

        # get the __file__ of the calling script
        example_filename = getattr(sys.modules.get("__main__"), "__file__", None)

        # Extract example basename and directory
        example_basename = os.path.basename(example_filename).replace(".py", "")
        __dirname__ = os.path.dirname(os.path.abspath(example_filename))

        if args.command == "commands":

            print(
                "Command file generation trigger exception at the moment, it depends on https://github.com/vispy/GSP/issues/14 ."
            )

            commands_filename = f"{__dirname__}/output/{example_basename}.commands.json"
            gsp.save(commands_filename)
            print(f"Commands saved to {commands_filename}")

            # Re-load commands and re-execute them
            if args.command_file_cycle == True:

                # reset objects - TODO make it cleaner - call a function e.g. .clear() ?
                gsp.Object.objects = {}

                # gsp.Object.clear()

                # load commands from file
                command_queue = gsp.io.json.load(commands_filename)

                for command in command_queue:
                    gsp.log.info("%s" % command)

                # KEY: REQUIRED FOR THE GLOBALS - Super dirty!!!
                # gsp.use("matplotlib")

                # TODO send matplotlib as namespace in command_queue.run
                command_queue.run(globals(), locals())

                import matplotlib.pyplot as plt

                plt.show(block=True)
        elif args.command == "matplotlib_image":
            import matplotlib.pyplot as plt

            # save a screenshot of the rendered canvas
            image_filename = f"{__dirname__}/output/{example_basename}.png"
            plt.savefig(image_filename)

            print(f"Image saved to {image_filename}")
        elif args.command == "matplotlib_camera":
            camera = Camera(mode=args.camera_mode)
            for _visual in visuals:
                camera.connect(viewport, "motion", _visual.render)
            camera.run()
        else:
            print(f"Unknown command: {args.command}")

    @staticmethod
    def __parse_args(example_description: str | None = None) -> argparse.Namespace:
        """
        Parse command line arguments.
        """

        # If no description is provided, get one based on the calling script name
        if example_description is None:
            example_filename = getattr(sys.modules.get("__main__"), "__file__", None)
            example_basename = os.path.basename(example_filename).replace(".py", "")
            example_description = f"Example using GSP called {example_basename}."

        # define the command line arguments
        argument_parser = argparse.ArgumentParser(
            description=example_description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        argument_parser.add_argument(
            "command",
            nargs="?",
            help="Define the command to execute. 'commands' will generate a command file. 'matplotlib_image' will show the image using matplotlib. 'matplotlib_camera' will use a matplotlib camera to navigate the scene.",
            choices=["commands", "matplotlib_image", "matplotlib_camera"],
            default="matplotlib_camera",
        )
        argument_parser.add_argument(
            "-c",
            "--camera_mode",
            help="Define the matplotlib camera mode. Valid IIF the command is 'matplotlib_camera'.",
            choices=["ortho", "perspective"],
            default="perspective",
        )
        argument_parser.add_argument(
            "-cyc",
            "--command_file_cycle",
            help="If true, after generating a command file, it will be re-loaded and executed.",
            action="store_true",
        )
        argument_parser.add_argument(
            "-l",
            "--log_level",
            help="Set the logging level for `GSP.log()` .",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            default=None,
        )

        # parse the arguments
        args = argument_parser.parse_args()

        return args
    

def parse_args(
    example_description: str | None = None,
) -> tuple[
    gsp.core,   # type: ignore
    gsp.visual, # type: ignore
    Callable[
        [gsp.core.viewport.Canvas, list[gsp.core.viewport.Viewport], list[Visual]], None
    ],
]:
    """
    Parse command line arguments and return the appropriate gsp core and visual modules.
    It returns also a function to render the result of the example.

    It depends if the user wants to generate a command file or use matplotlib for rendering.

    Args:
        example_description (str | None): Description of the example to show in the inline help message

    Returns:
        tuple[gsp.core, gsp.visual, Callable]: The gsp core and visual modules, and a function to render the result of the example.
    """
    core, visual = _ExampleLauncher.parse_args(example_description=example_description)

    def render_func(
        canvas: gsp.core.viewport.Canvas,
        viewports: list[gsp.core.viewport.Viewport],
        visuals: list[Visual],
    ) -> None:
        # FIXME run all the viewports, for now just the first one
        
        first_viewport = viewports[0] if len(viewports) > 0 else None
        _ExampleLauncher.render(canvas, first_viewport, visuals)

    return core, visual, render_func

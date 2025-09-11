import os
import gsp
import argparse
import sys

from .camera import Camera
from gsp.visual.visual import Visual

class ExampleArgsParse:

    @staticmethod
    def parse(example_description: str | None = None) -> tuple:
        """
        Parse command line arguments and return the appropriate gsp core and visual modules.
        It depends if the user wants to generate a command file or use matplotlib for rendering.

        Args:
            example_description (str | None): Description of the example to show in the help message.
        """

        args = ExampleArgsParse.__parse_args(example_description=example_description)

        if args.command == "command_file":
            gsp_core = gsp.core
            gsp_visual = gsp.visual
        elif (
            args.command == "matplotlib_image"
            or args.command == "matplotlib_camera"
        ):
            gsp_core = gsp.matplotlib.core
            gsp_visual = gsp.matplotlib.visual
        else:
            raise ValueError(f"Unknown command: {args.command}")

        # set logging level if specified
        if args.log_level is not None:
            gsp.log.setLevel(args.log_level)

        return gsp_core, gsp_visual

    @staticmethod
    def show(
        canvas: gsp.core.viewport.Canvas,
        viewport: gsp.core.viewport.Viewport,
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

        args = ExampleArgsParse.__parse_args()

        # get the __file__ of the calling script
        example_filename = getattr(sys.modules.get("__main__"), "__file__", None)

        # Extract example basename and directory
        example_basename = os.path.basename(example_filename).replace(".py", "")
        __dirname__ = os.path.dirname(os.path.abspath(example_filename))

        if args.command == "command_file":

            print("Command file generation trigger exception at the moment, it depends on https://github.com/vispy/GSP/issues/14 .")

            commands_filename = f"{__dirname__}/output/{example_basename}.commands.json"
            gsp.save(commands_filename)
            print(f"Commands saved to {commands_filename}")

            # Re-load commands and re-execute them
            if args.command_file_cycle == True:

                # reset objects - TODO make it cleaner - call a function e.g. .clear() ?
                gsp.Object.objects = {}

                # load commands from file
                command_queue = gsp.io.json.load(commands_filename)

                for command in command_queue:
                    gsp.log.info("%s" % command)

                # KEY: REQUIRED FOR THE GLOBALS - Super dirty!!!
                gsp.use("matplotlib")

                # TODO send matplotlib as namespace in command_queue.run
                command_queue.run(globals(), locals())
                # print(f"object: {gsp.Object.objects[1]}")

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

        # If no description is provided, get one based on the calling script name
        if example_description is None:
            example_filename = getattr(sys.modules.get("__main__"), "__file__", None)
            example_basename = os.path.basename(example_filename).replace(".py", "")
            example_description = f"Example using GSP called {example_basename}."

        # define the command line arguments
        arg_parser = argparse.ArgumentParser(
            description=example_description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        arg_parser.add_argument(
            "command",
            nargs="?",
            help="Define the command to execute. 'command_file' will generate a command file. 'matplotlib_image' will show the image using matplotlib. 'matplotlib_camera' will use a matplotlib camera to navigate the scene.",
            choices=["command_file", "matplotlib_image", "matplotlib_camera"],
            default="matplotlib_camera",
        )
        arg_parser.add_argument(
            "-c",
            "--camera_mode",
            help="Define the matplotlib camera mode. Valid IIF the command is 'matplotlib_camera'.",
            choices=["ortho", "perspective"],
            default="perspective",
        )
        arg_parser.add_argument(
            "-cyc",
            "--command_file_cycle",
            help="If true, after generating a command file, it will be re-loaded and executed.",
            action="store_true",
        )
        arg_parser.add_argument(
            "-l",
            "--log_level",
            help="Set the logging level for `GSP.log()` .",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            default=None,
        )

        # parse the arguments
        args = arg_parser.parse_args()

        return args
from argparse import ArgumentParser


def get_arg_parser(description: str = "Morty") -> ArgumentParser:
    """
    Get ArgumentParser with morty-related arguments
    """
    parser = ArgumentParser(add_help=False, description=description)

    parser.add_argument(
        "--config-path",
        "-cp",
        help="""Overrides the 'path' specified in @morty.config.config().
                    The 'path' is relative to the Python file declaring @morty.config.config()""",
    )

    parser.add_argument(
        "--config-name",
        "-cn",
        help="Overrides the 'name' specified in @morty.config.config()",
    )

    return parser

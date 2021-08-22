from argparse import ArgumentParser


def get_arg_parser(description: str = "Morty") -> ArgumentParser:
    """
    Get ArgumentParser with morty-related arguments
    """
    parser = ArgumentParser(add_help=False, description=description)

    parser.add_argument(
        "--config-path",
        "-cp",
        help="""Overrides the config_path specified in morty.config.main().
                    The config_path is relative to the Python file declaring @morty.config.main()""",
    )

    parser.add_argument(
        "--config-name",
        "-cn",
        help="Overrides the config_name specified in morty.config.main()",
    )

    return parser

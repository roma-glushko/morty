from morty.config import get_arg_parser


def test__args_parser__morty_options():
    arg_parser = get_arg_parser()

    args = arg_parser.parse_args([])

    assert "config_name" in args
    assert "config_path" in args

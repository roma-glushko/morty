from os import PathLike
from pathlib import Path

from flask import Flask


def create_backend_app() -> Flask:
    static_dir: PathLike = (Path(__file__) / ".." / ".." / "frontend" / "build").resolve()

    app = Flask(
        __name__,
        static_folder=static_dir,
        static_url_path="/",
    )

    @app.route("/", methods=["GET"])
    def index():
        return app.send_static_file("index.html")

    return app


__all__ = ("create_backend_app",)

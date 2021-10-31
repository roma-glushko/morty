from os import PathLike
from pathlib import Path

from flask import Flask


def create_backend_app() -> Flask:
    static_dir: PathLike = (
        Path(__file__) / ".." / ".." / "frontend" / "build"
    ).resolve()

    app = Flask(
        __name__,
        static_folder=static_dir,
        static_url_path="/",
    )

    @app.route("/", methods=["GET"])
    def index():
        return app.send_static_file("index.html")

    @app.route("/experiments", methods=["GET"])
    def experiments():
        return {
            "inspiring_hypatia": {
                "data": {
                    "accuracy": {
                        "max": 0.9738147854804993,
                        "mean": 0.9430185159047445,
                        "min": 0.8892407417297363,
                    },
                    "batch_size": 128,
                    "config_file": "configs/basic_config",
                    "config_name": None,
                    "config_path": None,
                    "created_at": "2021-10-31T15:06:30.899410+00:00",
                    "epoch": {"max": 2.0, "mean": 1.0, "min": 0.0},
                    "epochs": 3,
                    "experiment_id": "inspiring_hypatia",
                    "image_shape": [28, 28, 1],
                    "loss": {
                        "max": 0.3600384593009949,
                        "mean": 0.1856200397014618,
                        "min": 0.08564602583646774,
                    },
                    "num_classes": 10,
                    "optimizer": "adam",
                    "optimizer_configs.learning_rate": 0.0001,
                    "train_runs": ["2021-10-31T15:06:31.489994"],
                    "val_accuracy": {
                        "max": 0.9883333444595337,
                        "mean": 0.9851666688919067,
                        "min": 0.9810000061988831,
                    },
                    "val_dataset_fraction": 0.1,
                    "val_loss": {
                        "max": 0.07788745313882828,
                        "mean": 0.059153748055299125,
                        "min": 0.045631732791662216,
                    },
                },
                "last_updated_at": "2021-10-31T15:06:31.489994",
            }
        }

    return app


__all__ = ("create_backend_app",)

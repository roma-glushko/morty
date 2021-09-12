from pathlib import Path

config_content: str = """
args = {
    "num_classes": 10,
    "image_shape": (28, 28, 1),
    "val_dataset_fraction": 0.1,
    "epochs": 15,
    "batch_size": 128,
    "optimizer": "adam",
    "optimizer_configs": {
        "learning_rate": 1e-4,
    },
}
"""


def create_config_file(path: Path, filename: str):
    path.mkdir(parents=True, exist_ok=True)

    with open(path / filename, "w") as config_file:
        config_file.writelines(config_content)

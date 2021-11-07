class IndexWarning(UserWarning):
    pass


class GitLibNotInstalled(ModuleNotFoundError):
    pass


class TensorflowNotInstalled(ModuleNotFoundError):
    pass

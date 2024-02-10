def __get_runtime_version():
    import importlib.metadata

    try:
        return importlib.metadata.version("realm")
    except importlib.metadata.PackageNotFoundError:
        return None


__version__ = __get_runtime_version()

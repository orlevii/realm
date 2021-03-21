def __get_runtime_version():
    from pkg_resources import get_distribution
    realm = get_distribution('realm')
    return realm.version


__version__ = __get_runtime_version()

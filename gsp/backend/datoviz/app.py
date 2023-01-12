from datoviz import App

_APP = None


def default_app():
    global _APP
    if not _APP:
        _APP = App()
    assert _APP
    return _APP

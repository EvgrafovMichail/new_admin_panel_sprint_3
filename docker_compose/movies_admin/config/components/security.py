import os


SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


def _show_toolbar_callback(*_) -> bool:
    return DEBUG


SHOW_TOOLBAR_CALLBACK = _show_toolbar_callback

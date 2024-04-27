import os


SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = [f"http://{host}:8000" for host in ALLOWED_HOSTS]


def _show_toolbar_callback(*_) -> bool:
    return DEBUG


SHOW_TOOLBAR_CALLBACK = _show_toolbar_callback

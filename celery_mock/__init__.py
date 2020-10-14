# -*- coding: utf-8 -*-
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)
__author__ = """Konrad Rotkiewicz"""
__email__ = 'konrad@ulam.io'

from .celery_mock import task_mock  # noqa

import re
from importlib import import_module

from . import settings
from .restreamers.base import BaseRestreamer
from bot_controller import BotController


class RestreamerDispatcherException(Exception): pass


class RestreamerDispatcher:
    @staticmethod
    def get_restreamer_class(func_name, args):
        if func_name in [method for method in dir(BaseRestreamer) if not method.startswith('_')]:
            for service_identifier in settings.SERVICE_URL_IDENTIFIERS:
                if service_identifier in args[0]:
                    service_name = settings.SERVICE_URL_IDENTIFIERS[service_identifier]
                    break
            else:
                raise RestreamerDispatcherException('Can\'t determine appropriate restreamer')

            return getattr(import_module(f'music_sources.restreamers.{service_name}.restreamer'), 'Restreamer')

        if func_name in [method for method in dir(BotController) if not method.startswith('_')]:
            return BotController

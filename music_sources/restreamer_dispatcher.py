import re
from importlib import import_module

from . import settings
from .restreamers.base import BaseRestreamer
from bot_controller import BotController


class RestreamerDispatcher:
    def __init__(self):
        self.__url_pattern = re.compile(settings.URL_PATTERN)

    def get_restreamer_class(self, *args):
        if not any(args):
            return BotController

        try:
            service_name = self.__url_pattern.match(args[0]).group(settings.URL_TARGET_GROUP_NAME)
            return getattr(import_module(f'music_sources.restreamers.{service_name}.restreamer'), 'Restreamer')
        except Exception as e:
            raise settings.RestreamerDispatcherException('Can\'t determine appropriate restreamer')

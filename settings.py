from music_sources.restreamers.base import BaseRestreamer
from bot_controller import BotController

SPLIT_CHAR = ' '

# {<Recognizable_command>: (<BaseRestreamer_method_name>, (<arg1_type>, <arg2_type>)), ...}
COMMANDS_MAP = {
    '-p':       (BaseRestreamer.play.__name__, (str,)),
    '-play':    (BaseRestreamer.play.__name__, (str,)),
    '-s':       (BotController.stop.__name__, (None,)),
    '-stop':    (BotController.stop.__name__, (None,)),
    '-n':       (BotController.next.__name__, (None,)),
    '-next':    (BotController.next.__name__, (None,)),
    '-e':       (BotController.exit.__name__, (None,)),
    '-exit':    (BotController.exit.__name__, (None,)),
    '-q':       (BotController.queue.__name__, (None,)),
    '-queue':   (BotController.queue.__name__, (None,)),
    '-j':       (BotController.jump.__name__, (int,)),
    '-jump':    (BotController.jump.__name__, (int,)),
}

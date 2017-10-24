import ctypes
import os
import platform
import re
import subprocess
from datetime import datetime
import psutil

from nio.block.base import Block
from nio.command import command
from nio.properties.bool import BoolProperty
from nio.properties.holder import PropertyHolder
from nio.properties.object import ObjectProperty
from nio.properties.version import VersionProperty
from nio.signal.base import Signal

#RETRY_LIMIT = 3


class Menu(PropertyHolder):
    machine = BoolProperty(title='Hardware Architecture', default=False)
    os_version = BoolProperty(title='OS Version', default=False)
    platform = BoolProperty(title='Hardware Platform', default=False)
    dist = BoolProperty(title='OS Distribution', default=False)
    system = BoolProperty(title='OS Type', default=True)
    python = BoolProperty(title='Python Information', default=False)
    processor = BoolProperty(title='Processor Type', default=False)
    hostname = BoolProperty(title='Hostname', default=False)


class HostSpecs(Block):

    version = VersionProperty("0.1.0")
    menu = ObjectProperty(Menu, title='Menu', default=Menu())

    def __init__(self):
        super().__init__()
        self._retry_count = 0

    def process_signals(self, signals):
        plat = self.platform()
        self.notify_signals([Signal(plat)])

    def platform(self):
        '''Returns platform data
        '''
        keys = []
        out = {}

        if self.menu().machine():
            keys.append('machine')
        if self.menu().os_version():
            keys.append('version')
        if self.menu().platform():
            keys.append('platform')
        if self.menu().dist():
            keys.append('dist')
        if self.menu().system():
            keys.append('system')
        if self.menu().hostname():
            keys.append('node')
        if len(keys) > 0:
            out = {key: getattr(platform, key)() for key in tuple(keys)}
        self.logger.error(out)
        if self.menu().python():
            out['python'] = {key: getattr(platform, "python_" + key)() for
                             key in ('implementation', 'compiler', 'version')}
            out['python']['architecture'] = \
                int(ctypes.sizeof(ctypes.c_voidp) * 8)
        if self.menu().processor():
            out['processor'] = self._get_processor()
            out['cores'] = len(psutil.cpu_percent(percpu=True))

        return out

    def _get_processor(self):
        '''Get type of processor
        http://stackoverflow.com/questions/4842448/
        getting-processor-information-in-python
        '''
        out = None
        if platform.system() == "Windows":
            out = platform.processor()
        elif platform.system() == "Darwin":
            path = os.environ['PATH']
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            try:
                command = "sysctl -n machdep.cpu.brand_string"
                out = subprocess.check_output(command, shell=True)\
                    .strip().decode()
            finally:
                os.environ['PATH'] = path
        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True)\
                .strip().decode()
            for line in all_info.split("\n"):
                if "model name" in line:
                    out = re.sub(".*model name.*:", "", line, 1)

        if out is None:
            return platform.processor()
        else:
            return out

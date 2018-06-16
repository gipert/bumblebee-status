# pylint: disable=C0111,R0903

"""Displays a little icon if Docker daemon is running
"""

import os
import functools
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.docker))
        self.is_running = -1
        self.is_running = os.popen("ps -aef | grep -i 'dockerd' | grep -v 'grep' | awk '{ print $3 }'").read() != ''

        immediate_update = functools.partial(self.update, immediate=True)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=immediate_update)

    def docker(self, _):
        if self.is_running:
            return 'up'
        else:
            return 'down'

    def update(self, _, immediate=False):
        try:
            self.is_running = os.popen("ps -aef | grep -i 'dockerd' | grep -v 'grep' | awk '{ print $3 }'").read() != ''
        except Exception:
            self.is_running = -1

    def state(self, _):
        if not self.is_running:
            return "down"
        else:
            return "up"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

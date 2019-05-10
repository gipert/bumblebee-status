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
            bumblebee.output.Widget(full_text=self.ncmpcpp))
        self.song = os.popen("ncmpcpp --now-playing \"{{{{%a - }%t}}|{%f}}\"").read().rstrip()

        immediate_update = functools.partial(self.update, immediate=True)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=immediate_update)

    def ncmpcpp(self, _):
        return self.song

    def update(self, _, immediate=False):
        try:
            self.song = os.popen("ncmpcpp --now-playing \"{{{{%a - }%t}}|{%f}}\"").read().rstrip()
        except Exception:
            self.song = "n/a"

    def state(self, _):
        if self.song == "n/a":
            return "critical"
        elif self.song == "":
            return "stopped"
        else:
            return "warning"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

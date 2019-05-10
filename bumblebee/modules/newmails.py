# pylint: disable=C0111,R0903

"""Displays unread emails.

Parameters:
    * newmails.shortname  : a short alias to be displayed
    * newmails.imapserver : e.g. imap.gmail.com
    * newmails.user       : your username, some accounts want the complete user@domain
    * newmails.password   : your password (maybe 'chmod og-rwx bumblebee-status.conf' then)
"""

import imaplib
import functools
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.newmails))

        try:
            mail = imaplib.IMAP4_SSL(self.parameter("imapserver", ""))
            mail.login(self.parameter("user", ""), self.parameter("password", ""))
            mail.select("inbox", True) # connect to inbox.
            return_code, mail_ids = mail.search(None, 'UnSeen')
            self._count = len(mail_ids[0].split(" "))
            if len(mail_ids[0].split(" ")) == 1 and mail_ids[0].split(" ")[0] == '':
                self._count = 0
        except:
            self._count = 'n/a'

        immediate_update = functools.partial(self.update, immediate=True)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=immediate_update)

    def newmails(self, _):
        return self.parameter("shortname", "") + ' ' + str(self._count)

    def update(self, _, immediate=False):
        try:
            mail = imaplib.IMAP4_SSL(self.parameter("imapserver", ""))
            mail.login(self.parameter("user", ""), self.parameter("password", ""))
            mail.select("inbox", True) # connect to inbox.
            return_code, mail_ids = mail.search(None, 'UnSeen')
            self._count = len(mail_ids[0].split(" "))
            if len(mail_ids[0].split(" ")) == 1 and mail_ids[0].split(" ")[0] == '':
                self._count = 0
        except:
            self._count = 'n/a'

    def state(self, _):
        if self._count == 'n/a':
            return "critical"
        elif self._count != 0:
            return "warning"
        else:
            return "NONEW"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

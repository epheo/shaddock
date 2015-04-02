import logging
import os

from cliff.lister import Lister
from panama import backend, model

class Containers(Lister):
    """Show a list of Containers.
    The 'Name', 'Created', 'Started', 'IP', 'Tag', 'Docker-id' are printed by default.
    """

    log = logging.getLogger(__name__)


    def take_action(self, parsed_args):
        cf = model.ConfigFile()
        columns = ('Name', 'Created', 'Started', 'IP', 'Tag', 'Docker-id')
        l = ()
        for n in cf.services_keys:
            b = backend.Container(n)
            line = (n, b.created, b.started, b.ip, b.tag, b.id)
            l = l + (line, )
        return columns, l
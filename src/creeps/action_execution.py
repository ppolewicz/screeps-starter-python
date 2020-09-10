from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class ActionExecution:
    def __init__(self, creep, method, *args, **kwargs):
        self.creep = creep
        self.priority = kwargs[priority]
        self.method = method
        self.args = args
    def run(self):
        result = self.method(creep, *args)
        if result != OK:
            print("[{}] Unknown result from creep.{}({}): {}".format(creep.name, self.method.__name__, source, result))
    def build(self, creep, target):
        return creep.build(target)
    def harvest(self, creep, target):
        return creep.harvest(target)
    def moveTo(self, creep, target):
        return creep.moveTo(target)
    def upgradeController(self, creep, target):
        return creep.upgradeController(target)

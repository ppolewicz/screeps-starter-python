from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from utils import ERRORS


class ActionExecution:
    def __init__(self, creep, method, *args, priority=100, on_error=None):
        self.creep = creep
        self.priority = priority
        self.method = method
        self.args = args
        self.on_error = args[1].on_error
    def run(self):
        if self.method == 'build':
            result = self.build()
        elif self.method == 'harvest':
            result = self.harvest()
        elif self.method == 'moveTo':
            result = self.moveTo()
        elif self.method == 'upgradeController':
            result = self.upgradeController()
        elif self.method == 'transfer':
            result = self.transfer()
        elif self.method == 'withdraw':
            result = self.withdraw()
        elif self.method == 'pickup':
            result = self.pickup()
        else:
            assert False, 'unknown action'
        if result != OK:
            if self.on_error:
                self.on_error()
            else:
                del self.creep.memory.target
                del self.creep.memory.source
                print('ERROR', self, ERRORS[result])
    def build(self):
        return self.creep.build(self.args[0])
    def harvest(self):
        return self.creep.harvest(self.args[0])
    def moveTo(self):
        if self.creep.fatigue > 0:
            return OK  # TODO: some other feeback here
        where = self.args[0]
        return self.creep.moveTo(where, {'visualizePathStyle': {}})
    def upgradeController(self):
        return self.creep.upgradeController(self.args[0])
    def transfer(self):
        return self.creep.transfer(self.args[0], self.args[1])
    def withdraw(self):
        #print('withdraw', self.creep, self.args[0], self.args[1])
        return self.creep.withdraw(self.args[0], self.args[1])
    def pickup(self):
        #print('pickup', self.creep, self.args[0])
        return self.creep.pickup(self.args[0])
    def __str__(self):
        return '[{}] {}.{} {} (on_error={})'.format(
            self.priority,
            self.creep.name,
            self.method,
            str(self.args),
            self.on_error,
        )

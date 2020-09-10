from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class ScheduledAction:
    @classmethod
    def moveTo(cls, creep, target, priority=100):
        return ActionExecution(creep, ActionExecution.moveTo, target, priority)

    @classmethod
    def upgradeController(cls, creep, target, priority=100):
        return ActionExecution(creep, ActionExecution.upgradeController, target, priority)

    @classmethod
    def build(cls, creep, target, priority=100)
        return ActionExecution(creep, ActionExecution.build, target, priority)

    @classmethod
    def harvest(cls, creep, target, priority=100)
        return ActionExecution(creep, ActionExecution.harvest, target, priority)


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



def do_fill(creep):
    # If we have a saved source, use it
    if creep.memory.source:
        source = Game.getObjectById(creep.memory.source)
    else:
        # Get a random new source and save it
        source = _.sample(creep.room.find(FIND_SOURCES))
        creep.memory.source = source.id  # TODO: don't ever use memory, unless we've just reset RAM

    # If we're near the source, harvest it - otherwise, move to it.
    if not creep.pos.isNearTo(source):
        return [ScheduledAction.moveTo(creep, source)]
    return [ScheduledAction.harvest(creep, source)]



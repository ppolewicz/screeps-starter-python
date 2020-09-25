from creeps.parts.carry import Carry
from creeps.parts.work import Work
from creeps.scheduled_action import ScheduledAction


class AbstractCreep:
    DEBUG = False
    ICON = '?'
    def __init__(self, creep, name, creep_registry):
        self.creep = creep
        self.name = name
        self.creep_registry = creep_registry

    @classmethod
    def energy(cls, creep):  # TODO other res
        return _.sum(creep.carry)

    def get_debug(self):
        return self.DEBUG or self.creep.memory.debug
    debug = property(get_debug)

    def pre_run(self):
        if self.debug:
            self.creep.say(self.name[:8] + self.ICON)
        target = Game.flags[self.name]
        if target:
            return [ScheduledAction.moveTo(self.creep, target)]
        if self.creep.memory.room != self.creep.room.name:
            print(self.creep, 'is in', self.creep.room, 'but should be in', self.creep.memory.room)

    def run(self):
        override_actions = self.pre_run()
        if override_actions:
            return override_actions
        return self._run()

    def _run(self):
        pass  #raise NotImplementedError

    def class_exists(self, klass):
        return self.creep_registry.count_of_type(self.creep.room, klass) >= 1

    def total_creeps_in_room(self):
        return self.creep_registry.count(self.creep.room)

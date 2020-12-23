from creeps.parts.carry import Carry
from creeps.parts.work import Work
from creeps.scheduled_action import ScheduledAction
from utils import points_to_path

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class AbstractCreep:
    DEBUG = False
    ICON = '?'
    def __init__(self, creep, namee, creep_registry):
        self.creep = creep
        self.creep_registry = creep_registry

    @classmethod
    def energy(cls, creep):  # TODO other res
        return _.sum(creep.carry)

    def get_debug(self):
        return self.DEBUG or self.creep.memory.debug
    debug = property(get_debug)

    def pre_run(self):
        creep = self.creep
        if self.debug:
            creep.say(creep.name[:8] + self.ICON)
        target = Game.flags[creep.name]
        if target:
            if not creep.pos.isEqualTo(target):
                return [ScheduledAction.moveTo(self.creep, target)]
            target.remove()
        if creep.memory.room != undefined and creep.memory.room != creep.room.name:
            target_room = Game.rooms[creep.memory.room]
            if target_room == undefined:
                print(creep, 'is in', creep.room, 'but should be in', creep.memory.room, 'which we have no eyes on')
                rp = __new__(RoomPosition(25, 25, creep.memory.room))
                print('rp=', rp)
                return [ScheduledAction.moveTo(self.creep, rp)]
            else:
                return [ScheduledAction.moveTo(self.creep, target_room.controller)]

            #roompos = RoomPosition(24, 24, creep.memory.room)
            #print('roompos', roompos, creep.memory.room)
            #pos = {
            #    'range': 22,
            #    'pos': roompos,
            #}
            #return [ScheduledAction.moveTo(self.creep, pos)]

            #route = Game.map.findRoute(creep.room, target);
            #if len(route) > 0:
            #    exit = creep.pos.findClosestByPath(route[0].exit);
            #    return [ScheduledAction.moveTo(self.creep, exit]

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

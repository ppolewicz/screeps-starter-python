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
    REMOVE_FLAG_ON_ARRIVAL = True
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

    def get_smart_move_actions(self, where_pos):
        creep = self.creep
        if creep.pos.roomName == where_pos.roomName:  # just a regular single-room move
            return [ScheduledAction.moveTo(creep, where_pos)]

        limit = 10000
        if Game.cpu.tickLimit < limit/1000:
            print('WARNING:', creep.name, 'cannot pathfind, not enough cpu')
            return []
        result = PathFinder.search(
            creep.pos,
            where_pos,
            {
                'plainCost': 2,
                'swampCost': 10,
                'maxOps': limit,  # 1000 ops = 1 CPU
                #'maxRooms': 16,  # max 64
                #'maxCost': 123456,
            }
        )
        # result structure
        # path	An array of RoomPosition objects.
        # ops	Total number of operations performed before this path was calculated.
        # cost	The total cost of the path as derived from plainCost, swampCost and any given CostMatrix instances.
        # incomplete (flag)
        if result['ops'] >= 0.8*limit:
            print('WARNING: get_smart_move_actions() for', creep.name, 'used', result['ops'], 'mCPU to find path to', where_pos, 'in', where_pos.roomName)
        creep.memory.path = result['path']
        return [ScheduledAction.moveByPath(creep, creep.memory.path)]

    def pre_run(self):
        creep = self.creep
        if self.debug:
            creep.say(creep.name[:8] + self.ICON)

        if creep.memory.path != undefined:
            return [ScheduledAction.moveByPath(creep, points_to_path(creep.memory.path))]

        if creep.memory.target_flag != undefined:
            target_flag_name = creep.memory.target_flag
        else:
            target_flag_name = creep.name

        target = Game.flags[target_flag_name]
        if target:
            if creep.pos.isEqualTo(target):
                if self.REMOVE_FLAG_ON_ARRIVAL:
                    target.remove()
                else:
                    return []
            else:
                return self.get_smart_move_actions(target.pos)

        if creep.memory.room != undefined and creep.memory.room != creep.room.name:
            target_room = Game.rooms[creep.memory.room]
            if target_room == undefined:
                rp = __new__(RoomPosition(25, 25, creep.memory.room))
                #print(creep, 'is in', creep.room, 'but should be in', creep.memory.room, 'which we have no eyes on', rp)
                return self.get_smart_move_actions(rp)
            else:
                return self.get_smart_move_actions(target_room.controller.pos)

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

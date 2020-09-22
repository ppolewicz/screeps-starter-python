from creeps import CREEP_CLASSES
from room_manager import MANAGER_REGISTRY

# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class CreepRegistry:
    def __init__(self):
        self.by_room = {}
    def count_of_type(self, room, creep_type):
        if room not in self.by_room:
            return 0
        room_creeps = self.by_room[room]
        result = 0
        for creep in room_creeps:
            if creep.memory.cls == creep_type:
                result += 1
        #print('CreepRegistry.count_of_type(', room, creep_type, '):', result)
        return result
    def register(self, room, creep):
        if room not in self.by_room:
            self.by_room[room] = set()
        self.by_room[room].add(creep)


def main():
    """
    Main game logic loop.
    """

    creep_registry = CreepRegistry()
    imports = Game.cpu.getUsed()

    if Game.cpu.buffer > 9000:
        Game.cpu.generate_pixel()

    all_actions = []
    # Register each creep
    creeps_to_do = []
    for name in Object.keys(Game.creeps):
        #if name == 'Stella':
        #    # Game.creeps['Stella'].moveTo(Game.creeps['Stella'].room.controller)
        #    # Game.creeps['Stella'].signController(Game.creeps['Stella'].room.controller, '')
        #    continue
        creep = Game.creeps[name]
        creep_registry.register(creep.room, creep)
        if creep.spawning:
            continue
        creeps_to_do.append(creep)

    # Run each creep
    for creep in creeps_to_do:
        creep_class = CREEP_CLASSES[creep.memory.cls]
        if not creep_class:
            #print('ERROR, NO CREEP CLASS FOR', creep.memory.cls)
            creep_class = CREEP_CLASSES['harvester']
        #print('running', creep_class.__name__, 'for', creep)
        actions = creep_class(creep, creep.name, creep_registry).run()
        #print('actions for', creep, 'are', actions)
        all_actions.append(actions)
    #print('creeps done')
    # Get the number of our creeps in the room.
    #num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)

    my_rooms = set()  # TODO: cache my rooms in memory like a pro
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        my_rooms.add(spawn.room)
    #print('after rooms done, room count:', len(my_rooms))

    for room in my_rooms:
        manager_class = MANAGER_REGISTRY[room.controller.level]
        manager = manager_class(room, room.name, creep_registry, True)
        #print("before", manager_class.__name__, room)
        all_actions.extend(manager.run())

    #Game.rooms['W25N1'].visual.circle(10,20).line(0,0,10,20)
    #MANAGER_REGISTRY[2](room, room.name, creep_registry, False)

    actions_cost = execute_actions(all_actions)
    used = Game.cpu.getUsed()
    print(
        '-------- total:', round(used, 3),
        'imports:', round(imports, 3),
        'actions:', round(actions_cost, 3),
        'code:', round(used-imports-actions_cost, 3),
    )
    if Game.time % 1500 == 0:
        for name in Object.keys(Memory.creeps):
            if not Game.creeps[name]:
                print('Clearing non-existing creep memory(powered by python™): ' + name)
                del Memory.creeps[name]

    #<font color="red"></font>

def execute_actions(all_actions):
    all_actions.sort(key=lambda action_set: max(action.priority for action in action_set), reversed=True)
    total = 0
    for action_set in all_actions:
        if Game.cpu.tickLimit < len(action_set)*0.2:
            print('ran out of CPU before running %s' % action_set)
            break
        for action in action_set:
            action.run()
            total += 0.2
    return total


module.exports.loop = main

import collections

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
    # TODO: this class can be used to build roads and stuff
    def __init__(self):
        self.by_room = collections.defaultdict(list)
    def register(self, room, creep):
        self.by_room[room].append(creep)


def main():
    """
    Main game logic loop.
    """

    creep_registry = CreepRegistry()

    if Game.cpu.buffer > 9000:
        Game.cpu.generate_pixel()

    all_actions = []
    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        creep_registry.register(creep.room, creep)
        actions = CREEP_CLASSES[creep.memory.cls].run(creep)
        all_actions.append(actions)

    # Get the number of our creeps in the room.
    #num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)

    my_rooms = set()  # TODO: cache my rooms in memory like a pro
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        my_rooms.add(spawn.room)

    for room in my_rooms:
        manager_class = MANAGER_REGISTRY[room.controller.level]
        manager = manager_class(room, creep_registry)
        all_actions.extend(manager.run())
    execute_actions(all_actions)


def execute_actions(all_actions):
    all_actions.sort(key=lambda action_set: max(action.priority for action in action_set), reversed=True)
    for action_set in all_actions:
        if Cpu.limit < len(action_set)*0.2:
            print('ran out of CPU before running %s' % action_set)
            break
        for action in actions_set:
            action.run()


module.exports.loop = main

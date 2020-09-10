from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from action_execution import ActionExecution
from scheduled_action import ScheduledAction


class Harverster:
    @classmethod
    def run(cls, creep):
        # If we're full, stop filling up and remove the saved source
        if creep.memory.filling and _.sum(creep.carry) >= creep.carryCapacity:
            creep.memory.filling = False
            del creep.memory.source
        # If we're empty, start filling again and remove the saved target
        elif not creep.memory.filling and creep.carry.energy <= 0:
            creep.memory.filling = True
            del creep.memory.target

        if creep.memory.filling:
            return do_fill()

        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
            if target.energy == target.energyCapacity:  # full already
                del creep.memory.target
                target = cls.get_new_target()
        else:
            target = cls.get_new_target()
        # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
        if target.energyCapacity:
            is_close = creep.pos.isNearTo(target)
        else:
            is_close = creep.pos.inRangeTo(target, 3)

        if not is_close:
            return [ScheduledAction.moveTo(creep, target)]

        # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
        if target.energyCapacity:
            def clear_target():
                del creep.memory.target

            return [ScheduledAction.transfer(creep, target, RESOURCE_ENERGY, on_full=clear_target)]
            result = creep.transfer(target, RESOURCE_ENERGY)
            if result == OK or result == ERR_FULL:
                del creep.memory.target
        else:
            action = ScheduledAction.upgradeController(creep, target]
            if creeps.room.controller.ticksToDowngrade < 4000:
                action.priority = 1000
            return [action]
            #result = creep.upgradeController(target)
            #if result != OK:
            #    print("[{}] Unknown result from creep.upgradeController({}): {}".format(creep.name, target, result))
            ## Let the creeps get a little bit closer than required to the controller, to make room for other creeps.
            #if not creep.pos.inRangeTo(target, 2):
            #    return [ScheduledAction.moveTo(creep, target)]

    @classmethod
    def get_new_target(cls, creep):
        extensions_to_build = _(creep.room.find(FIND_CONSTRUCTION_SITES)) \
            .filter(
                lambda s: (
                (
                    s.structureType == STRUCTURE_EXTENSION
                )
            )
        )
        if extensions_to_build:
            target = extensions_to_build[0]
            is_close = creep.pos.isNearTo(target)
            if not is_close:
                return [ScheduledAction.moveTo(creep, target)]
            return [ScheduledAction.build(creep, target)]
        # Get a random new target.
        target = _(creep.room.find(FIND_MY_STRUCTURES)) \
            .filter(
                lambda s: (
                (
                    s.structureType == STRUCTURE_SPAWN or
                    s.structureType == STRUCTURE_EXTENSION or
                    s.structureType == STRUCTURE_TOWER  # somehow ;)
                )
                    and s.energy < s.energyCapacity
                )
            ).sample()
        if target is None:
            target = creep.room.controller
        creep.memory.target = target.id

    @classmethod
    def do_fill(cls, creep):
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

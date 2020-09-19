from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from creeps.scheduled_action import ScheduledAction
from creeps.abstract import AbstractCreep


class Harvester(AbstractCreep):
    @classmethod
    def run(cls, creep):
        # If we're full, stop filling up and remove the saved source
        if creep.memory.filling and cls.energy(creep) >= creep.carryCapacity:
            creep.memory.filling = False
            del creep.memory.source
        # If we're empty, start filling again and remove the saved target
        elif not creep.memory.filling and creep.carry.energy <= 0:
            creep.memory.filling = True
            del creep.memory.target

        if creep.memory.filling:
            return cls.do_fill(creep)

        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
            if not target:
                target = cls.get_new_target(creep)
            elif target.energy != undefined and target.energy == target.energyCapacity:  # a full container
                target = cls.get_new_target(creep)
        else:
            target = cls.get_new_target(creep)
        # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
        if target.energyCapacity:
            is_close = creep.pos.isNearTo(target)
        else:
            is_close = creep.pos.inRangeTo(target, 3)

        def reset_target():
            print(creep, "reset_target()")
            del creep.memory.target
        if not is_close:
            return [ScheduledAction.moveTo(creep, target, on_error=reset_target)]

        # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
        if target.energyCapacity:
            def clear_target():
                del creep.memory.target
            return [ScheduledAction.transfer(creep, target, RESOURCE_ENERGY, on_error=clear_target)]
        else:
            if target.structureType == STRUCTURE_CONTROLLER:
                action = ScheduledAction.upgradeController(creep, target)
                if creep.room.controller.ticksToDowngrade < 4000:
                    action.priority = 1000
            else:
                action = ScheduledAction.build(creep, target)
                action.priority = 200
            return [action]

    @classmethod
    def get_new_target(cls, creep):
        target = cls._get_new_target(creep)
        creep.memory.target = target.id
        return target

    @classmethod
    def _get_new_target(cls, creep):
        if creep.room.controller.level == 1:
            # in RCL1 we don't want to fill the spawn, it will fill by itself in 300t and there is nothing else to fill, really
            return creep.room.controller

        target_filter = lambda s: (
            (
                s.structureType == STRUCTURE_SPAWN or
                s.structureType == STRUCTURE_EXTENSION or
                s.structureType == STRUCTURE_TOWER  # somehow ;)
            )
            and s.energy < s.energyCapacity
        )
        target = _(creep.room.find(FIND_MY_STRUCTURES)).filter(target_filter).sample()  # TODO: reserve it so that everyone doesn't run to the same thing
        if target:
            return target

        sites = creep.room.find(FIND_CONSTRUCTION_SITES)
        def distanceFromCreep(site):
            return max(abs(site.pos.x-creep.pos.x), abs(site.pos.y-creep.pos.y))
        sites.sort(key=distanceFromCreep)
        for site in sites:
            #if site.structureType != STRUCTURE_EXTENSION and site.structureType != STRUCTURE_ROAD:
            #    continue
            return site

        return creep.room.controller

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


class WorkTarget:
    @classmethod
    def get_new_target(cls, creep):
        target = cls._get_new_target(creep)
        print('new target for', creep, 'is', target)
        creep.memory.target = target.id
        return target

    @classmethod
    def _get_closest_construction_site(cls, creep):
        return creep.pos.findClosestByRange(FIND_CONSTRUCTION_SITES)

    @classmethod
    def _get_rcl1_controller(cls, creep):
        if creep.room.controller.level == 1:
            # in RCL1 we don't want to fill the spawn, it will fill by itself in 300t and there is nothing else to fill, really
            return creep.room.controller

    @classmethod
    def _get_random_nonempty_util_building(cls, creep):
        target_filter = lambda s: (
            (
                s.structureType == STRUCTURE_SPAWN or
                s.structureType == STRUCTURE_EXTENSION or
                s.structureType == STRUCTURE_TOWER  # somehow ;)
            )
            and s.energy < s.energyCapacity
        )
        return _(creep.room.find(FIND_MY_STRUCTURES)).filter(target_filter).sample()  # TODO: reserve it so that everyone doesn't run to the same thing

    @classmethod
    def _get_room_controller(cls, creep):
        return creep.room.controller

    @classmethod
    def _get_random_non_miner_container(cls, creep):
        containers = []
        for s in creep.room.find(FIND_STRUCTURES):
            if s.structureType != STRUCTURE_CONTAINER:
                continue
            # TODO: if store is not full
            # s.store[RESOURCE_ENERGY]
            #    continue
            #print('container found', s)
            nearby_sources = s.pos.findInRange(FIND_SOURCES, 1)
            #print('len', len(nearby_sources))
            if len(nearby_sources) >= 1:
                continue  # that's for a miner
            containers.append(s)
        return containers[0]  # TODO: get a "random" one ha ha, maybe Creep.id + Game.time


    @classmethod
    def _get_new_target(cls, creep):
        for target_getter in cls._get_target_getters(creep):
        #for target_getter in cls.TARGET_GETTERS:
            target = target_getter(creep)
            if target:
                return target
        print('FATAL: no targets for', creep, 'and no default')

    @classmethod
    def get_new_target(cls, creep):
        target = cls._get_new_target(creep)
        print('new target for', creep, 'is', target)
        creep.memory.target = target.id
        return target


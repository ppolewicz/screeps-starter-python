from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


non_empty_util_building_filter = lambda s: (
    (
        s.structureType == STRUCTURE_SPAWN or
        s.structureType == STRUCTURE_EXTENSION or
        s.structureType == STRUCTURE_TOWER  # somehow ;)
    )
    and s.energy < s.energyCapacity
)


class WorkTarget:
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
        return _(creep.room.find(FIND_MY_STRUCTURES)).filter(non_empty_util_building_filter).sample()  # TODO: reserve it so that everyone doesn't run to the same thing

    @classmethod
    def _get_closest_nonempty_util_building(cls, creep):
        return creep.pos.findClosestByPath(FIND_MY_STRUCTURES, {'filter': non_empty_util_building_filter})

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
            if s.store.getFreeCapacity(RESOURCE_ENERGY) == 0:
                continue  # it's full
            containers.append(s)
        if len(containers) >= 1:
            return containers[0]  # TODO: get a "random" one ha ha, maybe Creep.id + Game.time

    @classmethod
    def _get_storage(cls, creep):
        storage = creep.room.storage
        if storage != undefined:
            return storage

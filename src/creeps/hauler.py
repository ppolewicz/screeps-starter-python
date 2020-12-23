from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from creeps.harvester import Harvester
from room_manager.abstract import g_links


class Hauler(Harvester):
    #DEBUG = True
    ICON = '🚚'
    def room_really_needs_refill(self):
        creep = self.creep
        room = creep.room
        emergency_sum = 0
        if room.storage != undefined:
            emergency_sum += room.storage.store[RESOURCE_ENERGY]
        if room.terminal != undefined:
            emergency_sum += room.terminal.store[RESOURCE_ENERGY]
        to_fill = room.energyCapacityAvailable - room.energyAvailable
        if to_fill > creep.store[RESOURCE_ENERGY] and emergency_sum > creep.carryCapacity:
            return True
        return False

    @classmethod
    def _get_target_getters(cls, creep):
        targets = [
            cls._get_closest_nonempty_util_building,
            #cls._get_random_nonempty_util_building,  # TODO: balance
            #cls._get_neighboring_nonfull_link,       # TODO: remove that function if miner doesn't use it
        ]
        #print('g_links', g_links, g_links.get)
        #if not g_links or g_links == undefined:
        #    print('warning!!!')
        #    return
        #our_links = g_links.get(creep.room.name)
        #if not our_links.operational():
        if creep.room.controller.level <= 4:
            targets.append(
                cls._get_random_non_miner_container,
            )
        fullest_miner_container = cls._get_fullest_miner_container(creep)
        if fullest_miner_container != undefined and fullest_miner_container.store[RESOURCE_ENERGY] > 0:
            #print('yeah', creep.name, fullest_miner_container.store[RESOURCE_ENERGY], fullest_miner_container.id)
            targets.append(cls._get_nonfull_terminal)
            targets.append(cls._get_nonfull_storage)
        #else:
        #    print('nope', creep.name)
        return targets

    def _get_source_getters(self):
        sources = []
        sources.append(self._get_nearby_dropped_resource)
        if self.creep.room.energyCapacityAvailable - self.creep.room.energyAvailable >= 1:
            sources.append(self._get_refill_source)
        if self.room_really_needs_refill():
            sources.append(self._get_nonempty_storage)
            sources.append(self._get_nonempty_terminal)
        sources.append(self._get_neighboring_miner_container)
        sources.append(self._get_dropped_resource)
        sources.append(self._get_random_energetic_ruin)
        #if self.creep.room.controller.level <= 4:
        sources.append(self._get_fullest_miner_container)
        #sources.append(self._get_closest_energetic_container)
        #else:
        #    sources.append(self._get_fullest_miner_container)  # TODO: this is until miners can figure out what to do with energy
        return sources

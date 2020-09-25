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


class Hauler(Harvester):
    DEBUG = True
    ICON = '🚚'
    @classmethod
    def _get_target_getters(cls, creep):
        return [
            cls._get_closest_nonempty_util_building,
            #cls._get_random_nonempty_util_building,
            cls._get_random_non_miner_container,
            cls._get_storage,
        ]

    def _get_source_getters(self):
        return [
            self._get_neighboring_miner_container,
            self._get_dropped_resource,
            self._get_random_energetic_ruin,
            self._get_fullest_miner_container,
        ]

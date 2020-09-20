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
    @classmethod
    def _get_target_getters(cls, creep):
        return [
            cls._get_random_non_miner_container,
        ]

    @classmethod
    def _get_source_getters(cls, creep):
        return [
            cls._get_dropped_resource,
            cls._get_random_energetic_ruin,
            cls._get_fullest_miner_container,
        ]

    @classmethod
    def run(cls, creep):
        return []
        #scheduled_actions = Hauler.run(creep)
        #if scheduled_actions:
        #    if scheduled_actions[0].method == 'build':
        #        scheduled_actions[0].method == 'transfer'
        #return scheduled_actions

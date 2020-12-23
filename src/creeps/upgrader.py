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


class Upgrader(Harvester):
    ICON = '👍'
    def _get_source_getters(self):
        if self.creep.room.controller.level >= 4 or self.class_exists('hauler'):
            return [self._get_nearby_dropped_resource, self._get_neighboring_nonempty_link, self._get_source_of_faith]
        return super()._get_source_getters()

    def _get_target_getters(self):
        if self.creep.room.controller.level == 8:
            return [self._get_best_free_church, self._get_room_controller]
        return super()._get_target_getters()

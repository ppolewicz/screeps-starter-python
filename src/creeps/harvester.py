from ..defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from creeps.easy import EasyCreep


class Harvester(EasyCreep):
    ICON = '☭'
    def _get_source_getters(self):
        result = []
        if not self.class_exists('hauler'):
            result.append(self._get_dropped_resource)
        result.append(self._get_closest_energetic_container)
        result.append(self._get_random_energetic_ruin)
        result.append(self._get_neighboring_source)
        result.append(self._get_nonempty_storage)
        result.append(self._get_random_source)
        return result

    def _get_target_getters(self):
        result = [self._get_rcl1_controller]
        if not self.class_exists('hauler'):
            #if self.total_creeps_in_room() == 1:
            result.append(self._get_closest_nonempty_util_building)
            #else:
            #    result.append(self._get_random_nonempty_util_building)
        #if not self.class_exists('builder') or self.creep.memory.cls == 'builder':  # TODO
        result.append(self._get_closest_construction_site)
        result.append(self._get_room_controller)
        return result


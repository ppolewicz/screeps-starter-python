from creeps.parts.carry import Carry
from creeps.parts.work import Work
from creeps.scheduled_action import ScheduledAction


class AbstractCreep(Carry, Work):
    DEBUG = False
    ICON = '?'
    def __init__(self, creep, name, creep_registry):
        self.creep = creep
        self.name = name
        self.creep_registry = creep_registry

    @classmethod
    def energy(cls, creep):  # TODO other res
        return _.sum(creep.carry)

    def get_debug(self):
        return self.DEBUG or self.creep.memory.debug
    debug = property(get_debug)

    def pre_run(self):
        if self.debug:
            self.creep.say(self.name[:8] + self.ICON)
        target = Game.flags[self.name]
        if target:
            return [ScheduledAction.moveTo(self.creep, target)]

    def run(self):
        override_actions = self.pre_run()
        if override_actions:
            return override_actions
        return self._run()

    def _run(self):
        pass  #raise NotImplementedError

    def class_exists(self, klass):
        return self.creep_registry.count_of_type(self.creep.room, klass) >= 1

    def _get_source_getters(self):
        result = []
        if not self.class_exists('hauler'):
            result.append(self._get_dropped_resource)
        result.append(self._get_closest_energetic_container)
        result.append(self._get_random_energetic_ruin)
        result.append(self._get_neighboring_source)
        result.append(self._get_random_source)
        return result

    def _get_target_getters(self):
        result = [self._get_rcl1_controller]
        if not self.class_exists('hauler'):
            result.append(self._get_random_nonempty_util_building)
        #if not self.class_exists('builder') or self.creep.memory.cls == 'builder':  # TODO
        result.append(self._get_closest_construction_site)
        result.append(self._get_room_controller)
        return result

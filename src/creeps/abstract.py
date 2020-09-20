from creeps.scheduled_action import ScheduledAction
from creeps.parts.carry import Carry
from creeps.parts.work import Work


class AbstractCreep(Carry, Work):
    @classmethod
    def energy(cls, creep):  # TODO other res
        return _.sum(creep.carry)

    # TODO: move defaults
    @classmethod
    def _get_source_getters(cls, creep):
        return [
            cls._get_dropped_resource,
            cls._get_closest_energetic_container,
            cls._get_random_energetic_ruin,
            cls._get_neighboring_source,
            cls._get_random_source,
        ]

    @classmethod
    def _get_target_getters(cls, creep):
        return [
            cls._get_rcl1_controller,
            cls._get_random_nonempty_util_building,
            cls._get_closest_construction_site,
            cls._get_room_controller,
        ]

from creeps.scheduled_action import ScheduledAction
from creeps.abstract import AbstractCreep


class Claimer(AbstractCreep):
    ICON = '⛪'
    def _run(self):
        super()._run()
        creep = self.creep
        room = creep.room
        controller = room.controller
        if controller.my:
            return []
        if not creep.pos.isNearTo(controller):
            return [ScheduledAction.moveTo(creep, controller)]
        return [ScheduledAction.claimController(creep, controller)]

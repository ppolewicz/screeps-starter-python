__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')


from creeps.scheduled_action import ScheduledAction
from creeps.abstract import AbstractCreep


class Claimer(AbstractCreep):
    DEBUG = True
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
        if controller.owner != undefined:
            # TODO: check if there are any other claimer creeps in this room that we could sync for a bigger bang
            #find_creeps
            # filter: creep.my and creep.parts has CLAIM and not creep.pos.isNearTo(controller)
            return [ScheduledAction.attackController(creep, controller)]
        return [ScheduledAction.claimController(creep, controller)]

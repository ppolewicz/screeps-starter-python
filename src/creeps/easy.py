from creeps.abstract import AbstractCreep
from creeps.parts.carry import Carry
from creeps.parts.work import Work
from creeps.scheduled_action import ScheduledAction

__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class EasyCreep(AbstractCreep, Carry, Work):
    DEBUG = False
    ICON = '?'
    def __init__(self, creep, name, creep_registry):
        self.creep = creep
        self.name = name
        self.creep_registry = creep_registry

    def _get_source_getters(self):
        raise NotImplementedError

    def _get_target_getters(self):
        raise NotImplementedError

    @classmethod
    def _get_storage(cls, creep):  # works for both source and target
        storage = creep.room.storage
        if storage != undefined:
            return storage

    def _get_new_target(self):
        for target_getter in self._get_target_getters(self.creep):
            target = target_getter(self.creep)
            if target:
                return target
        print('FATAL: no targets for', self.creep, '(', self.creep.memory.cls, ') and no default')

    def get_new_target(self):
        target = self._get_new_target()
        if target:
            print('new target for', self.creep, 'is', target)
            self.creep.memory.target = target.id
            return target

    def _run(self):
        super()._run()
        creep = self.creep
        # If we're full, stop filling up and remove the saved source
        if creep.memory.filling and self.energy(creep) >= creep.carryCapacity:
            creep.memory.filling = False
            del creep.memory.source
        # If we're empty, start filling again and remove the saved target
        elif not creep.memory.filling and creep.carry.energy <= 0:
            creep.memory.filling = True
            del creep.memory.target

        if creep.memory.filling:
            return self.do_fill(creep)

        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
            if not target:
                target = self.get_new_target(creep)
            elif target.energy != undefined and target.energy == target.energyCapacity:  # a full container
                target = self.get_new_target(creep)
        else:
            target = self.get_new_target(creep)

        if not target:
            return []

        # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
        if target.energyCapacity or target.store:
            is_close = creep.pos.isNearTo(target)
        else:
            is_close = creep.pos.inRangeTo(target, 3)

        def reset_target():
            print('WARNING', creep, "reset_target() had to be called on", creep.memory.target)
            del creep.memory.target

        if not is_close:
            return [ScheduledAction.moveTo(creep, target, on_error=reset_target)]

        # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
        if target.energyCapacity:
            return [ScheduledAction.transfer(creep, target, RESOURCE_ENERGY, on_error=reset_target)]

        # upgradeController
        if target.structureType == STRUCTURE_CONTROLLER:
            action = ScheduledAction.upgradeController(creep, target)
            if creep.room.controller.ticksToDowngrade < 4000:
                action.priority = 1000
            else:
                action.priority = 20
            return [action]

        # build
        if target.progressTotal:
            action = ScheduledAction.build(creep, target)
            action.priority = 200
            return [action]
        if target.store:
            return [ScheduledAction.transfer(creep, target, RESOURCE_ENERGY, on_error=reset_target)]
        print('ERROR: not sure what', creep, 'should do with', target)
        return []

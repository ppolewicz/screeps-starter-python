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
            fill_actions = self.do_fill(creep)
            #if fill_actions[0].method == 'move':  # TODO: fill and go move to a new target, but no double transfer
            return fill_actions

        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
            if not target:
                target = self.get_new_target(creep)
            elif target.energy != undefined and target.energy == target.energyCapacity:
                # full container, probably someone else filled it last tick or helped filling it
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
            actions = []
            if target.structureType == STRUCTURE_STORAGE or target.structureType == STRUCTURE_CONTAINER or target.structureType == STRUCTURE_TERMINAL:
                if not target.store:
                    pass  # that's a construction site, not an actual thing
                    #print(creep, 'not gonna repair anything on the way because heading to c-site')
                #elif target.store[RESOURCE_ENERGY] >= 1000:
                else:
                    if creep.body[0].type == WORK:  # TODO: IN, not body[0]
                        #print(creep, 'gonna try to repair because target >= 1000 and WORK')
                        repairs = []
                        for s in creep.pos.findInRange(FIND_STRUCTURES, 3):
                            if -1*(s.hits-s.hitsMax) > 500:  # if it's lower, we might get two repair dudes to overburn it
                                repairs.append(s)
                        #print('repairs', repairs)
                        if len(repairs) >= 1:
                            tgt = _.min(repairs, lambda s: s.hits)
                            #actions.append(ScheduledAction.repair(creep, tgt, priority=20))
                            a = ScheduledAction.repair(creep, tgt)
                            a.priority = 20
                            actions.append(a)
                            #print(creep, 'gonna try to repair', tgt, tgt.pos, tgt.hits)
                        else:
                            #print(creep, 'not gonna repair anything on the way')
                            builds = creep.pos.findInRange(FIND_CONSTRUCTION_SITES, 3)
                            if len(builds) >= 1:
                                tgt = _.min(builds, lambda s: s.progressTotal - s.progress)
                                actions.append(ScheduledAction.build(creep, builds[0], priority=20))
            actions.append(ScheduledAction.moveTo(creep, target, on_error=reset_target))
            return actions

        # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
        if target.energyCapacity:
            actions = []
            actions.append(ScheduledAction.transfer(creep, target, RESOURCE_ENERGY, on_error=reset_target))
            if target.store.getFreeCapacity(RESOURCE_ENERGY) >= self.energy(creep):
                actions.extend(self.do_fill(creep))
                #print(creep, 'gooooo')  # TODO XXX: test it
            else:
                # we will fill it to the brim
                # maybe someone will pull from this container or spawn or something and in the next tick
                # it would need to be filled again - but in that case we will run self.get_new_target() with
                # next tick where we know what happened.
                target = self.get_new_target(creep)  # TODO XXX: but this should be a different one!
                actions.append(ScheduledAction.moveTo(creep, target))
            return actions

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
            actions = [ScheduledAction.transfer(creep, target, RESOURCE_ENERGY, on_error=reset_target)]
            #if target.store.getFreeCapacity(RESOURCE_ENERGY) >= self.energy(creep):
            #    #print(creep, 'gooooo2')  # TODO XXX: flaps near storage if room really needs refill
            #    actions.extend(self.do_fill(creep))
            return actions
        actions = []
        actions.append(ScheduledAction.moveTo(creep, target))
        #print('ERROR: not sure what', creep, 'should do with', target)
        return actions

__pragma__('noalias', 'undefined')

from creeps.scheduled_action import ScheduledAction


class CarrySource:
    @classmethod
    def _get_cached_source(cls, creep):
        if creep.memory.source:  # TODO: don't ever use memory, unless we've just reset RAM
            return Game.getObjectById(creep.memory.source)

    @classmethod
    def _get_dropped_resource(cls, creep):
        # when a creep dies and leaves some energy, go pick it up
        source_filter = lambda s: (
            s.resourceType == RESOURCE_ENERGY and s.amount >= 50
        )
        source = creep.pos.findClosestByRange(FIND_DROPPED_RESOURCES, filter=source_filter)  # TODO: reserve it for the creep that is closest to the thing
        return source

    @classmethod
    def _get_closest_energetic_container(cls, creep):
        #free_capacity = creep.store.getFreeCapacity(RESOURCE_ENERGY)
        source_filter = lambda s: (
            (s.structureType == STRUCTURE_CONTAINER or s.structureType == STRUCTURE_STORAGE or s.structureType == STRUCTURE_TERMINAL)
            and s.store[RESOURCE_ENERGY] >= 50
        )
        result = creep.pos.findClosestByRange(FIND_STRUCTURES, filter=source_filter)
        #print('closest energetic container for', creep, 'is', result)
        return result

    @classmethod
    def _get_nearby_dropped_resource(cls, creep):
        sources = creep.pos.findInRange(FIND_DROPPED_RESOURCES, 3)
        if len(sources) >= 1:
            return sources[0]

    @classmethod
    def _get_random_energetic_ruin(cls, creep):
        source_filter = lambda s: (
            s.store[RESOURCE_ENERGY] >= 1
        )
        return _(creep.room.find(FIND_RUINS)).filter(source_filter).sample()  # TODO: reserve it so that everyone doesn't run to the same thing

    def get_source(self):
        source = self._get_cached_source(self.creep)
        if source:
            return source
        for source_getter_id, source_getter in enumerate(self._get_source_getters()):
            source = source_getter(self.creep)
            if source and source.pos != None:
                self.creep.memory.source = source.id
                return source
        print(self.creep, 'no source!')

    @classmethod
    def _get_neighboring_nonempty_link(cls, creep):
        source_filter = lambda s: (
            s.structureType == STRUCTURE_LINK and s.store[RESOURCE_ENERGY] >= 50
        )
        container = creep.pos.findInRange(FIND_STRUCTURES, 1, filter=source_filter)
        if len(container) >= 1:
            return container[0]

    @classmethod
    def _get_neighboring_nonfull_link(cls, creep):
        source_filter = lambda s: (
            s.structureType == STRUCTURE_LINK and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0
        )
        container = creep.pos.findInRange(FIND_STRUCTURES, 3, filter=source_filter)  # TODO
        if len(container) >= 1:
            return container[0]

    @classmethod
    def _get_neighboring_miner_container(cls, creep):
        source_filter = lambda s: (  # TODO: deduplicate those lambdas
            s.structureType == STRUCTURE_CONTAINER and s.store[RESOURCE_ENERGY] >= 50
        )
        container = creep.pos.findInRange(FIND_STRUCTURES, 1, filter=source_filter)
        if len(container) >= 1:
            nearby_sources = container[0].pos.findInRange(FIND_SOURCES, 1)
            if len(nearby_sources) >= 1:
                return container[0]

    @classmethod
    def _get_neighboring_source(cls, creep):
        return creep.pos.findInRange(FIND_SOURCES, 1)

    @classmethod
    def _get_random_source(cls, creep):
        source = _.sample(creep.room.find(FIND_SOURCES))  # TODO: balance instead of randomizing
        if creep.room.name == 'sim':
            while source.pos.x == 6 and source.pos.y == 44:  # TODO: do not just walk up to a Source Keeper
                source = _.sample(creep.room.find(FIND_SOURCES))
        return source

    @classmethod
    def _get_fullest_miner_container(cls, creep):
        containers = []
        for s in creep.room.find(FIND_STRUCTURES):
            if s.structureType != STRUCTURE_CONTAINER:
                continue
            if s.store[RESOURCE_ENERGY] <= 0:
                continue
            nearby_sources = s.pos.findInRange(FIND_SOURCES, 1)
            if len(nearby_sources) == 0:
                continue  # that's not for a miner
            containers.append(s)
        #def distanceFromCreep(site):
        #    return max(abs(site.pos.x-creep.pos.x), abs(site.pos.y-creep.pos.y))
        containers.sort(key=lambda container: -1*container.store[RESOURCE_ENERGY])
        return containers[0]  # TODO: get a "random" one ha ha, maybe Creep.id + Game.time

    @classmethod
    def _get_source_of_faith(cls, creep):
        containers = []
        for s in creep.room.controller.pos.findInRange(FIND_STRUCTURES, 3):
            if s.structureType != STRUCTURE_CONTAINER and s.structureType != STRUCTURE_LINK:
                continue
            if s.store[RESOURCE_ENERGY] > 0:
                return s

    @classmethod
    def _get_nonempty_storage(cls, creep):
        storage = creep.room.storage
        if storage != undefined:
            if storage.store[RESOURCE_ENERGY] > 50:
                return storage

    @classmethod
    def _get_nonempty_terminal(cls, creep):
        terminal = creep.room.terminal
        if terminal != undefined:
            if terminal.store[RESOURCE_ENERGY] > 50:
                return terminal

    def do_fill(self):
        creep = self.creep
        source = self.get_source(creep)

        def reset_source():
            if creep.store.getFreeCapacity(RESOURCE_ENERGY) < creep.store.getCapacity(RESOURCE_ENERGY) * 0.6:
                creep.memory.filling = False  # XXX HACKS
            del creep.memory.source

        if not creep.pos.isNearTo(source):
            return [ScheduledAction.moveTo(creep, source, reset_source)]

        if source.amount != None:  # dropped resource
            return [ScheduledAction.pickup(creep, source, reset_source)]
        elif source.destroyTime != None:  # ruin
            del creep.memory.source  # we'll drain it to our capacity all in one tick, lets not try taking it again next tick
            return [ScheduledAction.withdraw(creep, source, RESOURCE_ENERGY)]
        elif source.store != None:  # container/storage
            if creep.store.getFreeCapacity(RESOURCE_ENERGY) >= source.store[RESOURCE_ENERGY]:
                who = creep.room.lookForAt(LOOK_CREEPS, source.pos)
                if len(who) >= 1:
                    # some creep is currently there
                    if who[0].memory.cls == 'miner':  # and it's a miner!
                        # save CPU: don't just stand there and siphon it as it is being filled
                        if Game.time % 10 != 0:  # TODO: save even more cpu
                            # but if the room is drained completely, don't wait for the entire pilgrimage
                            # try to unstuck
                            return []
            return [ScheduledAction.withdraw(creep, source, RESOURCE_ENERGY)]  # TODO: reset_source doesn't work
        else:  # a source
            return [ScheduledAction.harvest(creep, source)]

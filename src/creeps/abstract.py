from creeps.scheduled_action import ScheduledAction


class AbstractCreep:
    @classmethod
    def energy(cls, creep):  # TODO other res
        return _.sum(creep.carry)

    @classmethod
    def _get_cached_source(cls, creep):
        if creep.memory.source:  # TODO: don't ever use memory, unless we've just reset RAM
            return Game.getObjectById(creep.memory.source)

    @classmethod
    def _get_dropped_resource(cls, creep):
        # when a creep dies and leaves some energy, go pick it up
        #resource = _.sample(creep.room.find(FIND_DROPPED_RESOURCES))
        return creep.pos.findClosestByRange(FIND_DROPPED_RESOURCES)  # TODO: reserve it for the creep that is closest to the thing

    @classmethod
    def _get_source(cls, creep):
        source = cls._get_cached_source(creep)
        if source:
            return source

        source = cls._get_dropped_resource(creep)
        if source:
            creep.memory.source = source.id
            return source

        source_filter = lambda s: (
            s.structureType == STRUCTURE_CONTAINER and s.store[RESOURCE_ENERGY] >= 1
        )
        source = creep.pos.findClosestByRange(FIND_STRUCTURES, filter=source_filter)
        if source:
            print('found a container with energy', creep, source)
            creep.memory.source = source.id
            return source

        source_filter = lambda s: (
            s.store[RESOURCE_ENERGY] >= 1
        )
        source = _(creep.room.find(FIND_RUINS)).filter(source_filter).sample()  # TODO: reserve it so that everyone doesn't run to the same thing
        if source:
            print('found energetic ruin', source)
            creep.memory.source = source.id
            return source

        sources = creep.room.find(FIND_SOURCES)
        def distanceFromCreep(site):
            return max(abs(site.pos.x-creep.pos.x), abs(site.pos.y-creep.pos.y))
        sources.sort(key=distanceFromCreep)
        if distanceFromCreep(sources[0]) <= 1 and creep.hits == 700:  # TODO: optimize via lookAt or something
            source = sources[0]
        elif creep.hits != 700:
            source = sources[1]  # XXX HACK
        else:
            # Get a random new source and save it
            source = _.sample(creep.room.find(FIND_SOURCES))  # TODO: balance instead of randomizing
            if creep.room.name == 'sim':
                while source.pos.x == 6 and source.pos.y == 44:  # TODO: do not just walk up to a Source Keeper
                    source = _.sample(creep.room.find(FIND_SOURCES))
        creep.memory.source = source.id
        return source

    @classmethod
    def do_fill(cls, creep):
        source = cls._get_source(creep)

        def reset_source():
            del creep.memory.source

        if not creep.pos.isNearTo(source):
            return [ScheduledAction.moveTo(creep, source, reset_source)]

        if source.amount != None:  # dropped resource
            return [ScheduledAction.pickup(creep, source, reset_source)]
        elif source.destroyTime != None:  # ruin
            reset_source()  # we'll drain it to our capacity all in one tick, lets not try taking it again next tick
            return [ScheduledAction.withdraw(creep, source, RESOURCE_ENERGY)]  # TODO: reset_source doesn't work
        elif source.store != None:  # container/storage
            return [ScheduledAction.withdraw(creep, source, RESOURCE_ENERGY)]  # TODO: reset_source doesn't work
        else:  # a source
            return [ScheduledAction.harvest(creep, source)]

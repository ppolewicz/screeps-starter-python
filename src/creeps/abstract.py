from creeps.scheduled_action import ScheduledAction


class AbstractCreep:
    @classmethod
    def do_fill(cls, creep):
        # If we have a saved source, use it
        if creep.memory.source:  # TODO: don't ever use memory, unless we've just reset RAM
            source = Game.getObjectById(creep.memory.source)
        else:
            #source = _.sample(creep.room.find(FIND_RESOURCE))  # TODO: when a creep dies and leaves some energy, go pick it up maybe, but only use one creep to do it
            # Get a random new source and save it
            source = _.sample(creep.room.find(FIND_SOURCES))  # TODO: balance instead of randomizing
            while source.pos.x == 6 and source.pos.y == 44:  # TODO: do not just walk up to a Source Keeper
                source = _.sample(creep.room.find(FIND_SOURCES))
            creep.memory.source = source.id

        def reset_source():
            del creep.memory.source

        if not creep.pos.isNearTo(source):
            return [ScheduledAction.moveTo(creep, source, reset_source)]
        return [ScheduledAction.harvest(creep, source)]

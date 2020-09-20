from creeps.scheduled_action import ScheduledAction
from creeps.abstract import AbstractCreep
from utils import get_thing_at_coordinates
from utils import search_room

# TODO: if you are sitting on it, check if the source is empty, if it's not, hammer it
# TODO: if the source is empty and there is another non-reserved source in that room that can be reached before our current source resets, then switch designated source to that new one and go to it
# TODO: if all sources are empty and we can reach spawn before sources reset + our spawning time, go to the spawn
# TODO: if you are at the spawn, decide whether to recycle itself or renew itself


class Miner(AbstractCreep):
    @classmethod
    def run(cls, creep):
        room = creep.room
        sources = search_room(room, FIND_SOURCES)
        containers = search_room(room, FIND_STRUCTURES, lambda x: x.structureType == STRUCTURE_CONTAINER)
        thing = get_thing_at_coordinates(containers, creep.pos.x, creep.pos.y)  # TODO save CPU via lookAt
        if thing:
            for source in sources:
                if creep.pos.isNearTo(source):
                    return [ScheduledAction.harvest(creep, source)]

        for source in sources:
            # we are on a container, woot
            #if Game.time % 100 < 99:
            #    if creep.pos.isNearTo(source):
            #        return [ScheduledAction.harvest(creep, source)]
            path = creep.room.findPath(source.pos, creep.room.controller.pos, {'ignoreCreeps': True})
            where = path[0]
            if creep.pos.isEqualTo(where.x, where.y):
                # mine regardless of whether there is a container or not
                # other creeps will come and pick it up, use it to build the container
                return [ScheduledAction.harvest(creep, source)]

            thing = get_thing_at_coordinates(containers, where.x, where.y)
            if not thing:
                # oops, no container
                # TODO: build it from here rather than waiting 100 ticks for a room to build, or maybe trigger the room planner?
                return [ScheduledAction.moveTo(creep, room.getPositionAt(where.x, where.y))]  # go there anyway, we'll mine and someone will come build it
            who = room.lookForAt(LOOK_CREEPS, thing.pos)
            if len(who) >= 1:
                # some other creep is currently there
                continue  # lets try another source
            return [ScheduledAction.moveTo(creep, thing)]
        print('WARNING', creep, 'has no source to mine')
        return []

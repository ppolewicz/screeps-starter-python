__pragma__('noalias', 'undefined')

from creeps.scheduled_action import ScheduledAction
from creeps.abstract import AbstractCreep
from utils import get_thing_at_coordinates
from utils import search_room
from utils import part_count

# TODO: if the source is empty and there is another non-reserved source in that room that can be reached before our current source resets, then switch designated source to that new one and go to it
# TODO: if all sources are empty and we can reach spawn before sources reset + our spawning time, go to the spawn
# TODO: if you are at the spawn, decide whether to recycle itself or renew itself


class Miner(AbstractCreep):
    ICON = '⛏️'
    def _run(self):
        super()._run()
        creep = self.creep
        room = creep.room
        sources = search_room(room, FIND_SOURCES)
        containers = search_room(room, FIND_STRUCTURES, lambda x: x.structureType == STRUCTURE_CONTAINER)
        thing = get_thing_at_coordinates(containers, creep.pos.x, creep.pos.y)  # TODO save CPU via lookAt
        if thing:
            for source in sources:
                if creep.pos.isNearTo(source):
                    works = part_count(creep, 'work')
                    #if source.ticksToRegeneration == undefined or source.energy / source.ticksToRegeneration > works * HARVEST_POWER:  # TODO: check for off-by-one
                    #print(creep, source.ticksToRegeneration, source.ticksToRegeneration % (works/5) == 0)
                    actions = []
                    #if creep.store.getCapacity(RESOURCE_ENERGY) > 0 and creep.store[RESOURCE_ENERGY] > 0:
                    #    actions.append(ScheduledAction.drop(creep, RESOURCE_ENERGY))
                    #if creep.store.getCapacity(RESOURCE_ENERGY) > 0 and creep.store.getFreeCapacity(RESOURCE_ENERGY) == 0:
                    #    for s in creep.pos.findInRange(FIND_MY_STRUCTURES, 1):
                    #        if s.structureType != STRUCTURE_LINK:
                    #            continue
                    #        if s.store.getFreeCapacity(RESOURCE_ENERGY) > 0:
                    #            actions.append(
                    #                ScheduledAction.transfer(creep, s, RESOURCE_ENERGY, priority=80)
                    #            )
                    #        break  # only handle one link
                    if source.ticksToRegeneration == undefined or (source.ticksToRegeneration % (works/5) == 0):
                        actions.append(
                            ScheduledAction.harvest(creep, source)
                        )
                    else:
                        pass # conserve CPU
                    return actions

        for source in sources:
            path = creep.room.findPath(source.pos, creep.room.controller.pos, {'ignoreCreeps': True})
            where = path[0]
            if creep.pos.isEqualTo(where.x, where.y):
                # mine regardless of whether there is a container or not
                # other creeps will come and pick it up, use it to build the container
                return [ScheduledAction.harvest(creep, source)]

            who = room.lookForAt(LOOK_CREEPS, where.x, where.y)
            if len(who) >= 1:
                # some other creep is currently there
                if not who[0].my:
                    continue
                if who[0].memory.cls == 'miner':  # and it's a miner!
                    continue  # lets try another source
            return [ScheduledAction.moveTo(creep, room.getPositionAt(where.x, where.y))]
        print('WARNING', creep, 'has no source to mine')
        return []

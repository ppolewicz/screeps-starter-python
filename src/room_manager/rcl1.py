from room_manager.abstract import AbstractRoomManager
from utils import get_first_spawn


class RoomManagerRCL1(AbstractRoomManager):
    MAX_HARVESTERS = 8
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if self.creep_registry.count_of_type(room, 'harvester') < self.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 250:  # wait until source is full (there are no extensions)
                    spawn.createCreep([WORK, CARRY, MOVE, MOVE], "", {'cls': 'harvester'})

    def build(self):
        pass  # do literally nothing

from room_manager.abstract import AbstractRoomManager
from utils import get_first_spawn


class RoomManagerRCL1(AbstractRoomManager):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if self.creep_registry.count_of_type(room, 'harvester') < 4:
                if room.energyAvailable >= 300:  # wait until source is full (there are no extensions)
                    spawn.createCreep([WORK, CARRY, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})

    def build(self):
        pass  # do literally nothing

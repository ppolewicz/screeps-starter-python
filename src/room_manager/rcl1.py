from abstract import AbstractRoomManager

class RoomManagerRCL1(AbstractRoomManager):
    def spawn_creeps(self):
        if not self.room.spawns[0].spawning:
            if len(creep_registry[room]['harvester']) < 4:
                if self.room.energyAvailable >= 300:  # wait until source is full (there are no extensions)
                    self.spawns[0].createCreep([WORK, CARRY, MOVE, MOVE, MOVE], "", {memory: {cls: 'harvester'}})

    def build(self):
        pass  # do literally nothing

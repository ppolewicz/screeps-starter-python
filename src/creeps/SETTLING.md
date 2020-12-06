put settler1 flag on the first waypoint and move it manually as the creep goes over it, unless one is enough

Game.spawns["Spawn1"].spawnCreep([CLAIM, MOVE, MOVE, MOVE, MOVE, MOVE], "settler1", {"memory": {"room": "TARGET_ROOM", "cls": "claimer"}})

tag other creeps with the target room and give them flags if necessary or 
Game.spawns["Spawn1"].spawnCreep([WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "settler2", {"memory": {"room": "TARGET_ROOM", "cls": "harvester"}})
Game.spawns["Spawn1"].spawnCreep([WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "BOB1", {"memory": {"room": "W24N2", "cls": "builder"}})
Game.spawns["Spawn1"].spawnCreep([WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE], "settler17", {"memory": {"room": "W25S1", "cls": "builder"}})

once settler1 claims the room, make a spawn construction site and clear the room description


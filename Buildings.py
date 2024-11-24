from enum import Enum

class BUILDING_GROUP(Enum):
    PRODUCER = 1
    CRAFTER = 2
    CONVERTER = 3
    PASSIVE = 4

class PRODUCER(Enum):
    MINE = 1
    FORESTER = 2
    FARM = 3
    FISHERY = 4

class CRAFTER(Enum):
    LUMBER_MILL = 1
    WORKSHOP = 2
    FOOD_MILL = 3
    TAILOR = 4
    STONE_MASON = 5
    PASTURE = 6
    FORGE = 7
    KITCHEN = 8
    MACHINE_SHOP = 9
    MEDICINE_HUT = 10
    LABORATORY = 11
    STEAM_GENERATOR = 12
    MAGE_TOWER = 13
    MAGIC_FORGE = 14
    ELEMENTAL_REFINERY = 15
    ENCHANTER = 16

class PASSIVE(Enum):
    FIRE_SHRINE = 1
    WATER_SHRINE = 2
    EARTH_SHRINE = 3
    AIR_SHRINE = 4
    WELL = 5
    WATER_PUMP = 6
    STEAM_ENGINE = 7
    RECHARGER = 8
    FIRE_TEMPLE = 9
    WATER_TEMPLE = 10
    AIR_TEMPLE = 11
    EARTH_TEMPLE = 12

class CONVERTER(Enum):
    FUEL = 1

type BUILDING = PRODUCER | CRAFTER | CONVERTER | PASSIVE

#Converts a building type enum to the building group enum
def GetBuildingGroup(type: BUILDING):
    if isinstance(type, PRODUCER):
        return BUILDING_GROUP.PRODUCER
    elif isinstance(type, CRAFTER):
        return BUILDING_GROUP.CRAFTER
    elif isinstance(type, CONVERTER):
        return BUILDING_GROUP.CONVERTER
    elif isinstance(type, PASSIVE):
        return BUILDING_GROUP.PASSIVE
    
    TypeError("Failed to convert building type to group")
from enum import Enum
import Happiness
from Buildings import *
from Items import *

class SUPPLIER(Enum):
    WORKER_TYPE_1 = 1
    WORKER_TYPE_2 = 2
    STEAM = 3
    YELLOW_COIN = 4
    RED_COIN = 5
    BLUE_COIN = 6
    PURPLE_COIN = 7
    PASTURE_UPGRADE = 8
    PASSIVE = 9

#Stores stats about each supplier
supplier_stats = {
    SUPPLIER.WORKER_TYPE_1: {
        "resource": "Worker",
        "work_units": { "base": 0, "per_increment": 1 + Happiness.GetCurrentProductionBoost() },
        "max": 10,
        "min": 1
    },
    SUPPLIER.WORKER_TYPE_2: {
        "resource": "Worker",
        "work_units": { "base": 0.5, "per_increment": 0.5 + Happiness.GetCurrentProductionBoost() },
        "max": 5,
        "min": 1
    },
    SUPPLIER.STEAM: {
        "resource": CRAFTING_ITEM.steam,
        "work_units": { "base": 1, "per_increment": 1 },
        "max": 2
    },
    SUPPLIER.YELLOW_COIN: {
        "resource": "Yellow Coin",
        "increment": 0.5,
        "work_units": { "base": 0, "per_increment": 1 },
        "max": 10
    },
    SUPPLIER.RED_COIN: {
        "resource": "Red Coin",
        "increment": 0.25,
        "work_units": { "base": 0, "per_increment": 1 },
        "max": 10
    },
    SUPPLIER.BLUE_COIN: {
        "resource": "Blue Coin",
        "increment": 0.125,
        "work_units": { "base": 0, "per_increment": 1 },
        "max": 10
    },
    SUPPLIER.PURPLE_COIN: {
        "resource": "Purple Coin",
        "increment": 0.0625,
        "work_units": { "base": 0, "per_increment": 1 },
        "max": 10
    },
    SUPPLIER.PASTURE_UPGRADE: {
        "work_units": { "base": 0, "per_increment": 0.5 },
        "max": 3,
        "min": 3
    },
    SUPPLIER.PASSIVE: {
        "work_units": { "base": 0, "per_increment": 1 },
        "max": 1,
        "min": 1
    },
}

#Stores the valid suppliers for each building type
group_suppliers = {
    BUILDING_GROUP.PRODUCER: [SUPPLIER.WORKER_TYPE_1],
    BUILDING_GROUP.CRAFTER: [SUPPLIER.WORKER_TYPE_2, SUPPLIER.STEAM],
    BUILDING_GROUP.PASSIVE: [SUPPLIER.PASSIVE],
    BUILDING_GROUP.CONVERTER: [],
}

#Stores supplier mods for individual buildings
building_supplier_mods = {
    CRAFTER.LUMBER_MILL: { "enable": [SUPPLIER.YELLOW_COIN] },
    CRAFTER.FOOD_MILL: { "enable": [SUPPLIER.YELLOW_COIN] },
    CRAFTER.TAILOR: { "enable": [SUPPLIER.YELLOW_COIN] },
    CRAFTER.STONE_MASON: { "enable": [SUPPLIER.YELLOW_COIN] },
    CRAFTER.PASTURE: { "enable": [SUPPLIER.YELLOW_COIN, SUPPLIER.PASTURE_UPGRADE], "disable": [SUPPLIER.STEAM] },
    CRAFTER.FORGE: { "enable": [SUPPLIER.YELLOW_COIN] },
    CRAFTER.KITCHEN: { "enable": [SUPPLIER.YELLOW_COIN] },
    PRODUCER.FISHERY: { "enable": [SUPPLIER.WORKER_TYPE_2, SUPPLIER.RED_COIN], "disable": [SUPPLIER.WORKER_TYPE_1] },
    CRAFTER.WORKSHOP: { "enable": [SUPPLIER.RED_COIN] },
    CRAFTER.MACHINE_SHOP: { "enable": [SUPPLIER.RED_COIN] },
    CRAFTER.MEDICINE_HUT: { "enable": [SUPPLIER.RED_COIN], "disable": [SUPPLIER.STEAM] },
    CRAFTER.STEAM_GENERATOR: { "enable": [SUPPLIER.YELLOW_COIN], "disable": [SUPPLIER.STEAM] },
    CRAFTER.LABORATORY: { "enable": [SUPPLIER.RED_COIN], "disable": [SUPPLIER.STEAM] },
    CRAFTER.MAGE_TOWER: { "enable": [SUPPLIER.BLUE_COIN], "disable": [SUPPLIER.STEAM] },
    CRAFTER.MAGIC_FORGE: { "enable": [SUPPLIER.BLUE_COIN] },
    CRAFTER.ELEMENTAL_REFINERY: { "enable": [SUPPLIER.RED_COIN] },
    CRAFTER.ENCHANTER: { "enable": [SUPPLIER.BLUE_COIN], "disable": [SUPPLIER.STEAM] },
    PASSIVE.RECHARGER: { "enable": [SUPPLIER.YELLOW_COIN] },
    PASSIVE.FIRE_TEMPLE: { "enable": [SUPPLIER.RED_COIN] },
    PASSIVE.WATER_TEMPLE: { "enable": [SUPPLIER.BLUE_COIN] },
    PASSIVE.AIR_TEMPLE: { "enable": [SUPPLIER.YELLOW_COIN] },
    PASSIVE.EARTH_TEMPLE: { "enable": [SUPPLIER.PURPLE_COIN] },
}

#Gets the suppliers for the given building
def GetSuppliers(building: BUILDING) -> list[SUPPLIER]:
    group = GetBuildingGroup(building)
    suppliers = group_suppliers[group].copy()

    #Apply mods
    if (building in building_supplier_mods):
        mods = building_supplier_mods[building]
        if ("enable" in mods):
            suppliers += mods["enable"]
        if ("disable" in mods):
            suppliers = [s for s in suppliers if s not in mods["disable"]]
    
    return suppliers

class BuildingConfig():
    building: BUILDING
    optimal: bool

    work_units: int
    suppliers: dict[SUPPLIER, float]
    resources: dict[SUPPLIER, ITEM | str]

    def __init__(self, building: BUILDING, optimal: bool = True) -> None:
        self.building = building
        self.optimal = optimal

        self.work_units = 0
        self.suppliers = dict()
        self.resources = dict()

        suppliers = GetSuppliers(building)
        for supplier in suppliers:
            stats = supplier_stats[supplier]
            
            count = stats.get("min", 1 if stats["work_units"]["base"] > 0 else 0) if optimal else stats["max"]
            
            if (count > 0):
                self.work_units += stats["work_units"]["base"]
                self.work_units += stats["work_units"]["per_increment"] * count
                self.suppliers[supplier] = stats.get("increment", 1) * count
                if "resource" in stats:
                    self.resources[supplier] = stats["resource"]
    
    #Returns a list of supplier resources which are items and their quantities
    def GetItemSuppliers(self) -> dict[ITEM, float]:
        result: dict[ITEM, float] = dict()
        for supplier, resource in self.resources.items():
            if isinstance(resource, NATURAL_RESOURCE | CRAFTING_ITEM | POWER):
                result[resource] = self.suppliers[supplier]
        return result

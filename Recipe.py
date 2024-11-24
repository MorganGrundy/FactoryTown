from Buildings import *
from Items import *

#Base recipe class
class BaseRecipe():
    building: BUILDING
    outputs: dict[ITEM, int]

    inputs: dict[ITEM, int]
    work_units: int

    def __init__(self, outputs: dict[ITEM, int], inputs: dict[ITEM, int], work_units: int):
        self.outputs = outputs
        self.inputs = inputs | {}
        self.work_units = work_units
    
    def __str__(self) -> str:
        result = f"{self.building.name}: Outputs=("
        for item, amount in self.outputs.items():
            result += f"{item.name} = {amount},"
            
        result += "), Inputs=("
        for item, amount in self.inputs.items():
            result += f"{item.name} = {amount},"

        result += f"), WorkUnits = {self.work_units}"
        return result

#Class for managing recipes
class RecipeManager():
    recipes: dict[ITEM, list[BaseRecipe]]

    def __init__(self):
        self.recipes = {}
    
    #Adds the given recipes with the given building
    def Add(self, building: BUILDING, recipes: list[BaseRecipe]):
        for recipe in recipes:
            recipe.building = building
            outputs = recipe.outputs.keys()
            for output in outputs:
                if not output in self.recipes:
                    self.recipes[output] = []
                self.recipes[output].append(recipe)
    
    #Returns the recipes for the given item
    def Get(self, output: ITEM) -> list[BaseRecipe]:
        if output not in self.recipes:
            raise ValueError(f"There is no recipe for the {output}")
        return self.recipes[output]
    
    #Returns the recipes where the the given item it the primary (first) output
    def GetPrimary(self, output: ITEM) -> list[BaseRecipe]:
        if output not in self.recipes:
            raise ValueError(f"There is no recipe for the {output}")
        return [recipe for recipe in self.recipes[output] if next(iter(recipe.outputs)) == output]

manager = RecipeManager()

manager.Add(PRODUCER.MINE, [
    BaseRecipe(outputs={NATURAL_RESOURCE.stone: 2}, inputs={}, work_units=4),
    BaseRecipe(outputs={NATURAL_RESOURCE.coal: 1}, inputs={}, work_units=4),
    BaseRecipe(outputs={NATURAL_RESOURCE.iron_ore: 1}, inputs={}, work_units=4),
    BaseRecipe(outputs={NATURAL_RESOURCE.mana_shard: 1}, inputs={}, work_units=6),
    BaseRecipe(outputs={NATURAL_RESOURCE.fire_stone: 4}, inputs={}, work_units=6),
    BaseRecipe(outputs={NATURAL_RESOURCE.air_stone: 4}, inputs={}, work_units=6),
    BaseRecipe(outputs={NATURAL_RESOURCE.water_stone: 4}, inputs={}, work_units=6),
    BaseRecipe(outputs={NATURAL_RESOURCE.earth_stone: 4}, inputs={}, work_units=6),
    BaseRecipe(outputs={NATURAL_RESOURCE.gold_ore: 1}, inputs={}, work_units=10)
])

manager.Add(PRODUCER.FORESTER, [
    BaseRecipe(outputs={NATURAL_RESOURCE.wood: 1}, inputs={}, work_units=4),
    BaseRecipe(outputs={NATURAL_RESOURCE.apple: 1}, inputs={}, work_units=2),
    BaseRecipe(outputs={NATURAL_RESOURCE.pear: 1}, inputs={}, work_units=2),
    BaseRecipe(outputs={NATURAL_RESOURCE.dragonfruit: 1}, inputs={}, work_units=4)
])

manager.Add(PRODUCER.FARM, [
    BaseRecipe(outputs={NATURAL_RESOURCE.grain: 1}, inputs={}, work_units=2),
    BaseRecipe(outputs={NATURAL_RESOURCE.herb: 1}, inputs={}, work_units=3),
    BaseRecipe(outputs={NATURAL_RESOURCE.sugar: 1}, inputs={}, work_units=4),
    BaseRecipe(outputs={NATURAL_RESOURCE.berries: 1}, inputs={}, work_units=2),
    BaseRecipe(outputs={NATURAL_RESOURCE.carrot: 1}, inputs={}, work_units=3),
    BaseRecipe(outputs={NATURAL_RESOURCE.potato: 1}, inputs={}, work_units=3),
    BaseRecipe(outputs={NATURAL_RESOURCE.tomato: 1}, inputs={}, work_units=3),
    BaseRecipe(outputs={NATURAL_RESOURCE.cotton: 1}, inputs={}, work_units=2),
    BaseRecipe(outputs={NATURAL_RESOURCE.cactus_fruit: 1}, inputs={}, work_units=4),
])

manager.Add(CRAFTER.LUMBER_MILL, [
    BaseRecipe(outputs={CRAFTING_ITEM.planks: 1}, inputs={NATURAL_RESOURCE.wood: 1}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.paper: 2}, inputs={NATURAL_RESOURCE.wood: 1, CRAFTING_ITEM.water: 1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.fluid_pipe: 1}, inputs={NATURAL_RESOURCE.wood: 2}, work_units=2),
])

manager.Add(CRAFTER.FOOD_MILL, [
    BaseRecipe(outputs={CRAFTING_ITEM.flour: 1}, inputs={NATURAL_RESOURCE.grain: 3}, work_units=4),
    #Grain is the best recipe for animal feed (as it has better yield) and no reason not to use it even if already using carrots/potatoes
    BaseRecipe(outputs={CRAFTING_ITEM.animal_feed: 1}, inputs={NATURAL_RESOURCE.grain: 2}, work_units=2),
    #BaseRecipe(outputs={CRAFTING_ITEM.animal_feed: 1}, inputs={NATURAL_RESOURCE.carrot: 2}, work_units=2),
    #BaseRecipe(outputs={CRAFTING_ITEM.animal_feed: 1}, inputs={NATURAL_RESOURCE.potato: 2}, work_units=2),
])

manager.Add(CRAFTER.WORKSHOP, [
    BaseRecipe(outputs={CRAFTING_ITEM.wood_wheel: 1}, inputs={CRAFTING_ITEM.planks: 2}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.cloth: 1}, inputs={NATURAL_RESOURCE.cotton: 2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.cloth: 1}, inputs={CRAFTING_ITEM.wool: 1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.book: 1}, inputs={CRAFTING_ITEM.paper: 4, CRAFTING_ITEM.leather:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.book: 1}, inputs={CRAFTING_ITEM.paper: 4, CRAFTING_ITEM.cloth:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.wood_conveyor_belt: 1}, inputs={NATURAL_RESOURCE.wood: 2, CRAFTING_ITEM.planks:2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.cloth_conveyor_belt: 1}, inputs={CRAFTING_ITEM.wood_conveyor_belt: 1, CRAFTING_ITEM.cloth:1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.cloth_conveyor_belt: 1}, inputs={CRAFTING_ITEM.wood_wheel: 2, CRAFTING_ITEM.cloth:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.wooden_rail: 1}, inputs={CRAFTING_ITEM.planks: 2, NATURAL_RESOURCE.stone:2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.reinforced_plank: 1}, inputs={CRAFTING_ITEM.planks: 1, CRAFTING_ITEM.iron_plate:1, CRAFTING_ITEM.nails:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.wood_axe: 1}, inputs={CRAFTING_ITEM.planks: 1, CRAFTING_ITEM.iron_plate:1}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.pickaxe: 1}, inputs={CRAFTING_ITEM.reinforced_plank: 1, CRAFTING_ITEM.iron_plate:1}, work_units=12),
])

manager.Add(CRAFTER.TAILOR, [
    BaseRecipe(outputs={CRAFTING_ITEM.shirt: 1}, inputs={CRAFTING_ITEM.cloth: 2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.cloak: 1}, inputs={CRAFTING_ITEM.cloth: 2, CRAFTING_ITEM.leather:2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.warm_coat: 1}, inputs={CRAFTING_ITEM.wool: 2, CRAFTING_ITEM.leather:1, CRAFTING_ITEM.shirt:1}, work_units=12),
    BaseRecipe(outputs={CRAFTING_ITEM.shoe: 1}, inputs={CRAFTING_ITEM.nails: 2, CRAFTING_ITEM.leather:2}, work_units=5),
])

manager.Add(CRAFTER.STONE_MASON, [
    BaseRecipe(outputs={CRAFTING_ITEM.stone_brick: 1}, inputs={NATURAL_RESOURCE.stone: 3}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.polished_stone: 1}, inputs={NATURAL_RESOURCE.stone: 10}, work_units=10),
])

manager.Add(CRAFTER.PASTURE, [
    BaseRecipe(outputs={CRAFTING_ITEM.egg: 1}, inputs={CRAFTING_ITEM.animal_feed: 1}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.raw_chicken: 1}, inputs={CRAFTING_ITEM.animal_feed: 2}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.fertilizer: 1}, inputs={CRAFTING_ITEM.animal_feed: 1, CRAFTING_ITEM.water:1}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.wool: 1, CRAFTING_ITEM.fertilizer: 1}, inputs={CRAFTING_ITEM.animal_feed: 2, CRAFTING_ITEM.water:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.leather: 1, CRAFTING_ITEM.fertilizer: 1}, inputs={CRAFTING_ITEM.animal_feed: 4, CRAFTING_ITEM.water:4}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.beef: 1, CRAFTING_ITEM.fertilizer: 1}, inputs={CRAFTING_ITEM.animal_feed: 4, CRAFTING_ITEM.water:4}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.milk: 1, CRAFTING_ITEM.fertilizer: 1}, inputs={CRAFTING_ITEM.animal_feed: 2, CRAFTING_ITEM.water:2}, work_units=2),
])

manager.Add(CRAFTER.FORGE, [
    BaseRecipe(outputs={CRAFTING_ITEM.iron_plate: 1}, inputs={NATURAL_RESOURCE.iron_ore: 2, CRAFTING_ITEM.fuel:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.gold_ingot: 1}, inputs={NATURAL_RESOURCE.gold_ore: 4, CRAFTING_ITEM.fuel:4}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.nails: 1}, inputs={NATURAL_RESOURCE.iron_ore: 1, CRAFTING_ITEM.fuel:1}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.steam_pipe: 1}, inputs={NATURAL_RESOURCE.iron_ore: 1, CRAFTING_ITEM.fuel:1}, work_units=3),
])

manager.Add(CONVERTER.FUEL, [
    BaseRecipe(outputs={CRAFTING_ITEM.fuel: 1}, inputs={CRAFTING_ITEM.fertilizer: 1}, work_units=0),
    BaseRecipe(outputs={CRAFTING_ITEM.fuel: 2}, inputs={NATURAL_RESOURCE.wood: 1}, work_units=0),
    BaseRecipe(outputs={CRAFTING_ITEM.fuel: 4}, inputs={NATURAL_RESOURCE.coal: 1}, work_units=0),
    BaseRecipe(outputs={CRAFTING_ITEM.fuel: 8}, inputs={CRAFTING_ITEM.magma: 1}, work_units=0),
])

manager.Add(CRAFTER.KITCHEN, [
    BaseRecipe(outputs={CRAFTING_ITEM.bread: 1}, inputs={CRAFTING_ITEM.flour: 2, CRAFTING_ITEM.fuel:1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.cooked_beef: 1}, inputs={CRAFTING_ITEM.beef: 1, CRAFTING_ITEM.fuel:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.cooken_chicken: 1}, inputs={CRAFTING_ITEM.raw_chicken: 1, CRAFTING_ITEM.fuel:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.cooked_fish: 1}, inputs={NATURAL_RESOURCE.fish: 1, CRAFTING_ITEM.fuel:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.apple_juice: 1}, inputs={NATURAL_RESOURCE.apple: 2}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.pear_juice: 1}, inputs={NATURAL_RESOURCE.pear: 2}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.berry_juice: 1}, inputs={NATURAL_RESOURCE.berries: 2}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.apple_jam: 1}, inputs={NATURAL_RESOURCE.apple: 4, NATURAL_RESOURCE.sugar:1, CRAFTING_ITEM.fuel:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.pear_jam: 1}, inputs={NATURAL_RESOURCE.pear: 4, NATURAL_RESOURCE.sugar:1, CRAFTING_ITEM.fuel:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.berry_jam: 1}, inputs={NATURAL_RESOURCE.berries: 4, NATURAL_RESOURCE.sugar:1, CRAFTING_ITEM.fuel:1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.dragon_punch: 1}, inputs={NATURAL_RESOURCE.dragonfruit: 1, CRAFTING_ITEM.berry_juice:1, CRAFTING_ITEM.apple_juice:1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.cactus_jam: 1}, inputs={NATURAL_RESOURCE.cactus_fruit: 1, CRAFTING_ITEM.pear_juice:1, NATURAL_RESOURCE.sugar:1, CRAFTING_ITEM.fuel:2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.butter: 1}, inputs={CRAFTING_ITEM.milk: 2}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.cheese: 2}, inputs={CRAFTING_ITEM.milk: 5, CRAFTING_ITEM.cloth:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.veggie_stew: 1}, inputs={NATURAL_RESOURCE.tomato: 1, NATURAL_RESOURCE.potato:1, NATURAL_RESOURCE.carrot:1, CRAFTING_ITEM.fuel:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.fish_stew: 1}, inputs={NATURAL_RESOURCE.fish: 1, NATURAL_RESOURCE.tomato:2, CRAFTING_ITEM.butter:1, CRAFTING_ITEM.fuel:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.meat_stew: 1}, inputs={NATURAL_RESOURCE.potato: 1, NATURAL_RESOURCE.carrot:1, CRAFTING_ITEM.cooked_beef:1, CRAFTING_ITEM.fuel:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.sandwich: 1}, inputs={CRAFTING_ITEM.bread: 1, CRAFTING_ITEM.cheese:1, CRAFTING_ITEM.cooken_chicken:1}, work_units=3),
    BaseRecipe(outputs={CRAFTING_ITEM.apple_pie: 1}, inputs={CRAFTING_ITEM.flour:4, NATURAL_RESOURCE.sugar:2, CRAFTING_ITEM.butter:1, NATURAL_RESOURCE.apple:2, CRAFTING_ITEM.fuel:2}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.cake: 1}, inputs={CRAFTING_ITEM.flour:4, NATURAL_RESOURCE.sugar:2, CRAFTING_ITEM.butter:1, CRAFTING_ITEM.egg:2, CRAFTING_ITEM.fuel:2}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.berry_cake: 1}, inputs={CRAFTING_ITEM.cake:1, CRAFTING_ITEM.apple_jam:2, NATURAL_RESOURCE.sugar:2, NATURAL_RESOURCE.berries:4}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.bread: 1}, inputs={CRAFTING_ITEM.flour:1, NATURAL_RESOURCE.potato:1, CRAFTING_ITEM.fuel:1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.protein_shake: 1}, inputs={CRAFTING_ITEM.milk:1, NATURAL_RESOURCE.sugar:1, CRAFTING_ITEM.egg:1}, work_units=6),
])

manager.Add(PRODUCER.FISHERY, [
    BaseRecipe(outputs={NATURAL_RESOURCE.fish: 1}, inputs={}, work_units=4),
])

manager.Add(CRAFTER.MACHINE_SHOP, [
    BaseRecipe(outputs={CRAFTING_ITEM.gear: 1}, inputs={CRAFTING_ITEM.iron_plate: 1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.iron_wheel: 1}, inputs={CRAFTING_ITEM.iron_plate: 2}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.metal_rail: 1}, inputs={CRAFTING_ITEM.iron_plate: 2, CRAFTING_ITEM.wooden_rail:1}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.metal_rail: 1}, inputs={CRAFTING_ITEM.iron_plate: 2, CRAFTING_ITEM.planks:2, NATURAL_RESOURCE.stone:4}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.mechanical_rail: 1}, inputs={CRAFTING_ITEM.metal_rail: 1, CRAFTING_ITEM.gear:8}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.mechanical_rail: 1}, inputs={CRAFTING_ITEM.iron_plate: 4, CRAFTING_ITEM.planks:2, CRAFTING_ITEM.gear:8}, work_units=12),
    BaseRecipe(outputs={CRAFTING_ITEM.metal_conveyor_belt: 1}, inputs={CRAFTING_ITEM.iron_plate: 2, CRAFTING_ITEM.cloth_conveyor_belt:1, CRAFTING_ITEM.gear:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.metal_conveyor_belt: 1}, inputs={CRAFTING_ITEM.iron_plate: 4, CRAFTING_ITEM.gear:2}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.nails: 2}, inputs={CRAFTING_ITEM.iron_plate: 1}, work_units=2),
    BaseRecipe(outputs={CRAFTING_ITEM.steam_pipe: 2}, inputs={CRAFTING_ITEM.iron_plate: 1}, work_units=2),
])

manager.Add(CRAFTER.MEDICINE_HUT, [
    BaseRecipe(outputs={CRAFTING_ITEM.bandage: 1}, inputs={CRAFTING_ITEM.cloth: 1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.poultice: 1}, inputs={CRAFTING_ITEM.bandage: 1, NATURAL_RESOURCE.herb:2}, work_units=4),
    BaseRecipe(outputs={CRAFTING_ITEM.medical_wrap: 1}, inputs={CRAFTING_ITEM.poultice: 1, CRAFTING_ITEM.ointment:1, CRAFTING_ITEM.cloth:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.remedy: 1}, inputs={NATURAL_RESOURCE.herb: 2, CRAFTING_ITEM.water:1, CRAFTING_ITEM.fuel:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.fish_oil: 1}, inputs={NATURAL_RESOURCE.fish: 1}, work_units=5),
    BaseRecipe(outputs={CRAFTING_ITEM.ointment: 1}, inputs={NATURAL_RESOURCE.herb: 4, CRAFTING_ITEM.fish_oil:2}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.antidote: 1}, inputs={CRAFTING_ITEM.remedy: 2, CRAFTING_ITEM.fish_oil:1, NATURAL_RESOURCE.sugar:1}, work_units=12),
    BaseRecipe(outputs={CRAFTING_ITEM.health_potion: 1, CRAFTING_ITEM.depleted_mana:1}, inputs={CRAFTING_ITEM.remedy: 2, CRAFTING_ITEM.apple_juice:1, CRAFTING_ITEM.mana_crystal:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.elixir: 1, CRAFTING_ITEM.depleted_water:2}, inputs={CRAFTING_ITEM.health_potion: 1, CRAFTING_ITEM.antidote:1, CRAFTING_ITEM.water_crystal:2}, work_units=10),
])

manager.Add(CRAFTER.STEAM_GENERATOR, [
    BaseRecipe(outputs={CRAFTING_ITEM.steam: 2}, inputs={CRAFTING_ITEM.fuel:1, CRAFTING_ITEM.water:1}, work_units=1),
])

manager.Add(PASSIVE.WELL, [
    BaseRecipe(outputs={CRAFTING_ITEM.water: 1}, inputs={}, work_units=2),
])

manager.Add(PASSIVE.WATER_PUMP, [
    BaseRecipe(outputs={CRAFTING_ITEM.water: 2}, inputs={CRAFTING_ITEM.steam: 1}, work_units=1),
    BaseRecipe(outputs={CRAFTING_ITEM.water: 2}, inputs={POWER.rotation_power: 1}, work_units=1),
])

manager.Add(CRAFTER.LABORATORY, [
    BaseRecipe(outputs={CRAFTING_ITEM.natural_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.book: 1, NATURAL_RESOURCE.herb:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.natural_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.natural_knowledge_tome_lv1: 1, CRAFTING_ITEM.fish_oil:1, CRAFTING_ITEM.remedy:1}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.natural_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.natural_knowledge_tome_lv2: 1, CRAFTING_ITEM.health_potion:1, CRAFTING_ITEM.antidote:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.industrial_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.book: 1, CRAFTING_ITEM.iron_plate:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.industrial_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.industrial_knowledge_tome_lv1: 1, CRAFTING_ITEM.iron_wheel:1, CRAFTING_ITEM.steam_pipe:2}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.industrial_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.industrial_knowledge_tome_lv2: 1, CRAFTING_ITEM.metal_rail:1, CRAFTING_ITEM.metal_conveyor_belt:1}, work_units=10),
])

manager.Add(CRAFTER.MAGE_TOWER, [
    BaseRecipe(outputs={CRAFTING_ITEM.magical_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.book: 1, CRAFTING_ITEM.mana_crystal:1, CRAFTING_ITEM.cloak:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.magical_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.magical_knowledge_tome_lv1: 1, CRAFTING_ITEM.mana_brick:1, CRAFTING_ITEM.mana_pipe:1}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.magical_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.magical_knowledge_tome_lv2: 1, CRAFTING_ITEM.magic_robe:1, CRAFTING_ITEM.ward:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.fire_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.enchanted_book: 1, CRAFTING_ITEM.fire_ether:4}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.fire_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.fire_knowledge_tome_lv1: 1, CRAFTING_ITEM.fire_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.fire_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.fire_knowledge_tome_lv2: 1, CRAFTING_ITEM.strength_spellbook:1}, work_units=12),
    BaseRecipe(outputs={CRAFTING_ITEM.water_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.enchanted_book: 1, CRAFTING_ITEM.water_ether:4}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.water_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.water_knowledge_tome_lv1: 1, CRAFTING_ITEM.water_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.water_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.water_knowledge_tome_lv2: 1, CRAFTING_ITEM.cure_spellbook:1}, work_units=12),
    BaseRecipe(outputs={CRAFTING_ITEM.earth_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.enchanted_book: 1, CRAFTING_ITEM.earth_ether:4}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.earth_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.earth_knowledge_tome_lv1: 1, CRAFTING_ITEM.earth_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.earth_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.earth_knowledge_tome_lv2: 1, CRAFTING_ITEM.protection_spellbook:1}, work_units=12),
    BaseRecipe(outputs={CRAFTING_ITEM.air_knowledge_tome_lv1: 1}, inputs={CRAFTING_ITEM.enchanted_book: 1, CRAFTING_ITEM.air_ether:4}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.air_knowledge_tome_lv2: 1}, inputs={CRAFTING_ITEM.air_knowledge_tome_lv1: 1, CRAFTING_ITEM.air_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.air_knowledge_tome_lv3: 1}, inputs={CRAFTING_ITEM.air_knowledge_tome_lv2: 1, CRAFTING_ITEM.stamina_spellbook:1}, work_units=12),
])

manager.Add(PASSIVE.STEAM_ENGINE, [
    BaseRecipe(outputs={POWER.rotation_power: 2}, inputs={CRAFTING_ITEM.steam:1}, work_units=1),
])

manager.Add(CRAFTER.MAGIC_FORGE, [
    BaseRecipe(outputs={CRAFTING_ITEM.mana_crystal: 1}, inputs={NATURAL_RESOURCE.mana_shard:2, CRAFTING_ITEM.fuel:10}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.mana_brick: 1}, inputs={CRAFTING_ITEM.stone_brick:1, CRAFTING_ITEM.mana_crystal:1, CRAFTING_ITEM.fuel:12}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.mana_pipe: 4}, inputs={CRAFTING_ITEM.steam_pipe:1, CRAFTING_ITEM.mana_crystal:1, CRAFTING_ITEM.fuel:8}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.omnipipe: 2}, inputs={CRAFTING_ITEM.mana_pipe:2, CRAFTING_ITEM.omnistone:1, CRAFTING_ITEM.fuel:20}, work_units=10),
])

manager.Add(CRAFTER.ELEMENTAL_REFINERY, [
    BaseRecipe(outputs={CRAFTING_ITEM.fire_ether:4, CRAFTING_ITEM.depleted_mana:1}, inputs={NATURAL_RESOURCE.fire_stone:4, CRAFTING_ITEM.mana_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.water_ether:4, CRAFTING_ITEM.depleted_mana:1}, inputs={NATURAL_RESOURCE.water_stone:4, CRAFTING_ITEM.mana_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.earth_ether:4, CRAFTING_ITEM.depleted_mana:1}, inputs={NATURAL_RESOURCE.earth_stone:4, CRAFTING_ITEM.mana_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.air_ether:4, CRAFTING_ITEM.depleted_mana:1}, inputs={NATURAL_RESOURCE.air_stone:4, CRAFTING_ITEM.mana_crystal:1}, work_units=10),
])

manager.Add(CRAFTER.ENCHANTER, [
    BaseRecipe(outputs={CRAFTING_ITEM.ward:1, CRAFTING_ITEM.depleted_mana:1}, inputs={CRAFTING_ITEM.reinforced_plank:1, CRAFTING_ITEM.polished_stone:1, CRAFTING_ITEM.mana_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.magic_cloak:1, CRAFTING_ITEM.depleted_mana:2}, inputs={CRAFTING_ITEM.cloak:1, CRAFTING_ITEM.wool:1, CRAFTING_ITEM.mana_crystal:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.magic_robe:1, CRAFTING_ITEM.depleted_mana:2}, inputs={CRAFTING_ITEM.shirt:1, CRAFTING_ITEM.leather:1, CRAFTING_ITEM.mana_crystal:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.fire_ring:1, CRAFTING_ITEM.depleted_fire:2}, inputs={CRAFTING_ITEM.gold_ingot:1, CRAFTING_ITEM.polished_stone:2, CRAFTING_ITEM.fire_crystal:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.water_ring:1, CRAFTING_ITEM.depleted_water:2}, inputs={CRAFTING_ITEM.gold_ingot:1, CRAFTING_ITEM.polished_stone:2, CRAFTING_ITEM.water_crystal:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.crown:1, CRAFTING_ITEM.depleted_air:2}, inputs={CRAFTING_ITEM.gold_ingot:2, CRAFTING_ITEM.iron_plate:2, CRAFTING_ITEM.air_crystal:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.necklace:1, CRAFTING_ITEM.depleted_earth:2}, inputs={CRAFTING_ITEM.polished_stone:2, CRAFTING_ITEM.iron_plate:2, CRAFTING_ITEM.earth_crystal:2}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.magic_rail:1, CRAFTING_ITEM.depleted_fire:1}, inputs={CRAFTING_ITEM.metal_rail:1, CRAFTING_ITEM.fire_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.magic_conveyor_belt:1, CRAFTING_ITEM.depleted_air:1}, inputs={CRAFTING_ITEM.metal_conveyor_belt:1, CRAFTING_ITEM.air_crystal:1}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.enchanted_book:1, CRAFTING_ITEM.depleted_mana:1}, inputs={CRAFTING_ITEM.book:1, CRAFTING_ITEM.mana_crystal:1}, work_units=8),
    BaseRecipe(outputs={CRAFTING_ITEM.strength_spellbook:1, CRAFTING_ITEM.depleted_fire:2}, inputs={CRAFTING_ITEM.enchanted_book:1, CRAFTING_ITEM.fire_crystal:2}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.stamina_spellbook:1, CRAFTING_ITEM.depleted_air:2}, inputs={CRAFTING_ITEM.enchanted_book:1, CRAFTING_ITEM.air_crystal:2}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.cure_spellbook:1, CRAFTING_ITEM.depleted_water:2}, inputs={CRAFTING_ITEM.enchanted_book:1, CRAFTING_ITEM.water_crystal:2}, work_units=10),
    BaseRecipe(outputs={CRAFTING_ITEM.protection_spellbook:1, CRAFTING_ITEM.depleted_earth:2}, inputs={CRAFTING_ITEM.enchanted_book:1, CRAFTING_ITEM.earth_crystal:2}, work_units=10),
])

manager.Add(PASSIVE.RECHARGER, [
    BaseRecipe(outputs={CRAFTING_ITEM.mana_crystal:1}, inputs={CRAFTING_ITEM.depleted_mana:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.fire_crystal:1}, inputs={CRAFTING_ITEM.depleted_fire:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.water_crystal:1}, inputs={CRAFTING_ITEM.depleted_water:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.earth_crystal:1}, inputs={CRAFTING_ITEM.depleted_earth:1}, work_units=6),
    BaseRecipe(outputs={CRAFTING_ITEM.air_crystal:1}, inputs={CRAFTING_ITEM.depleted_air:1}, work_units=6),
])

manager.Add(PASSIVE.FIRE_SHRINE, [
    BaseRecipe(outputs={CRAFTING_ITEM.magma:1, CRAFTING_ITEM.depleted_fire:1}, inputs={CRAFTING_ITEM.fire_crystal:1}, work_units=1),
    BaseRecipe(outputs={POWER.fire_boost:1, CRAFTING_ITEM.depleted_fire:1}, inputs={CRAFTING_ITEM.fire_crystal:1}, work_units=1),
])

manager.Add(PASSIVE.WATER_SHRINE, [
    BaseRecipe(outputs={CRAFTING_ITEM.water:4, CRAFTING_ITEM.depleted_water:1}, inputs={CRAFTING_ITEM.water_crystal:1}, work_units=1),
    BaseRecipe(outputs={POWER.water_boost:1, CRAFTING_ITEM.depleted_water:1}, inputs={CRAFTING_ITEM.water_crystal:1}, work_units=1),
])

manager.Add(PASSIVE.AIR_SHRINE, [
    BaseRecipe(outputs={POWER.air_boost:1, CRAFTING_ITEM.depleted_air:1}, inputs={CRAFTING_ITEM.air_crystal:1}, work_units=1),
    BaseRecipe(outputs={POWER.worker_speed_boost:1, CRAFTING_ITEM.depleted_air:1}, inputs={CRAFTING_ITEM.air_crystal:1}, work_units=1),
])

manager.Add(PASSIVE.EARTH_SHRINE, [
    BaseRecipe(outputs={POWER.earth_boost:1, CRAFTING_ITEM.depleted_earth:1}, inputs={CRAFTING_ITEM.earth_crystal:1}, work_units=1),
    BaseRecipe(outputs={POWER.regen_boost:1, CRAFTING_ITEM.depleted_earth:1}, inputs={CRAFTING_ITEM.earth_crystal:1}, work_units=1),
])

manager.Add(PASSIVE.FIRE_TEMPLE, [
    BaseRecipe(outputs={CRAFTING_ITEM.fire_crystal:1}, inputs={CRAFTING_ITEM.fire_ether:8, CRAFTING_ITEM.mana_crystal:2}, work_units=10),
])

manager.Add(PASSIVE.WATER_TEMPLE, [
    BaseRecipe(outputs={CRAFTING_ITEM.water_crystal:1}, inputs={CRAFTING_ITEM.water_ether:8, CRAFTING_ITEM.mana_crystal:2}, work_units=10),
])

manager.Add(PASSIVE.AIR_TEMPLE, [
    BaseRecipe(outputs={CRAFTING_ITEM.air_crystal:1}, inputs={CRAFTING_ITEM.air_ether:8, CRAFTING_ITEM.mana_crystal:2}, work_units=10),
])

manager.Add(PASSIVE.EARTH_TEMPLE, [
    BaseRecipe(outputs={CRAFTING_ITEM.earth_crystal:1}, inputs={CRAFTING_ITEM.earth_ether:8, CRAFTING_ITEM.mana_crystal:2}, work_units=10),
])
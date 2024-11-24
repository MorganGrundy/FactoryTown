import Recipe, WorkUnits
import math
from Buildings import *

class ResourceNode():
    def __init__(self, grow_time_s: int, default_yield: int):
        self.grow_time_s = grow_time_s
        self.default_yield = default_yield
    
    def GetTotalYield() -> int:
        raise NotImplementedError()
    
    def GetConsumptionRequirements(self, consumption_per_s: int) -> dict[str, float]:
        data = {}
        yield_lasts_s = self.GetTotalYield() / consumption_per_s
        data["nodes_needed"] = 1 + self.grow_time_s / yield_lasts_s
        return data

class MineResourceNode(ResourceNode):
    def __init__(self):
        super().__init__(1000, 50)
    
    def GetTotalYield(self) -> int:
        #Default + 400% from pickaxes
        return self.default_yield * 5
    
    def GetConsumptionRequirements(self, consumption_per_s: int) -> dict[str, float]:
        data = {}
        yield_lasts_s = self.GetTotalYield() / consumption_per_s
        data["nodes_needed"] = 1 + self.grow_time_s / yield_lasts_s
        data["pickaxes/sec"] = 1 / yield_lasts_s
        return data

class ForestorResourceNode(ResourceNode):
    def __init__(self, type: str):
        if (type == "wood"):
            super().__init__(500, 10)
        else:
            super().__init__(500, 8)
    
    def GetTotalYield(self) -> int:
        #Default + 100% from planter * 4 for affinity
        return self.default_yield * 2 * 4

class FarmResourceNode(ResourceNode):
    def __init__(self, type: str, water: bool = False, fertilizer: bool = False):
        grow_time_s = 333 if type == "cactus_fruit" else 250
        default_yield = {"grain": 10, "herb": 4, "sugar": 8, "berries": 5, "carrot": 4, "potato": 4, "tomato": 4, "cotton": 5, "cactus_fruit": 20}[type]
        super().__init__(grow_time_s, default_yield)
        
        self.farm_tile = {"grain": 1, "herb": 1, "sugar": 0.5, "berries": 1, "carrot": 1, "potato": 1, "tomato": 0.5, "cotton": 0.5, "cactus_fruit": 0}[type]
        self.water = {"grain": 0.5, "herb": 0.5, "sugar": 2, "berries": 0.5, "carrot": 0.5, "potato": 0.5, "tomato": 1, "cotton": 1, "cactus_fruit": 0}[type] if water else 0
        self.fertilizer = 0 if not fertilizer or type == "cactus_fruit" else 0.5
        self.affinity = {"grain": 2, "herb": 4, "sugar": 2, "berries": 4, "carrot": 4, "potato": 4, "tomato": 4, "cotton": 4, "cactus_fruit": 4}[type]
        
    def GetTotalYield(self) -> int:
        #Default + farm tile + water (if enabled) + fertilizer (if enabled) * affinity
        return (1 + self.farm_tile + self.water + self.fertilizer) * self.default_yield * self.affinity

#Virtual producer class
class VirtualProducer():
    node: ResourceNode
    def __init__(self, type: BUILDING, recipe: Recipe.BaseRecipe):
        self.type = type
        self.recipe = recipe
    
    def GetConsumptionRequirements(self, consumption_per_s: int) -> dict[str, float|int]:
        data = self.node.GetConsumptionRequirements(consumption_per_s)
        total_work = consumption_per_s * self.recipe.work_units
        data["building_needed"] = math.ceil(total_work / WorkUnits.GetMaxConfig(self.type)["work_units"])
        data["work_per"] = total_work / data["building_needed"]
        return data

class Mine(VirtualProducer):
    def __init__(self, recipe: Recipe.BaseRecipe):
        VirtualProducer.__init__(self, PRODUCER.MINE, recipe)
        self.node = MineResourceNode()

class Forestor(VirtualProducer):
    def __init__(self, recipe: Recipe.BaseRecipe):
        VirtualProducer.__init__(self, PRODUCER.FORESTER, recipe)
        outputs = list(recipe.outputs.keys())
        if len(outputs) != 1:
            raise ValueError("Expected a single output")
        self.node = ForestorResourceNode(outputs[0])

class Farm(VirtualProducer):
    def __init__(self, recipe: Recipe.BaseRecipe):
        VirtualProducer.__init__(self, PRODUCER.FARM, recipe)
        outputs = list(recipe.outputs.keys())
        if len(outputs) != 1:
            raise ValueError("Expected a single output")
        self.node = FarmResourceNode(outputs[0])

#Returns the producer type and recipe
def GetProducer(output: str) -> VirtualProducer:
    recipes = Recipe.manager.Get(output)
    if len(recipes) != 1:
        raise ValueError("Expected a single recipe")
    recipe = recipes[0]

    if recipe.building == PRODUCER.MINE:
        return Mine(recipe.recipe)
    elif recipe.building == PRODUCER.FORESTER:
        return Forestor(recipe.recipe)
    elif recipe.building == PRODUCER.FARM:
        return Farm(recipe.recipe)
    else:
        raise ValueError("No producer for the given output")
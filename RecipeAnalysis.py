import Recipe, WorkUnits, Buildings, Speciality
from Items import *
from collections import deque
from datetime import datetime
import math
from typing import TypeVar
import ProductionChain_Sorting

#Stores relations (producers and consumers) for a given item in a production line
class ItemRelations():
    item: ITEM

    #Stores the recipe which is the primary producer for this item
    primaryProducer: Recipe.BaseRecipe | None
    #Stores non-primary recipes producing this item
    secondaryProducers: list[Recipe.BaseRecipe]

    #Stores recipes consuming this item
    consumers: list[Recipe.BaseRecipe]

    def __init__(self, item: ITEM) -> None:
        self.item = item
        self.primaryProducer = None
        self.secondaryProducers = []
        self.consumers = []
    
    def copy(self):
        obj = ItemRelations(self.item)
        obj.primaryProducer = self.primaryProducer
        obj.secondaryProducers = self.secondaryProducers.copy()
        obj.consumers = self.consumers.copy()
        return obj
    
    def GetAllProducers(self) -> list[Recipe.BaseRecipe]:
        producers = self.secondaryProducers.copy()
        if self.primaryProducer:
            producers.append(self.primaryProducer)
        return producers

class ItemProductionData():
    item: ITEM

    #Stores the amount of this item required by each consumer (a recipe or None for outputs from the production line)
    consumerRequires: dict[None | Recipe.BaseRecipe, float]
    #Stores the total amount of this item required
    required: float
    #Stores history of changes to toal required
    requiredDiffHistory: list[float]

    #Stores the amount of this item achieved by each producer
    producerAchieved: dict[Recipe.BaseRecipe, float]
    #Stores the total amount of this item produced
    achieved: float

    #Stores the circular depth of this item
    circularDepth: int

    def __init__(self, item: ITEM, circularDepth: int) -> None:
        self.item = item

        self.consumerRequires = {}
        self.required = 0
        self.requiredDiffHistory = []
        self.producerAchieved = {}
        self.achieved = 0

        self.circularDepth = circularDepth
        
    def __str__(self) -> str:
        result = f"{self.item} = {self.achieved}"
        return result
    
    #Sets the amount of this item consumed by the given consumer (recipe or None for outputs from the production line)
    def SetConsumption(self, cycle: int, quantity: float, recipe: Recipe.BaseRecipe | None):
        diff = quantity
        if recipe in self.consumerRequires:
            diff -= self.consumerRequires[recipe]
        else:
            self.consumerRequires[recipe] = 0
        
        while len(self.requiredDiffHistory) <= cycle:
            self.requiredDiffHistory.append(0)
            
        if len(self.requiredDiffHistory) == cycle + 1:
            self.requiredDiffHistory[cycle] += diff
        else:
            raise ValueError(f"Tried to set consumption with cycle {cycle} when required diff history length was {len(self.requiredDiffHistory)}")

        self.consumerRequires[recipe] += diff
        self.required += diff
    
    #Sets the amount of this item produced by the given producer
    def SetProduced(self, quantity: float, recipe: Recipe.BaseRecipe):
        diff = quantity
        if recipe in self.producerAchieved:
            diff -= self.producerAchieved[recipe]
        else:
            self.producerAchieved[recipe] = 0

        self.producerAchieved[recipe] += diff
        self.achieved += diff
    
    #Returns whether the requirement history shows divergence
    def IsDiverging(self):
        #Requirements are out of sync by circular depth cycles
        #Wait that many cycles before checking for divergence
        
        indexA = len(self.requiredDiffHistory) - 1
        indexB = indexA - 1
        count = 0
        while indexB >= self.circularDepth and count < 5:
            if self.requiredDiffHistory[indexA] >= self.requiredDiffHistory[indexB]:
                return True
            count += 1
            indexA -= 1
            indexB -= 1

        return False
    
    #Returns whether the given item requirements are satisfied
    def IsSatisfied(self):
        return self.achieved >= self.required

######################################################################################################################################################

class ProductionStats():
    #Number of buildings for each recipe
    buildingsPerRecipe: dict[Recipe.BaseRecipe, int]
    #Number of each work unit suppliers for each recipe
    suppliersPerRecipe: dict[Recipe.BaseRecipe, dict[WorkUnits.SUPPLIER, float]]
    #Total number of each work unit suppliers
    totalSuppliers: dict[WorkUnits.SUPPLIER, float]
    #Items that aren't consumed at all and their quantity
    wasteItems: dict[ITEM, int]
    #The amount each item is overproduced
    overproduced: dict[ITEM, int]
    #The amount of each base input
    baseResources: dict[NATURAL_RESOURCE, int]

    def __init__(self) -> None:
        self.buildingsPerRecipe = dict()
        self.suppliersPerRecipe = dict()
        self.totalSuppliers = dict()
        self.wasteItems = dict()
        self.overproduced = dict()
        self.baseResources = dict()
    
    def __str__(self) -> str:
        result = "Supplies: ("
        workers = 0
        if WorkUnits.SUPPLIER.WORKER_TYPE_1 in self.totalSuppliers:
            workers += self.totalSuppliers[WorkUnits.SUPPLIER.WORKER_TYPE_1]
        if WorkUnits.SUPPLIER.WORKER_TYPE_2 in self.totalSuppliers:
            workers += self.totalSuppliers[WorkUnits.SUPPLIER.WORKER_TYPE_2]
        if workers > 0:
            result += f"Workers: {workers}, "
        for supplier, amount in self.totalSuppliers.items():
            if supplier != WorkUnits.SUPPLIER.WORKER_TYPE_1 and supplier != WorkUnits.SUPPLIER.WORKER_TYPE_2:
                result += f"{supplier}: {amount}, "
        result += ")\nWaste: ("
        for item, amount in self.wasteItems.items():
            result += f"{item}: {amount}, "
        result += ")\nOverproduced: ("
        for item, amount in self.overproduced.items():
            result += f"{item}: {amount}, "
        result += ")\nBase Resources: ("
        for item, amount in self.baseResources.items():
            result += f"{item}: {amount}, "
        result += ")\n"
        return result

######################################################################################################################################################

class ProductionLine():
    target: ITEM
    recipes: list[Recipe.BaseRecipe]
    group_id: int

    #Stores the work unit building configs of each building
    buildingConfigs: dict[Buildings.BUILDING, WorkUnits.BuildingConfig]
    #Stores the speciality each recipe is using
    recipeSpecialities: dict[Recipe.BaseRecipe, Speciality.SPECIALITY]
    
    #Stores the item relations for each item
    itemRelations: dict[ITEM, ItemRelations]

    #Maps from each item to the ItemProductionData class
    itemData: dict[ITEM, ItemProductionData]

    #Stores whether this production chain is valid
    valid: bool

    #Stores stats about this production chain
    stats: ProductionStats | None

    def __init__(self, target: ITEM) -> None:
        self.target = target
        self.recipes = []
        self.group_id = -1
        self.buildingConfigs = dict()
        self.recipeSpecialities = dict()
        self.itemRelations = dict()
        self.itemData = dict()
        self.valid = True
        self.stats = None
    
    def copy(self):
        obj = ProductionLine(self.target)
        obj.recipes = self.recipes.copy()
        obj.group_id = self.group_id
        obj.buildingConfigs = self.buildingConfigs.copy()
        obj.recipeSpecialities = self.recipeSpecialities.copy()
        for item, relation in self.itemRelations.items():
            obj.itemRelations[item] = relation.copy()
        obj.itemData = self.itemData.copy()
        obj.valid = self.valid
        return obj
    
    def HasRecipe(self, recipe: Recipe.BaseRecipe) -> bool:
        return recipe in self.recipes
    
    #Returns all the inputs and resources for the given recipe
    def GetInputsAndResource(self, recipe: Recipe.BaseRecipe) -> set[ITEM]:
        if recipe.building not in self.buildingConfigs:
            self.buildingConfigs[recipe.building] = WorkUnits.BuildingConfig(recipe.building)
        
        return set(recipe.inputs.keys()).union(self.buildingConfigs[recipe.building].GetItemSuppliers().keys())
    
    #Adds the given recipe to the production line
    #Returns a list of the input items and building resources
    def AddRecipe(self, recipe: Recipe.BaseRecipe) -> list[ITEM]:
        #Recipe already added
        if recipe in self.recipes:
            raise ValueError("Recipe already exists")
        
        self.recipes.append(recipe)

        primaryOutput = next(iter(recipe.outputs))

        if recipe.building not in self.buildingConfigs:
            self.buildingConfigs[recipe.building] = WorkUnits.BuildingConfig(recipe.building)

        #Set items primary producer
        if primaryOutput not in self.itemRelations:
            self.itemRelations[primaryOutput] = ItemRelations(primaryOutput)
        self.itemRelations[primaryOutput].primaryProducer = recipe

        #Set as secondary producer for other output items
        for item in list(recipe.outputs.keys()):
            if item == primaryOutput:
                continue
            if item not in self.itemRelations:
                self.itemRelations[item] = ItemRelations(item)
            self.itemRelations[item].secondaryProducers.append(recipe)

        inputsAndResources = self.GetInputsAndResource(recipe)
        #Set as consumer for input items and resources
        for item in inputsAndResources:
            if item not in self.itemRelations:
                self.itemRelations[item] = ItemRelations(item)
            self.itemRelations[item].consumers.append(recipe)
        
        #Returns input items (including building resources)
        return inputsAndResources
    
    #Returns whether the production line is valid based on various conditions
    def Validate(self) -> bool:
        #Contains recipes
        if not self.recipes:
            return False
        
        #All items are in the item relations
        for recipe in self.recipes:
            for item in list(recipe.inputs.keys()):
                if item not in self.itemRelations:
                    return False
            
        return True

    def __str__(self) -> str:
        result = f"{self.target} - Group ID: {self.group_id}\n"
        for recipe in self.recipes:
            if recipe in self.recipeSpecialities:
                result += f"{self.recipeSpecialities[recipe]}, "
            if self.stats and recipe in self.stats.buildingsPerRecipe:
                result += f"(x{self.stats.buildingsPerRecipe[recipe]})"
            result += f"{recipe}\n"
        for itemData in list(self.itemData.values()):
            result += f"{itemData}\n"
        if self.stats:
            result += f"{self.stats}"
        return result
    
    #Returns the speciality boost for the given item
    def GetSpecialityBoost(self, item: ITEM, recipe: Recipe.BaseRecipe) -> float:
        boost = 1
        if recipe in self.recipeSpecialities:
            speciality = self.recipeSpecialities[recipe]
            if speciality in Speciality.GetSpecialities(item, recipe.building):
                boost = Speciality.GetProductionBoost(speciality, 10)
        return boost
    
    #Calculates and returns the depth of each recipe
    def CalculateRecipeDepth(self) -> dict[Recipe.BaseRecipe, int]:
        recipeDepth: dict[Recipe.BaseRecipe, int] = dict()
        #Returns the percentage of the output consumers with a depth set
        def GetDepthPercentage(recipe: Recipe.BaseRecipe) -> float:
            if recipe == self.itemRelations[self.target].primaryProducer: # Always want the target item primary producer to be first
                return 2
            totalConsumer = 0
            consumerWithDepth = 0
            seenRecipe: set[Recipe.BaseRecipe] = set() # Don't count a recipe multiple times for multiple items
            for output in list(recipe.outputs.keys()):
                for consumer in self.itemRelations[output].consumers:
                    if not consumer in seenRecipe:
                        seenRecipe.add(consumer)
                        totalConsumer += 1
                        if consumer in recipeDepth:
                            consumerWithDepth += 1
            if totalConsumer == 0:
                return 1
            return consumerWithDepth / totalConsumer

        nextRecipes: list[Recipe.BaseRecipe] = self.recipes.copy()
        while nextRecipes:
            #Sort recipes by percentage of output consumers with a depth set
            nextRecipes = sorted(nextRecipes, key=lambda x: GetDepthPercentage(x), reverse=True)

            recipe = nextRecipes.pop(0)
            #Find the max depth of the output consumers
            maxDepthOfOutputConsumers = -1
            for output in list(recipe.outputs.keys()):
                for consumer in self.itemRelations[output].consumers:
                    if consumer in recipeDepth:
                        maxDepthOfOutputConsumers = max(maxDepthOfOutputConsumers, recipeDepth[consumer])
            
            #Recipe depth is max of output consumers + 1
            #If there are no output consumers this will give 0
            recipeDepth[recipe] = maxDepthOfOutputConsumers + 1
        
        return recipeDepth
    
    #Calculates and returns the depth of each item
    def CalculateItemDepth(self, recipeDepth: dict[Recipe.BaseRecipe, int]) -> dict[ITEM, int]:
        itemDepth: dict[ITEM, int] = dict()
        
        #Item depth = Max depth of their producers
        for item, relation in self.itemRelations.items():
            maxDepthOfProducers = -1
            for producer in relation.GetAllProducers():
                maxDepthOfProducers = max(maxDepthOfProducers, recipeDepth[producer])
            itemDepth[item] = maxDepthOfProducers
        
        return itemDepth
    
    #Returns which items are circular (where the item depth is less than one of it's consumers depth)
    def GetCircularItems(self, recipeDepth: dict[Recipe.BaseRecipe, int], itemDepth: dict[ITEM, int]) -> set[ITEM]:
        circularItems: set[ITEM] = set()
        for item, depth in itemDepth.items():
            for consumer in self.itemRelations[item].consumers:
                if depth < recipeDepth[consumer]:
                    circularItems.add(item)
                    break
        return circularItems
    
    #Calculates and returns the circular depth of each item
    def CalculateCircularDepth(self, circularItems: set[ITEM]) -> dict[ITEM, int]:
        circularDepth: dict[ITEM, int] = dict()
        for item in list(self.itemRelations.keys()):
            circularDepth[item] = 0
        #For each circular item, traverse the chain down through it's producers
        #Increment the circular depth of each item as we traverse
        #Visiting each item only once per circular item
        for startItem in circularItems:
            seenItems: set[ITEM] = set([startItem])
            nextItems: deque[ITEM] = deque([startItem])
            while nextItems:
                item = nextItems.popleft()
                circularDepth[item] += 1
                for producer in self.itemRelations[item].GetAllProducers():
                    for consumedItem in self.GetInputsAndResource(producer):
                        if consumedItem not in seenItems:
                            seenItems.add(consumedItem)
                            nextItems.append(consumedItem)

        return circularDepth

    #Updates the given item
    #Returns: -1 for divergence, 0 for had changes, 1 for no changes
    def UpdateItem(self, target: ITEM, cycle: int) -> int:
        itemData = self.itemData[target]
        #Check for convergence or divergence
        if itemData.IsDiverging():
            return -1
        
        itemRelation = self.itemRelations[target]
        #Circular recipes can have no primary producer
        if not itemRelation.primaryProducer:
            return 1
        
        #Calculate the amount to produce in the primary producer (reduce total by secondary producer amounts)
        needToProduce = itemData.required
        for recipe in itemRelation.secondaryProducers:
            if recipe in itemData.producerAchieved:
                needToProduce -= itemData.producerAchieved[recipe]
        
        diffFromPrimaryProducer = needToProduce
        if itemRelation.primaryProducer in itemData.producerAchieved:
            diffFromPrimaryProducer -= itemData.producerAchieved[itemRelation.primaryProducer]
            
        #print(f"{target} = {itemData.required}, {needToProduce}, {diffFromPrimaryProducer}")

        #Update primary producer, only update if the differene is substantial enough
        if needToProduce > 0 and abs(diffFromPrimaryProducer) > 0.0000001:
            #Reduce amount needed to produce by speciality boost
            needToProduce /= self.GetSpecialityBoost(target, itemRelation.primaryProducer)
            scale = needToProduce / itemRelation.primaryProducer.outputs[target]
            work_units = scale * itemRelation.primaryProducer.work_units

            #Get the building resources
            buildingResources: dict[ITEM, float] = dict()
            buildings: int = 1
            if work_units > 0:
                buildingConfig = self.buildingConfigs[itemRelation.primaryProducer.building]
                if buildingConfig.work_units > 0:
                    buildings = work_units / buildingConfig.work_units #Allow partial buildings for the resource calculations
                    buildingResources = self.buildingConfigs[itemRelation.primaryProducer.building].GetItemSuppliers()
            
            #Set production of outputs (boosted by speciality boost)
            for item, amount in itemRelation.primaryProducer.outputs.items():
                self.itemData[item].SetProduced(scale * amount * self.GetSpecialityBoost(item, itemRelation.primaryProducer), itemRelation.primaryProducer)
            #Set consumption of inputs
            for item, amount in itemRelation.primaryProducer.inputs.items():
                self.itemData[item].SetConsumption(cycle, scale * amount, itemRelation.primaryProducer)
            #Set consumption of building resource
            for item, amount in buildingResources.items():
                self.itemData[item].SetConsumption(cycle, buildings * amount, itemRelation.primaryProducer)
                
            return 0
        
        #Always return 0 instead of 1 until we reach the circular depth
        return cycle > itemData.circularDepth
    
    #Calculates the production of every recipe to achieve the given amount of the target item
    def CalculateItemData(self, amount: int):
        #Calculate depths
        recipeDepth = self.CalculateRecipeDepth()
        itemDepth = self.CalculateItemDepth(recipeDepth)
        circularItems = self.GetCircularItems(recipeDepth, itemDepth)
        circularDepth = self.CalculateCircularDepth(circularItems)

        #Create item data
        self.itemData = dict()
        for item, relations in self.itemRelations.items():
            self.itemData[item] = ItemProductionData(item, circularDepth[item])
        
        cycle = 0
        #Set output consumption of target item
        self.itemData[self.target].SetConsumption(cycle, amount, None)

        #Get item list and sort by ascending depth, ascending circular depth
        items = list(self.itemRelations.keys())
        items.sort(key=lambda x: (itemDepth[x], circularDepth[x]))
        
        #Repeat until either all items stop changing (for two cycles) or any diverges
        hadChanges = True
        cyclesSinceLastChange = 0
        while cyclesSinceLastChange < 2:
            hadChanges = False
            #Update each item
            for item in items:
                updateResult = self.UpdateItem(item, cycle)
                if updateResult == -1:
                    self.valid = False
                    return
                elif updateResult == 0:
                    hadChanges = True
            if not hadChanges:
                cyclesSinceLastChange += 1
            else:
                cyclesSinceLastChange = 0
            cycle += 1

        #Check that the requirements are all satisfied
        for item, itemData in self.itemData.items():
            missing = itemData.required - itemData.achieved
            if missing > 0.00001:
                self.valid = False
                return
            
        #This shouldn't ever trigger?
        for item, relations in self.itemRelations.items():
            if len(relations.consumers) > 0:
                itemData = self.itemData[item]
                overproduction = itemData.achieved - itemData.required
                if overproduction > 0.00001:
                    raise ValueError("Overproducing")
    
    #Calculates stats for production chain
    def CalculateStats(self):
        if not self.itemData:
            raise ValueError("Item data not calculated")
        
        self.stats = ProductionStats()
        
        for item, itemData in self.itemData.items():
            relations = self.itemRelations[item]
            if itemData.required == 0:
                if itemData.achieved > 0:
                    self.stats.wasteItems[item] = itemData.achieved
            elif itemData.achieved > itemData.required:
                self.stats.overproduced[item] = itemData.required - itemData.achieved
            
            if isinstance(item, NATURAL_RESOURCE):
                self.stats.baseResources[item] = itemData.achieved
            
            for recipe in relations.GetAllProducers():
                if recipe in self.stats.buildingsPerRecipe or isinstance(recipe.building, Buildings.CONVERTER):
                    continue

                optimal_config = self.buildingConfigs[recipe.building]

                scale = 0
                if recipe in itemData.producerAchieved:
                    scale = itemData.producerAchieved[recipe] / recipe.outputs[item]
                    scale /= self.GetSpecialityBoost(next(iter(recipe.outputs.keys())), recipe)
                total_work_units = scale * recipe.work_units
                self.stats.buildingsPerRecipe[recipe] = math.ceil(total_work_units / optimal_config.work_units)

                suppliers: dict[WorkUnits.SUPPLIER, float] = optimal_config.suppliers
                self.stats.suppliersPerRecipe[recipe] = dict()
                for supplier, amount in suppliers.items():
                    if supplier in optimal_config.resources and not isinstance(optimal_config.resources[supplier], NATURAL_RESOURCE | CRAFTING_ITEM | POWER):
                        self.stats.suppliersPerRecipe[recipe][supplier] = amount * self.stats.buildingsPerRecipe[recipe]

                        if supplier not in self.stats.totalSuppliers:
                            self.stats.totalSuppliers[supplier] = 0
                        self.stats.totalSuppliers[supplier] += amount * self.stats.buildingsPerRecipe[recipe]

######################################################################################################################################################

#Sub-function of CreateProductionLines/CreateProductionLines_Internal
#Adds recipe to the chain and links the item as a primary output
#Adds the item to the seen set
#Adds the recipe inputs to the seen set and queue
def CreateProductionLines_AddRecipe(recipe: Recipe.BaseRecipe, itemQueue: deque[ITEM], seenItems: set[ITEM], currentChain: ProductionLine):
    inputItems = currentChain.AddRecipe(recipe)
    seenItems.add(next(iter(recipe.outputs)))

    for item in inputItems:
        if item not in seenItems:
            seenItems.add(item)
            itemQueue.append(item)

#Internal recursive function for CreateProductionLines
#Returns the production chains for the given item
def CreateProductionLines_Internal(itemQueue: deque[ITEM], seenItems: set[ITEM], currentChain: ProductionLine) -> list[ProductionLine]:
    while len(itemQueue) > 0:
        item = itemQueue.popleft()
        recipes = Recipe.manager.GetPrimary(item)

        if len(recipes) == 0:
            #If there are no primary recipes then we either get this item as a byproduct from a recipe added elsewhere or it's not valid
            #We'll determine that later
            #raise ValueError(f"No recipes with {item} as the primary output")
            pass
        elif len(recipes) > 1:
            productionLines: list[ProductionLine] = []
            for recipe in recipes:
                if not currentChain.HasRecipe(recipe):
                    itemQueueCopy = itemQueue.copy()
                    seenItemsCopy = seenItems.copy()
                    currentChainCopy = currentChain.copy()
                    CreateProductionLines_AddRecipe(recipe, itemQueueCopy, seenItemsCopy, currentChainCopy)
                        
                    productionLines += CreateProductionLines_Internal(itemQueueCopy, seenItemsCopy, currentChainCopy)
            return productionLines
        elif not currentChain.HasRecipe(recipes[0]):
            CreateProductionLines_AddRecipe(recipes[0], itemQueue, seenItems, currentChain)

    return [currentChain]

#Returns the production chains for the given item
#Some will be invalid and need filtered out later
def CreateProductionLines(item: ITEM) -> list[ProductionLine]:
    productionLines = CreateProductionLines_Internal(deque([item]), {item}, ProductionLine(item))
    productionLines = [line for line in productionLines if line.Validate()]
    return productionLines

T = TypeVar("T")
T2 = TypeVar("T2")

def MinimiseVariants_Internal(items: deque[tuple[T, set[T2]]], seen: set[T2], current: dict[T, T2]) -> tuple[list[dict[T, T2]], int]:
    while items:
        key, variants = items.popleft()
        #Filter variants to the already seen ones
        selectFromVariants = variants.intersection(seen)
        #If no variants match the already seen then accept the new variants
        if not selectFromVariants:
            selectFromVariants = variants.copy()
        
        if len(selectFromVariants) == 1:
            variant = selectFromVariants.pop()
            seen.add(variant)
            current[key] = variant
        elif len(selectFromVariants) > 1:
            result: list[dict[T, T2]] = []
            seenCount = 9999
            for variant in selectFromVariants:
                itemsCopy = items.copy()
                seenCopy = seen.copy()
                currentCopy = current.copy()
                seenCopy.add(variant)
                currentCopy[key] = variant
                newResult, newSeenCount = MinimiseVariants_Internal(itemsCopy, seenCopy, currentCopy)
                result += newResult
                seenCount = min(seenCount, newSeenCount)
            return result, seenCount
        else:
            raise ValueError("No variants?")
    
    return [current], len(seen)

#Given a dictionary where each entry contains a set of possible values
#Minimises the variation of possible values
#Returning a list of dictionary where the value is a single option from the possible values
def MinimiseVariants(dictOfSet: dict[T, set[T2]]) -> list[dict[T, T2]]:
    result, seenCount = MinimiseVariants_Internal(deque(dictOfSet.items()), set(), dict())

    #result = [x for x in result if len(set(x.values())) <= seenCount]
    return result

#Returns speciality variants of the given production line
#Tries to minimise the total number of specialities
def SpecialiseProductionLine(line: ProductionLine) -> list[ProductionLine]:
    #Find the specialities for each recipe
    recipeSpecialities: dict[Recipe.BaseRecipe, set[Speciality.SPECIALITY]] = dict()
    for recipe in line.recipes:
        recipeSpecialities[recipe] = set()
        for item in list(recipe.outputs.keys()):
            recipeSpecialities[recipe].update(Speciality.GetSpecialities(item, recipe.building))
        if not recipeSpecialities[recipe]:
            del recipeSpecialities[recipe]
    
    minimisedSpecialities = MinimiseVariants(recipeSpecialities)

    productionLines: list[ProductionLine] = []
    for specialityConfig in minimisedSpecialities:
        specialisedLine = line.copy()
        for recipe, speciality in specialityConfig.items():
            specialisedLine.recipeSpecialities[recipe] = speciality
        productionLines.append(specialisedLine)
    return productionLines

def PrintProductionLines(productionLines: list[ProductionLine]):
    for i, chain in enumerate(productionLines):
        print(f"Chain {i}:\n{chain}")

#Writes valid chains to a file
def WriteValidChains(item: ITEM, chains: list[ProductionLine]):
    now = datetime.now()
    nowStr = now.strftime('%d-%m-%y#%H-%M-%S')
    with open(f"Chains\\{item.name}-ValidChains-{nowStr}.txt", "w") as file:
        validChains = 0
        for chain in chains:
            if chain.valid:
                validChains += 1

        file.write(f"{validChains} out of {len(chains)} are valid.\n")
        for i, chain in enumerate(chains):
            if chain.valid:
                file.write(f"Chain {i} is valid:\n{chain}\n")
            else:
                file.write(f"Chain {i} is not valid:\n{chain}\n")

#Returns a list of valid and finalised production lines for the given item
def GetProductionLines(item: ITEM) -> list[ProductionLine]:
    allProductionLines = CreateProductionLines(item)
    specialisedProductionLines: list[ProductionLine] = list()

    #Filter out invalid chains, specialise all the valid ones
    for i, line in enumerate(allProductionLines):
        line.CalculateItemData(2)
        if line.valid:
            line.group_id = i
            specialisedProductionLines.extend(SpecialiseProductionLine(line))
    
    #Calculate item data and stats for specialised production lines
    for i, line in enumerate(specialisedProductionLines):
        line.CalculateItemData(2)
        if not line.valid:
            raise ValueError("Specialised production line became invalid?")
        
        line.CalculateStats()
    
    return specialisedProductionLines

def main():
    targetItem = CRAFTING_ITEM.pickaxe
    productionLines = GetProductionLines(targetItem)

    #Sort by number of workers
    productionLines.sort(key=lambda x: (ProductionChain_Sorting.SortByWorkers(x), ProductionChain_Sorting.SortByRequired(x, NATURAL_RESOURCE.iron_ore), ProductionChain_Sorting.SortByBuildings(x)))

    WriteValidChains(targetItem, productionLines)

    print("Done")

if __name__ == "__main__":
    main()

#TODO:
# - Select a production line
# - Re-calculate with target production
# - Calculate conveyors for each recipes I/O
# - For NATURAL_RESOURCE/producers, calculate number of buildings and nodes (link up with Producers.py)
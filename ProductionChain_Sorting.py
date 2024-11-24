from RecipeAnalysis import ProductionLine
import WorkUnits
from Items import *

#Sorts by complexity/number of recipes
def SortByComplexity(x: ProductionLine) -> int:
    return len(x.recipes)

#Sorts by number of workers
def SortByWorkers(x: ProductionLine) -> int:
    return (x.stats.totalSuppliers[WorkUnits.SUPPLIER.WORKER_TYPE_1] if WorkUnits.SUPPLIER.WORKER_TYPE_1 in x.stats.totalSuppliers else 0) + (x.stats.totalSuppliers[WorkUnits.SUPPLIER.WORKER_TYPE_2] if WorkUnits.SUPPLIER.WORKER_TYPE_2 in x.stats.totalSuppliers else 0)

#Sorts by required amount of given item
def SortByRequired(x: ProductionLine, item: ITEM) -> int:
    return x.itemData[item].achieved if item in x.itemData else 0

#Sorts by number of buildings
def SortByBuildings(x: ProductionLine) -> int:
    return sum(x.stats.buildingsPerRecipe.values())
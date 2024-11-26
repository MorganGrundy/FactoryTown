import ProductionLine
from Items import *

def main():
    targetItem = CRAFTING_ITEM.pickaxe
    productionLines = ProductionLine.GetProductionLines(targetItem)

    #Sort by number of workers
    productionLines.sort(key=lambda x: (ProductionLine.SortByWorkers(x), ProductionLine.SortByRequired(x, NATURAL_RESOURCE.iron_ore), ProductionLine.SortByBuildings(x)))

    ProductionLine.WriteValidChains(targetItem, productionLines)

    print("Done")

if __name__ == "__main__":
    main()

#TODO:
# - Select a production line
# - Re-calculate with target production
# - Calculate conveyors for each recipes I/O
# - For NATURAL_RESOURCE/producers, calculate number of buildings and nodes (link up with Producers.py)
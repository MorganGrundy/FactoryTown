happiness_thresholds = [0, 8, 26, 60, 120, 200, 330, 520, 750, 1050, 1400, 1800]
production_boosts = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.65, 0.8, 1, 1.2, 1.4, 1.6]
if len(happiness_thresholds) != len(production_boosts):
    ValueError("Happiness data is incorrect.")

#Returns the production boost from the given happiness
def GetProductionBoost(happiness: int):
    for idx, threshold in enumerate(happiness_thresholds):
        if happiness < threshold:
            return production_boosts[idx-1]
    return production_boosts[len(production_boosts)-1]

#Returns the production boost from the current happiness
def GetCurrentProductionBoost():
    happiness = 1400
    return GetProductionBoost(happiness)
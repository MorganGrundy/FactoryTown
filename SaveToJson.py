import json

levels = [0, 8, 26, 60, 120, 200, 330, 520, 750, 1050, 1400, 1800]
production_boosts = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.65, 0.8, 1, 1.2, 1.4, 1.6]

data = []
for level, production_boost in zip(levels, production_boosts):
    data.append({"level": level, "production_boost": production_boost})

with open('data/Happiness.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
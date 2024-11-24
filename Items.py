from enum import Enum

NATURAL_RESOURCE = Enum('NATURAL_RESOURCE',
    ['berries','carrot','cotton','grain','herb','potato','sugar', 'tomato', 'cactus_fruit',
     'apple', 'pear', 'dragonfruit','wood','fish','stone','coal','iron_ore','gold_ore','mana_shard',
     'fire_stone','water_stone','earth_stone','air_stone'])

CRAFTING_ITEM = Enum('CRAFTING_ITEM',
    ['water','planks','paper','fluid_pipe','flour','animal_feed','wood_wheel','cloth','book','wood_conveyor_belt',
     'cloth_conveyor_belt','wooden_rail','reinforced_plank','wood_axe','pickaxe','egg','raw_chicken',
     'fertilizer','wool','leather','beef','milk','bread','cooked_beef','cooken_chicken','cooked_fish',
     'apple_juice','pear_juice','berry_juice','apple_jam','pear_jam','berry_jam','dragon_punch',
     'cactus_jam','butter','cheese','veggie_stew','fish_stew','meat_stew','sandwich','apple_pie','cake',
     'berry_cake','protein_shake','stone_brick','polished_stone','shirt','cloak','warm_coat','shoe',
     'bandage','poultice','remedy','fish_oil','ointment','antidote','medical_wrap','health_potion',
     'elixir','natural_knowledge_tome_lv1','natural_knowledge_tome_lv2','natural_knowledge_tome_lv3',
     'industrial_knowledge_tome_lv1','industrial_knowledge_tome_lv2','industrial_knowledge_tome_lv3',
     'gear','iron_wheel','metal_rail','mechanical_rail','metal_conveyor_belt','nails','steam_pipe',
     'iron_plate','gold_ingot','steam','magical_knowledge_tome_lv1',
     'magical_knowledge_tome_lv2','magical_knowledge_tome_lv3','fire_knowledge_tome_lv1',
     'fire_knowledge_tome_lv2','fire_knowledge_tome_lv3','water_knowledge_tome_lv1',
     'water_knowledge_tome_lv2','water_knowledge_tome_lv3','earth_knowledge_tome_lv1',
     'earth_knowledge_tome_lv2','earth_knowledge_tome_lv3','air_knowledge_tome_lv1',
     'air_knowledge_tome_lv2','air_knowledge_tome_lv3','mana_crystal','mana_brick','mana_pipe',
     'omnipipe','ward','magic_cloak','magic_robe','fire_ring','water_ring','crown','necklace',
     'magic_rail','magic_conveyor_belt','enchanted_book','strength_spellbook','cure_spellbook',
     'protection_spellbook','stamina_spellbook','fire_ether','water_ether','earth_ether','air_ether',
     'magma','fire_crystal','water_crystal','earth_crystal','air_crystal','omnistone','fuel',
     'depleted_mana', 'depleted_water', 'depleted_fire', 'depleted_earth', 'depleted_air'])

POWER = Enum('POWER',
    ['rotation_power','fire_boost','water_boost','air_boost','earth_boost',
     'worker_speed_boost','regen_boost'])

type ITEM = NATURAL_RESOURCE | CRAFTING_ITEM | POWER

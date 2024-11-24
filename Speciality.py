from enum import Enum
from Items import *
import Buildings

SPECIALITY = Enum('SPECIALITY', ['FARMING', 'FORESTRY', 'MINING', 'PROCESSING', 'COMMERCE', 'INDUSTRY',
    'KNOWLEDGE', 'ARTISTRY', 'MAGIC'])

#Returns the production boost for the given specialty and town level
def GetProductionBoost(type: SPECIALITY, town_level: int) -> float:
    if type in [SPECIALITY.FARMING, SPECIALITY.FORESTRY, SPECIALITY.MINING]:
        return 1 + min(1, 0.2 * town_level)
    elif type in [SPECIALITY.PROCESSING, SPECIALITY.INDUSTRY, SPECIALITY.KNOWLEDGE, SPECIALITY.ARTISTRY, SPECIALITY.MAGIC]:
        return 1 + min(1, 0.1 * town_level)
    elif type == SPECIALITY.COMMERCE:
        return 0
    raise ValueError("Unexpected speciality")

#Returns the specialities for the given item when produced from the given building
def GetSpecialities(item: ITEM, building: Buildings.BUILDING) -> set[SPECIALITY]:
    result = set()

    #Some buildings are bugged? And don't apply speciality boosts :(
    if building in [Buildings.PASSIVE.RECHARGER, Buildings.PASSIVE.AIR_SHRINE, Buildings.PASSIVE.FIRE_SHRINE, Buildings.PASSIVE.EARTH_SHRINE, Buildings.PASSIVE.WATER_SHRINE, Buildings.PASSIVE.WELL, Buildings.PASSIVE.WATER_PUMP]:
        return result

    if item in [NATURAL_RESOURCE.grain, NATURAL_RESOURCE.herb, NATURAL_RESOURCE.sugar, NATURAL_RESOURCE.berries, NATURAL_RESOURCE.carrot, NATURAL_RESOURCE.potato, NATURAL_RESOURCE.tomato, NATURAL_RESOURCE.cotton, NATURAL_RESOURCE.cactus_fruit,
                CRAFTING_ITEM.egg, CRAFTING_ITEM.raw_chicken, CRAFTING_ITEM.fertilizer, CRAFTING_ITEM.wool, CRAFTING_ITEM.leather, CRAFTING_ITEM.beef, CRAFTING_ITEM.milk,
                NATURAL_RESOURCE.fish]:
        result.add(SPECIALITY.FARMING)
    
    if item in [NATURAL_RESOURCE.apple, NATURAL_RESOURCE.pear, NATURAL_RESOURCE.dragonfruit, NATURAL_RESOURCE.wood,
                CRAFTING_ITEM.planks, CRAFTING_ITEM.fluid_pipe, CRAFTING_ITEM.wood_wheel, CRAFTING_ITEM.wood_axe]:
        result.add(SPECIALITY.FORESTRY)
    
    if item in [CRAFTING_ITEM.planks, CRAFTING_ITEM.fluid_pipe, CRAFTING_ITEM.wood_wheel,
                CRAFTING_ITEM.iron_plate, CRAFTING_ITEM.gold_ingot, CRAFTING_ITEM.stone_brick,
                CRAFTING_ITEM.paper, CRAFTING_ITEM.flour, CRAFTING_ITEM.animal_feed, CRAFTING_ITEM.cloth,
                CRAFTING_ITEM.book, CRAFTING_ITEM.nails, CRAFTING_ITEM.steam_pipe,
                CRAFTING_ITEM.bread, CRAFTING_ITEM.cooked_beef, CRAFTING_ITEM.cooken_chicken, CRAFTING_ITEM.cooked_fish, CRAFTING_ITEM.apple_juice, CRAFTING_ITEM.pear_juice, CRAFTING_ITEM.berry_juice,
                CRAFTING_ITEM.fire_ether, CRAFTING_ITEM.water_ether, CRAFTING_ITEM.earth_ether, CRAFTING_ITEM.air_ether]:
        result.add(SPECIALITY.PROCESSING)
    
    if item in [CRAFTING_ITEM.wood_axe,
                CRAFTING_ITEM.iron_plate, CRAFTING_ITEM.pickaxe, CRAFTING_ITEM.wood_conveyor_belt, CRAFTING_ITEM.cloth_conveyor_belt,
                CRAFTING_ITEM.wooden_rail, CRAFTING_ITEM.reinforced_plank, CRAFTING_ITEM.gear, CRAFTING_ITEM.iron_wheel, CRAFTING_ITEM.metal_rail, CRAFTING_ITEM.mechanical_rail, CRAFTING_ITEM.metal_conveyor_belt,
                CRAFTING_ITEM.steam, CRAFTING_ITEM.nails, CRAFTING_ITEM.steam_pipe,
                CRAFTING_ITEM.water]:
        result.add(SPECIALITY.INDUSTRY)
    
    if item in [NATURAL_RESOURCE.stone, NATURAL_RESOURCE.coal, NATURAL_RESOURCE.iron_ore, NATURAL_RESOURCE.mana_shard, NATURAL_RESOURCE.fire_stone, NATURAL_RESOURCE.earth_stone, NATURAL_RESOURCE.water_stone, NATURAL_RESOURCE.air_stone, NATURAL_RESOURCE.gold_ore,
                CRAFTING_ITEM.iron_plate, CRAFTING_ITEM.gold_ingot, CRAFTING_ITEM.stone_brick, CRAFTING_ITEM.pickaxe]:
        result.add(SPECIALITY.MINING)

    if item in [CRAFTING_ITEM.polished_stone, CRAFTING_ITEM.apple_jam, CRAFTING_ITEM.pear_jam, CRAFTING_ITEM.berry_jam, CRAFTING_ITEM.dragon_punch, CRAFTING_ITEM.cactus_jam, CRAFTING_ITEM.butter, CRAFTING_ITEM.cheese, CRAFTING_ITEM.veggie_stew, CRAFTING_ITEM.fish_stew, CRAFTING_ITEM.meat_stew, CRAFTING_ITEM.sandwich, CRAFTING_ITEM.apple_pie, CRAFTING_ITEM.cake, CRAFTING_ITEM.berry_cake, CRAFTING_ITEM.protein_shake,
                CRAFTING_ITEM.bread, CRAFTING_ITEM.cooked_beef, CRAFTING_ITEM.cooken_chicken, CRAFTING_ITEM.cooked_fish, CRAFTING_ITEM.apple_juice, CRAFTING_ITEM.pear_juice, CRAFTING_ITEM.berry_juice]:
        result.add(SPECIALITY.ARTISTRY)

    if item in [CRAFTING_ITEM.bandage, CRAFTING_ITEM.poultice, CRAFTING_ITEM.medical_wrap, CRAFTING_ITEM.remedy, CRAFTING_ITEM.fish_oil, CRAFTING_ITEM.ointment, CRAFTING_ITEM.antidote,
                CRAFTING_ITEM.natural_knowledge_tome_lv1, CRAFTING_ITEM.natural_knowledge_tome_lv2, CRAFTING_ITEM.natural_knowledge_tome_lv3, CRAFTING_ITEM.industrial_knowledge_tome_lv1, CRAFTING_ITEM.industrial_knowledge_tome_lv2, CRAFTING_ITEM.industrial_knowledge_tome_lv3, CRAFTING_ITEM.magical_knowledge_tome_lv1, CRAFTING_ITEM.magical_knowledge_tome_lv2, CRAFTING_ITEM.magical_knowledge_tome_lv3, CRAFTING_ITEM.fire_knowledge_tome_lv1, CRAFTING_ITEM.fire_knowledge_tome_lv2, CRAFTING_ITEM.fire_knowledge_tome_lv3, CRAFTING_ITEM.water_knowledge_tome_lv1, CRAFTING_ITEM.water_knowledge_tome_lv2, CRAFTING_ITEM.water_knowledge_tome_lv3, CRAFTING_ITEM.earth_knowledge_tome_lv1, CRAFTING_ITEM.earth_knowledge_tome_lv2, CRAFTING_ITEM.earth_knowledge_tome_lv3, CRAFTING_ITEM.air_knowledge_tome_lv1, CRAFTING_ITEM.air_knowledge_tome_lv2, CRAFTING_ITEM.air_knowledge_tome_lv3,
                CRAFTING_ITEM.book, CRAFTING_ITEM.health_potion, CRAFTING_ITEM.elixir, CRAFTING_ITEM.enchanted_book, CRAFTING_ITEM.strength_spellbook, CRAFTING_ITEM.stamina_spellbook, CRAFTING_ITEM.cure_spellbook, CRAFTING_ITEM.protection_spellbook]:
        result.add(SPECIALITY.KNOWLEDGE)

    if item in [CRAFTING_ITEM.ward, CRAFTING_ITEM.magic_cloak, CRAFTING_ITEM.magic_robe, CRAFTING_ITEM.fire_ring, CRAFTING_ITEM.water_ring, CRAFTING_ITEM.crown, CRAFTING_ITEM.necklace, CRAFTING_ITEM.magic_rail, CRAFTING_ITEM.magic_conveyor_belt, CRAFTING_ITEM.magma,
                CRAFTING_ITEM.mana_brick, CRAFTING_ITEM.mana_pipe, CRAFTING_ITEM.omnipipe,
                CRAFTING_ITEM.health_potion, CRAFTING_ITEM.elixir, CRAFTING_ITEM.enchanted_book, CRAFTING_ITEM.strength_spellbook, CRAFTING_ITEM.stamina_spellbook, CRAFTING_ITEM.cure_spellbook, CRAFTING_ITEM.protection_spellbook,
                CRAFTING_ITEM.fire_ether, CRAFTING_ITEM.water_ether, CRAFTING_ITEM.earth_ether, CRAFTING_ITEM.air_ether,
                CRAFTING_ITEM.water, CRAFTING_ITEM.mana_crystal]:
        result.add(SPECIALITY.MAGIC)

    return result

#Map from item to specialities
itemMap = {
    CRAFTING_ITEM.water: [SPECIALITY.MAGIC, SPECIALITY.INDUSTRY],
}

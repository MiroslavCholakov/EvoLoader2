#dictionaries for EvoLoader

MAX_TIER = [
            "Annihilator", "Arch Sage", "Avenger", "Champion", "Dark Arch Templar", "Demon Incarnate",
			"Grand Inquisitor", "Grand Templar", "Hierophant", "Jounin", "Lightbinder", "Light Caster",
			"Master Stalker", "Monster Hunter", "Mystic", "Phantom Assassin", "Professional Witcher", "Prophetess",
			"Rune Master", "Sky Sorceress", "Sniper", "Stargazer", "Summoner", "White Wizard", "Valkyrie",]
default_properties = {
            'gold': 0,
            'shards': 0,
            'code': '',
            'items': [],
            'stash_items': [[]]

        }
ALL_CLASS_LIST = {
            "Annihilator": default_properties.copy(),
            "Arch Sage": default_properties.copy(),
            "Avenger": default_properties.copy(),
            "Champion": default_properties.copy(),
            "Dark Arch Templar": default_properties.copy(),
            "Demon Incarnate": default_properties.copy(),
            "Grand Inquisitor": default_properties.copy(),
            "Grand Templar": default_properties.copy(),
            "Hierophant": default_properties.copy(),
            "Jounin": default_properties.copy(),
            "Lightbinder": default_properties.copy(),
            "Light Caster": default_properties.copy(),
            "Master Stalker": default_properties.copy(),
            "Monster Hunter": default_properties.copy(),
            "Mystic": default_properties.copy(),
            "Phantom Assassin": default_properties.copy(),
            "Professional Witcher": default_properties.copy(),
            "Prophetess": default_properties.copy(),
            "Rune Master": default_properties.copy(),
            "Sky Sorceress": default_properties.copy(),
            "Sniper": default_properties.copy(),
            "Stargazer": default_properties.copy(),
            "Summoner": default_properties.copy(),
            "White Wizard": default_properties.copy(),
            "Arch Druid": default_properties.copy(),
            "Swordsman": default_properties.copy(),
            "Knight": default_properties.copy(),
            "Crusader": default_properties.copy(),
            "Imperial Knight": default_properties.copy(),
            "Acolyte": default_properties.copy(),
            "Cleric": default_properties.copy(),
            "Priest": default_properties.copy(),
            "Matriarch": default_properties.copy(),
            "Initiate": default_properties.copy(),
            "Mage": default_properties.copy(),
            "Wizard": default_properties.copy(),
            "Sage": default_properties.copy(),
            "Witch Hunter": default_properties.copy(),
            "Slayer": default_properties.copy(),
            "Witcher": default_properties.copy(),
            "Inquisitor": default_properties.copy(),
            "Archer": default_properties.copy(),
            "Hunter": default_properties.copy(),
            "Marksman": default_properties.copy(),
            "Tracker": default_properties.copy(),
            "Druid": default_properties.copy(),
            "Shaman": default_properties.copy(),
            "Shapeshifter": default_properties.copy(),
            "Thief": default_properties.copy(),
            "Rogue": default_properties.copy(),
            "Assassin": default_properties.copy(),
            "Stalker": default_properties.copy(),
            "Templar": default_properties.copy(),
            "Arch Templar": default_properties.copy(),
            "High Templar": default_properties.copy(),
            "Dark Templar": default_properties.copy(),
            "Ninja": default_properties.copy(),
            "Genin": default_properties.copy(),
            "Chunin": default_properties.copy(),
            "Executioner": default_properties.copy(),
            "Novice (Male)": default_properties.copy(),
            "Novice (Female)": default_properties.copy(),
            "Caster": default_properties.copy(),
            "Clairvoyant": default_properties.copy(),
            "Sorceress": default_properties.copy(),
            "Illuminator": default_properties.copy(),
            "Acolyte (M)": default_properties.copy(),
            "Acolyte (F)": default_properties.copy(),
            "Cleric (F)": default_properties.copy(),
            "Valkyrie": default_properties.copy(),
            "Fairy": default_properties.copy(),
            "Sprite": default_properties.copy(),
            "Astronomer": default_properties.copy(),
            "Constellation": default_properties.copy(),
        }
        
RECIPES = {
            "Godly": {
		"materials": ["Twilight", "Eve"]
	},
	"Twilight": {
		"materials": ["Mystery", "Draconic Trinity", "Hellish Behemoth", "Nether Reactor"]
	},
	"Eve": {
		"materials": ["Blessing of Darkness", "Blessing of Dragon", "Blessing of Agony", "Nether Reactor"]
	},
	"Mystery": {
		"materials": ["Mantle of Darkness", "Blessing of Darkness", "Nether Reactor"]
	},
	"Mystical": {
		"materials": ["Godly Material", "Godly Material", "Godly Material", "Nether Reactor"]
	},
	"Draconic Trinity": {
		"materials": ["Dragon Tooth", "Dragon Egg", "Blessing of Dragon", "Nether Reactor"]
	},
	"Incinerator": {
		"materials": ["Fire Demon", "Fire Lotus"]
	},
	"Curse of Hell": {
		"materials": ["Incinerator", "Mystery", "Mystical", "Draconic Trinity", "Nether Reactor"]
	},
	"Fire Stone": {
		"materials": ["Incinerator", "Curse of Hell", "Nether Reactor"]
	},
	"Crystal of Eternal Flame": {
		"materials": ["Fire Rising", "Fire Stone", "Nether Reactor"]
	},
	"Demonic Flame": {
		"materials": ["Dragon Tooth", "Crystal of Eternal Flame"]
	},
	"Imp's Tail": {
		"materials": ["Dragon Egg", "Crystal of Eternal Flame"]
	},
	"Blessing of Fire": {
		"materials": ["Blessing of Dragon", "Crystal of Eternal Flame"]
	},
	"Hellish Behemoth": {
		"materials": ["Demonic Flame", "Imp's Tail", "Blessing of Fire", "Nether Reactor"]
	},
	"Blessing of Agony": {
		"materials": ["Essence of Nightmare", "Essence of Hell", "Fire Rising", "Agony"]
	},
	"Agony": {
		"materials": ["4M Gold","2K Shards"]}}
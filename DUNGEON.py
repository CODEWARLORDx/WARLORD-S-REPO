# ravensburg_rpg.py
import json
import os
import random
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

SAVE_FILE = "rpg_save.json"
SAVE_VERSION = 3  # bumped for chest schema
HOF_FILE = "hall_of_fame.json"

# --------------------------
# Dice utilities
# --------------------------
def roll(dice: str) -> int:
    """
    Roll dice notation like "1d8+2", "2d6-1", "d20", or a plain int string.
    """
    dice = dice.lower().strip()
    if "d" not in dice:
        return int(dice)
    parts = dice.replace(" ", "").split("d")
    n = parts[0]
    tail = parts[1]
    if n == "":
        n = 1
    n = int(n)
    mod = 0
    if "+" in tail:
        sides, add = tail.split("+")
        mod = int(add)
    elif "-" in tail:
        sides, sub = tail.split("-")
        mod = -int(sub)
    else:
        sides = tail
    sides = int(sides)
    total = sum(random.randint(1, sides) for _ in range(n)) + mod
    return total

def d20():
    return random.randint(1, 20)

# --------------------------
# Core tables (items/spells)
# --------------------------
WEAPONS = {
    "Dagger":   {"cost": 10, "damage": "1d4", "attr": "DEX"},
    "Shortsword":{"cost": 25, "damage": "1d6", "attr": "STR"},
    "Longsword":{"cost": 40, "damage": "1d8", "attr": "STR"},
    "Staff":    {"cost": 20, "damage": "1d6", "attr": "INT"},
    "Shortbow": {"cost": 35, "damage": "1d6", "attr": "DEX"},
}
WEAPONS.setdefault("Mace", {"cost": 30, "damage": "1d6+1", "attr": "STR"})

ARMORS = {
    "Clothes":  {"cost": 0,  "base_ac": 10, "dex_cap": None},
    "Leather":  {"cost": 30, "base_ac": 11, "dex_cap": None},
    "Chain":    {"cost": 60, "base_ac": 13, "dex_cap": +2},
    "Plate":    {"cost": 120,"base_ac": 16, "dex_cap": 0},
    "Robes":    {"cost": 25, "base_ac": 10, "dex_cap": None},
}

POTIONS = {
    "Healing Potion": {"cost": 25, "effect": "heal_10"},
    "Greater Healing": {"cost": 80, "effect": "heal_25"},
}

SPELLS = {
    "Firebolt": {"cost": 50, "type": "attack", "damage": "1d8", "attr": "INT", "desc": "Hurl fire at a foe."},
    "Magic Missile": {"cost": 90, "type": "attack_auto", "damage": "2d4+2", "attr": "INT", "desc": "Auto-hit force darts."},
    "Heal": {"cost": 60, "type": "heal", "amount": "1d8", "attr": "WIS", "desc": "Restore health."},
    "Shield": {"cost": 70, "type": "buff_ac", "bonus": 2, "turns": 3, "desc": "Raise AC temporarily."},
}

RACES = {
    "Human":   {"bonuses": {"ANY": +1}},
    "Elf":     {"bonuses": {"DEX": +2, "CON": -1}},
    "Dwarf":   {"bonuses": {"CON": +2, "CHA": -1}},
    "Halfling":{"bonuses": {"DEX": +2, "STR": -1}},
    "Gnome":   {"bonuses": {"INT": +2, "STR": -1}},
}

CLASSES = {
    "Warrior": {"hp_die": 10, "fav": "STR", "start": {"weapon": "Longsword", "armor": "Chain", "gold": 60}},
    "Rogue":   {"hp_die": 8,  "fav": "DEX", "start": {"weapon": "Shortsword", "armor": "Leather", "gold": 70}},
    "Wizard":  {"hp_die": 6,  "fav": "INT", "start": {"weapon": "Staff", "armor": "Robes", "gold": 80, "spells": ["Firebolt"]}},
    "Cleric":  {"hp_die": 8,  "fav": "WIS", "start": {"weapon": "Mace", "armor": "Chain", "gold": 70, "spells": ["Heal"]}},
}

ATTRS = ["STR", "DEX", "INT", "CON", "WIS", "CHA", "PER"]

# --------------------------
# Dungeon pieces
# --------------------------
MONSTER_TEMPLATES = [
    {"name":"Goblin",   "hp":"2d6+2", "ac":12, "atk_bonus":2, "dmg":"1d6", "xp":6, "gold":"1d8"},
    {"name":"Skeleton", "hp":"2d8",   "ac":13, "atk_bonus":3, "dmg":"1d6+1","xp":8, "gold":"1d6"},
    {"name":"Zombie",   "hp":"3d8",   "ac":10, "atk_bonus":2, "dmg":"1d6","xp":10, "gold":"1d10"},
    {"name":"Bandit",   "hp":"2d8+2", "ac":12, "atk_bonus":3, "dmg":"1d6+1","xp":9, "gold":"2d6"},
    {"name":"Giant Rat","hp":"1d8+1", "ac":11, "atk_bonus":2, "dmg":"1d4","xp":4, "gold":"1d4"},
]

NECROMANCER = {"name":"Evil Necromancer", "hp":"6d8+12","ac":15,"atk_bonus":5,"dmg":"1d8+2","xp":50,"gold":"5d10"}

ROOM_TYPES = ["monster", "trap", "treasure", "fountain", "empty"]

# --------------------------
# Data classes
# --------------------------
@dataclass
class Effects:
    ac_buff: int = 0
    ac_turns: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {"ac_buff": self.ac_buff, "ac_turns": self.ac_turns}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Effects":
        if not isinstance(d, dict):
            return Effects()
        return Effects(ac_buff=int(d.get("ac_buff", 0)), ac_turns=int(d.get("ac_turns", 0)))

@dataclass
class Character:
    name: str
    race: str
    char_class: str
    attrs: Dict[str, int]
    level: int = 1
    xp: int = 0
    gold: int = 0
    max_hp: int = 1
    hp: int = 1
    weapon: str = "Dagger"
    armor: str = "Clothes"
    potions: Dict[str, int] = field(default_factory=dict)
    spells: List[str] = field(default_factory=list)
    effects: Effects = field(default_factory=Effects)

    def mod(self, attr: str) -> int:
        return (self.attrs.get(attr, 10) - 10) // 2

    def calc_ac(self) -> int:
        armor = ARMORS.get(self.armor, ARMORS["Clothes"])
        base = armor["base_ac"]
        dex_mod = self.mod("DEX")
        if armor["dex_cap"] is None:
            dex_add = dex_mod
        else:
            dex_add = min(dex_mod, armor["dex_cap"])
        return base + max(0, dex_add) + self.effects.ac_buff

    def attack_bonus(self) -> int:
        prof = 2 + (self.level - 1) // 4
        weapon = WEAPONS.get(self.weapon, WEAPONS["Dagger"])
        attr = weapon["attr"]
        return prof + self.mod(attr)

    def damage_roll(self) -> int:
        weapon = WEAPONS.get(self.weapon, WEAPONS["Dagger"])
        base = roll(weapon["damage"])
        return max(1, base + self.mod(weapon["attr"]))

    def learn_spell(self, name: str):
        if name not in self.spells and name in SPELLS:
            self.spells.append(name)

    def add_potion(self, name: str, qty: int = 1):
        self.potions[name] = self.potions.get(name, 0) + qty

    def level_up_if_ready(self):
        needed = 25 * self.level
        leveled = False
        while self.xp >= needed:
            self.level += 1
            hp_gain = max(1, roll(f"1d{CLASSES[self.char_class]['hp_die']}") + self.mod("CON"))
            self.max_hp += hp_gain
            self.hp = self.max_hp
            fav = CLASSES[self.char_class]["fav"]
            self.attrs[fav] += 1
            print(f"\n*** LEVEL UP! You are now level {self.level}. +{hp_gain} HP, +1 {fav}. ***")
            leveled = True
            needed = 25 * self.level
        return leveled

    # ---- Serialization ----
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "race": self.race,
            "char_class": self.char_class,
            "attrs": self.attrs,
            "level": self.level,
            "xp": self.xp,
            "gold": self.gold,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "weapon": self.weapon,
            "armor": self.armor,
            "potions": self.potions,
            "spells": self.spells,
            "effects": self.effects.to_dict(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Character":
        eff = Effects.from_dict(d.get("effects", {}))
        return Character(
            name=d["name"],
            race=d["race"],
            char_class=d["char_class"],
            attrs={k:int(v) for k,v in d["attrs"].items()},
            level=int(d.get("level", 1)),
            xp=int(d.get("xp", 0)),
            gold=int(d.get("gold", 0)),
            max_hp=int(d.get("max_hp", 1)),
            hp=int(d.get("hp", 1)),
            weapon=d.get("weapon", "Dagger"),
            armor=d.get("armor", "Clothes"),
            potions={k:int(v) for k,v in d.get("potions", {}).items()},
            spells=list(d.get("spells", [])),
            effects=eff,
        )

@dataclass
class Monster:
    name: str
    hp: int
    ac: int
    atk_bonus: int
    dmg: str
    xp: int
    gold: int

@dataclass
class Room:
    visited: bool = False
    kind: str = "empty"
    content: Optional[Dict[str, Any]] = None  # monster/trap/chest/fountain/boss

    def to_dict(self) -> Dict[str, Any]:
        return {"visited": self.visited, "kind": self.kind, "content": self.content}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Room":
        return Room(bool(d.get("visited", False)), d.get("kind", "empty"), d.get("content"))

@dataclass
class Dungeon:
    rows: int
    cols: int
    grid: List[List[Room]]
    player_pos: Tuple[int, int]
    boss_pos: Tuple[int, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "player_pos": list(self.player_pos),
            "boss_pos": list(self.boss_pos),
            "grid": [[cell.to_dict() for cell in row] for row in self.grid],
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Dungeon":
        rows = int(d["rows"]); cols = int(d["cols"])
        grid = [[Room.from_dict(c) for c in row] for row in d["grid"]]
        ppos = tuple(d.get("player_pos", [0,0]))
        bpos = tuple(d.get("boss_pos", [rows-1, cols-1]))
        return Dungeon(rows, cols, grid, ppos, bpos)

# --------------------------
# Generation helpers
# --------------------------
def roll_4d6_drop_lowest() -> int:
    rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
    return sum(rolls[:3])

def generate_attributes() -> Dict[str, int]:
    vals = [roll_4d6_drop_lowest() for _ in ATTRS]
    random.shuffle(vals)
    return {attr: vals[i] for i, attr in enumerate(ATTRS)}

def apply_race_bonuses(attrs: Dict[str, int], race: str) -> Dict[str, int]:
    bonuses = RACES[race]["bonuses"]
    out = dict(attrs)
    if "ANY" in bonuses:
        choice = random.choice(ATTRS)
        out[choice] += bonuses["ANY"]
    for k, v in bonuses.items():
        if k == "ANY": continue
        out[k] = out.get(k, 10) + v
    return out

def starting_hp(attrs: Dict[str, int], char_class: str) -> int:
    die = CLASSES[char_class]["hp_die"]
    return max(1, die + max(0, (attrs["CON"] - 10)//2))

def new_character() -> Character:
    print("\n--- Welcome to Dungeon Adventure: Ravensburg ---")
    name = input("CALL ME (character name): ").strip() or "Hero"
    print("Choose race:", ", ".join(RACES.keys()))
    race = ""
    while race not in RACES:
        race = input("Race: ").title().strip()
    print("Choose class:", ", ".join(CLASSES.keys()))
    char_class = ""
    while char_class not in CLASSES:
        char_class = input("Class: ").title().strip()

    base_attrs = generate_attributes()
    base_attrs = apply_race_bonuses(base_attrs, race)

    print("\nRolled attributes:")
    for a in ATTRS:
        print(f"  {a}: {base_attrs[a]}")
    swap = input("Do you want to swap two attributes once? (y/n): ").lower().startswith("y")
    if swap:
        a = input("Swap FROM (e.g., STR): ").upper().strip()
        b = input("Swap TO (e.g., DEX): ").upper().strip()
        if a in ATTRS and b in ATTRS:
            base_attrs[a], base_attrs[b] = base_attrs[b], base_attrs[a]
            print("Swapped.")
        else:
            print("Invalid swap; keeping original values.")

    hp = starting_hp(base_attrs, char_class)
    start = CLASSES[char_class]["start"]
    weapon = start["weapon"]
    armor = start["armor"]
    gold = start.get("gold", 50)
    spells = start.get("spells", [])
    c = Character(
        name=name,
        race=race,
        char_class=char_class,
        attrs=base_attrs,
        level=1,
        xp=0,
        gold=gold,
        max_hp=hp,
        hp=hp,
        weapon=weapon,
        armor=armor,
        potions={"Healing Potion": 1},
        spells=spells[:],
    )
    print("\n--- CHARACTER CREATED ---")
    print_character(c)
    return c

def print_character(c: Character):
    print(f"\n{c.name} — Level {c.level} {c.race} {c.char_class}")
    print("Attributes: " + ", ".join([f"{a} {c.attrs[a]} ({c.mod(a):+d})" for a in ATTRS]))
    print(f"HP: {c.hp}/{c.max_hp}   AC: {c.calc_ac()}   XP: {c.xp}   Gold: {c.gold}")
    print(f"Weapon: {c.weapon}   Armor: {c.armor}")
    if c.potions:
        p = ", ".join([f"{k} x{v}" for k, v in c.potions.items()])
        print(f"Potions: {p}")
    if c.spells:
        print("Spells: " + ", ".join(c.spells))

def chest_payload() -> Dict[str, Any]:
    """
    Build a chest with trap + lock + loot.
    """
    gold_amt = roll("2d6+6")
    potion = random.choice([None, "Healing Potion", "Greater Healing", None])
    has_trap = random.random() < 0.55
    has_lock = random.random() < 0.75
    trap_dc = 11 + random.randint(0, 6)
    lock_dc = 12 + random.randint(0, 6)
    return {
        "type": "chest",
        "opened": False,
        "locked": has_lock,
        "lock_jammed": False,
        "lock_dc": lock_dc,
        "trap": {
            "armed": has_trap,
            "dc": trap_dc,
            "known": False,        # set True after a successful EXAMINE
            "disarmed": False
        },
        "loot": {
            "gold": gold_amt,
            "potion": potion
        }
    }

def generate_dungeon(rows=10, cols=10) -> Dungeon:
    grid: List[List[Room]] = []
    for i in range(rows):
        row: List[Room] = []
        for j in range(cols):
            kind = random.choices(ROOM_TYPES, weights=[35, 15, 20, 10, 20])[0]
            content = None
            if kind == "monster":
                content = {"monster": random.choice(MONSTER_TEMPLATES)}
            elif kind == "trap":
                content = {"dc": 12 + random.randint(0, 4), "dmg": "1d6+2"}
            elif kind == "treasure":
                content = chest_payload()
            elif kind == "fountain":
                content = {"type": random.choice(["heal", "buff", "poison"])}
            row.append(Room(False, kind, content))
        grid.append(row)
    boss_pos = (random.randint(rows//2, rows-1), random.randint(cols//2, cols-1))
    grid[boss_pos[0]][boss_pos[1]] = Room(False, "boss", {"monster": NECROMANCER})
    return Dungeon(rows, cols, grid, (0, 0), boss_pos)

# --------------------------
# Persistence (robust)
# --------------------------
def _atomic_write_json(path: str, data: Dict[str, Any]):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)

def save_game(c: Character, d: Dungeon):
    data = {
        "version": SAVE_VERSION,
        "character": c.to_dict(),
        "dungeon": d.to_dict(),
    }
    try:
        _atomic_write_json(SAVE_FILE, data)
        print(f"\n[SAVED] Game saved to {SAVE_FILE}")
    except Exception as e:
        print(f"[SAVE ERROR] {e}")

def load_game() -> Tuple[Optional[Character], Optional[Dungeon]]:
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return None, None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        version = int(data.get("version", 1))
        ch = data["character"]
        dg = data["dungeon"]
        c = Character.from_dict(ch)
        d = Dungeon.from_dict(dg)
        if version != SAVE_VERSION:
            print(f"[Loaded save version {version}] Converted to current format.")
        print("[LOADED] Save loaded.")
        return c, d
    except Exception as e:
        print(f"[LOAD ERROR] {e}")
        return None, None

def add_to_hof(name: str):
    hof = []
    if os.path.exists(HOF_FILE):
        try:
            with open(HOF_FILE, "r", encoding="utf-8") as f:
                hof = json.load(f)
        except Exception:
            hof = []
    hof.append({"name": name, "title": "Slayer of the Necromancer"})
    try:
        _atomic_write_json(HOF_FILE, hof)
        print("\n*** Your name has been etched into the HALL OF FAME! ***")
    except Exception as e:
        print(f"[HOF SAVE ERROR] {e}")

def show_hof():
    if not os.path.exists(HOF_FILE):
        print("The Hall of Fame is empty… for now.")
        return
    try:
        with open(HOF_FILE, "r", encoding="utf-8") as f:
            hof = json.load(f)
        print("\n--- HALL OF FAME ---")
        for i, entry in enumerate(hof, 1):
            print(f"{i}. {entry['name']} — {entry['title']}")
    except Exception as e:
        print(f"[HOF LOAD ERROR] {e}")

# --------------------------
# Town / Shop
# --------------------------
def town_menu(c: Character, d: Dungeon):
    print(
        "\nRavensburg needs your help! Monsters spill from the dungeon. "
        "Prepare in town, then venture forth to find and slay the Evil Necromancer."
    )
    while True:
        print("\n--- TOWN ---")
        print("Commands: LIST, PURCHASE <item>, SELL <item>, REST, TRAIN, ENTER DUNGEON, SAVE, LOAD, HOF, STATUS, INVENTORY, EQUIP <weapon>, WEAR <armor>, HELP, QUIT")
        cmd = input("> ").strip()
        if not cmd:
            continue
        low = cmd.lower()
        if low == "help":
            print_town_help()
        elif low == "list":
            list_shop()
        elif low.startswith("purchase "):
            item = cmd[9:].strip()
            purchase(c, item)
        elif low.startswith("sell "):
            item = cmd[5:].strip()
            sell(c, item)
        elif low == "rest":
            rest(c)
        elif low == "train":
            train(c)
        elif low == "status":
            print_character(c)
        elif low == "inventory":
            show_inventory(c)
        elif low.startswith("equip "):
            item = cmd[6:].strip()
            equip_weapon(c, item)
        elif low.startswith("wear "):
            item = cmd[5:].strip()
            wear_armor(c, item)
        elif low == "enter dungeon":
            explore_loop(c, d)
            if c.hp <= 0:
                print("You limp back to town… or rather, are carried. (Game over if HP is 0.)")
                return
        elif low == "save":
            save_game(c, d)
        elif low == "load":
            cc, dd = load_game()
            if cc and dd:
                c.__dict__.update(cc.__dict__)
                d.rows = dd.rows; d.cols = dd.cols; d.grid = dd.grid; d.player_pos = dd.player_pos; d.boss_pos = dd.boss_pos
        elif low == "hof":
            show_hof()
        elif low == "quit":
            print("Farewell, hero.")
            sys.exit(0)
        else:
            print("Unknown command. Type HELP.")

def print_town_help():
    print("""
TOWN COMMANDS:
  LIST                             – List items for sale
  PURCHASE <item>                  – Buy an item (weapon/armor/potion/spell)
  SELL <item>                      – Sell an item you own
  REST                             – Fully heal
  TRAIN                            – Small stat training (costs gold)
  ENTER DUNGEON                    – Venture into the dungeon
  STATUS / INVENTORY               – Show your character / items
  EQUIP <weapon> / WEAR <armor>    – Change your loadout
  SAVE / LOAD                      – Save or load your game
  HOF                              – Show Hall of Fame
  QUIT                             – Exit game
    """)

def list_shop():
    print("\n--- SHOP (Weapons) ---")
    for k, v in WEAPONS.items():
        print(f"  {k:<12} {v['cost']:>4}g  dmg {v['damage']} ({v['attr']})")
    print("\n--- SHOP (Armors) ---")
    for k, v in ARMORS.items():
        cap = v['dex_cap'] if v['dex_cap'] is not None else '—'
        print(f"  {k:<12} {v['cost']:>4}g  base AC {v['base_ac']}  dex cap: {cap}")
    print("\n--- SHOP (Potions) ---")
    for k, v in POTIONS.items():
        print(f"  {k:<16} {v['cost']:>4}g")
    print("\n--- SHOP (Spells) ---")
    for k, v in SPELLS.items():
        print(f"  {k:<16} {v['cost']:>4}g  – {v['desc']}")

def purchase(c: Character, item: str):
    item_title = item.title()
    if item_title in WEAPONS:
        cost = WEAPONS[item_title]["cost"]
        if c.gold >= cost:
            c.gold -= cost
            print(f"Purchased {item_title}. Use 'EQUIP {item_title}' to wield it.")
        else:
            print("Not enough gold.")
    elif item_title in ARMORS:
        cost = ARMORS[item_title]["cost"]
        if c.gold >= cost:
            c.gold -= cost
            print(f"Purchased {item_title}. Use 'WEAR {item_title}' to don it.")
        else:
            print("Not enough gold.")
    elif item_title in POTIONS:
        cost = POTIONS[item_title]["cost"]
        if c.gold >= cost:
            c.gold -= cost
            c.add_potion(item_title, 1)
            print(f"Purchased {item_title}.")
        else:
            print("Not enough gold.")
    elif item_title in SPELLS:
        cost = SPELLS[item_title]["cost"]
        if item_title in c.spells:
            print("You already know that spell.")
            return
        if c.gold >= cost:
            c.gold -= cost
            c.learn_spell(item_title)
            print(f"Learned spell {item_title}.")
        else:
            print("Not enough gold.")
    else:
        print("Item not found.")

def sell(c: Character, item: str):
    item_title = item.title()
    if item_title == c.weapon:
        price = WEAPONS.get(item_title, {}).get("cost", 0)//2
        c.gold += price
        c.weapon = "Dagger"
        print(f"Sold {item_title} for {price}g. You equip a Dagger.")
    elif item_title == c.armor:
        price = ARMORS.get(item_title, {}).get("cost", 0)//2
        c.gold += price
        c.armor = "Clothes"
        print(f"Sold {item_title} for {price}g. You wear Clothes.")
    elif item_title in c.potions and c.potions[item_title] > 0:
        price = POTIONS.get(item_title, {}).get("cost", 0)//2
        c.potions[item_title] -= 1
        if c.potions[item_title] <= 0:
            del c.potions[item_title]
        c.gold += price
        print(f"Sold 1x {item_title} for {price}g.")
    elif item_title in c.spells:
        print("You cannot sell knowledge once learned.")
    else:
        print("You don't have that item equipped/owned.")

def rest(c: Character):
    c.hp = c.max_hp
    c.effects = Effects()
    print("You rest at the inn. Fully healed and refreshed.")

def train(c: Character):
    cost = 40
    print(f"Training costs {cost}g and gives +1 to a chosen attribute.")
    if c.gold < cost:
        print("Not enough gold.")
        return
    choice = input("Train which attribute (STR/DEX/INT/CON/WIS/CHA/PER)? ").upper().strip()
    if choice not in ATTRS:
        print("Invalid attribute.")
        return
    c.gold -= cost
    c.attrs[choice] += 1
    print(f"Training complete. {choice} is now {c.attrs[choice]}.")

def show_inventory(c: Character):
    print("\n--- INVENTORY ---")
    print(f"Gold: {c.gold}")
    print(f"Weapon: {c.weapon}")
    print(f"Armor : {c.armor}")
    if c.potions:
        for k, v in c.potions.items():
            print(f"Potion: {k} x{v}")
    if c.spells:
        print("Spells: " + ", ".join(c.spells))

def equip_weapon(c: Character, item: str):
    item_title = item.title()
    if item_title in WEAPONS:
        print(f"You equip {item_title}.")
        c.weapon = item_title
    else:
        print("That is not a valid weapon.")

def wear_armor(c: Character, item: str):
    item_title = item.title()
    if item_title in ARMORS:
        print(f"You wear {item_title}.")
        c.armor = item_title
    else:
        print("That is not a valid armor.")

# --------------------------
# Dungeon exploration & combat
# --------------------------
def explore_loop(c: Character, d: Dungeon):
    print("\nYou travel to the dungeon entrance… darkness beckons.")
    while c.hp > 0:
        x, y = d.player_pos
        room = d.grid[x][y]
        if not room.visited:
            print(f"\nYou enter a new chamber at {d.player_pos}.")
            room.visited = True
            trigger_room(c, d, room)
            if c.hp <= 0:
                break
        print(f"\nYou are at {d.player_pos}.")
        print("Dungeon commands: WHERE AM I / LOOK, MAP, MOVE <N/E/S/W>, STATUS, INVENTORY, DRINK <potion>, CAST <spell>,")
        print("                  EXAMINE CHEST FOR TRAPS, DISARM CHEST TRAP, PICK CHEST LOCK, PRY CHEST LOCK, OPEN CHEST,")
        print("                  SAVE, LOAD, RETURN TOWN, HELP")
        cmd = input("> ").strip()
        if not cmd:
            continue
        low = cmd.lower()
        if low in ("where am i", "look", "look around"):
            describe_room(room)
            if room.kind == "treasure":
                describe_chest(room.content)
        elif low == "map":
            print(ascii_map(d))
        elif low.startswith("move "):
            dirc = low.split(" ", 1)[1].strip().upper()
            move_player(d, dirc)
        elif low in ("status", "character", "character stats", "character sheet"):
            print_character(c)
        elif low == "inventory":
            show_inventory(c)
        elif low.startswith("drink "):
            name = cmd[6:].strip().title()
            drink_potion(c, name)
        elif low.startswith("cast "):
            spell = cmd[5:].strip().title()
            cast_spell_out_of_combat(c, spell)
        elif low == "examine chest for traps":
            if room.kind == "treasure":
                chest_examine(c, room.content)
            else:
                print("There is no chest here.")
        elif low == "disarm chest trap":
            if room.kind == "treasure":
                chest_disarm(c, room.content)
            else:
                print("There is no chest here.")
        elif low == "pick chest lock":
            if room.kind == "treasure":
                chest_pick_lock(c, room.content)
            else:
                print("There is no chest here.")
        elif low == "pry chest lock":
            if room.kind == "treasure":
                chest_pry_lock(c, room.content)
            else:
                print("There is no chest here.")
        elif low == "open chest":
            if room.kind == "treasure":
                chest_open(c, room.content)
            else:
                print("There is no chest here.")
        elif low == "save":
            save_game(c, d)
        elif low == "load":
            cc, dd = load_game()
            if cc and dd:
                c.__dict__.update(cc.__dict__)
                d.rows = dd.rows; d.cols = dd.cols; d.grid = dd.grid; d.player_pos = dd.player_pos; d.boss_pos = dd.boss_pos
                print("(Loaded. You remain where the save placed you.)")
        elif low in ("return town", "go back", "back to town"):
            print("You carefully make your way back to Ravensburg.")
            return
        elif low == "help":
            print("""
DUNGEON COMMANDS:
  LOOK / WHERE AM I            – Describe current room
  MAP                          – Show mini-map (10x10, fog of war)
  MOVE N/E/S/W                 – Move to adjacent room (if possible)
  STATUS / INVENTORY           – View character or inventory
  DRINK <potion name>          – Drink a potion
  CAST <spell name>            – Cast a non-combat spell (e.g., Heal)
  EXAMINE CHEST FOR TRAPS      – Inspect the chest (treasure rooms)
  DISARM CHEST TRAP            – Attempt to disable the trap
  PICK CHEST LOCK              – Attempt to pick the lock
  PRY CHEST LOCK               – Force the lock open
  OPEN CHEST                   – Open (beware armed traps/locks)
  SAVE / LOAD                  – Save or load game
  RETURN TOWN                  – Exit to town
            """)
        else:
            print("Unrecognized command.")

def move_player(d: Dungeon, dirc: str):
    x, y = d.player_pos
    if dirc == "N" and x > 0:
        d.player_pos = (x-1, y)
    elif dirc == "S" and x < d.rows-1:
        d.player_pos = (x+1, y)
    elif dirc == "W" and y > 0:
        d.player_pos = (x, y-1)
    elif dirc == "E" and y < d.cols-1:
        d.player_pos = (x, y+1)
    else:
        print("You cannot move that way.")

def ascii_map(d: Dungeon) -> str:
    """Render a 10x10 mini-map with fog of war."""
    rows, cols = d.rows, d.cols
    lines = []
    border = "+" + "-" * (cols) + "+"
    lines.append(border)
    for i in range(rows):
        row_chars = []
        for j in range(cols):
            ch = " "
            room = d.grid[i][j]
            if (i, j) == d.player_pos:
                ch = "@"
            elif room.visited:
                # reveal boss if discovered (visited)
                if room.kind == "boss":
                    ch = "B"
                else:
                    ch = "·"
            row_chars.append(ch)
        lines.append("|" + "".join(row_chars) + "|")
    lines.append(border)
    legend = "\nLegend: @=You  ·=Explored  space=Unexplored  B=Boss (discovered)"
    return "\n".join(lines) + legend

def describe_room(room: Room):
    if room.kind == "empty":
        print("A dusty, silent chamber. Nothing stirs.")
    elif room.kind == "monster":
        print("You sense lurking danger — a monster had been here.")
    elif room.kind == "trap":
        print("You notice suspicious grooves and wires… a trap lies here.")
    elif room.kind == "treasure":
        print("A battered chest glints in the shadows.")
    elif room.kind == "fountain":
        print("An ancient fountain bubbles softly.")
    elif room.kind == "boss":
        print("A foreboding chamber reeks of dark magic…")

def trigger_room(c: Character, d: Dungeon, room: Room):
    if room.kind == "monster":
        start_fight(c, make_monster(room.content["monster"]))
    elif room.kind == "trap":
        resolve_trap(c, room.content)
    elif room.kind == "treasure":
        # first-time sighting reveals chest existence (but not trap/lock details)
        describe_chest(room.content, brief=True)
    elif room.kind == "fountain":
        resolve_fountain(c, room.content)
    elif room.kind == "boss":
        print("The Evil Necromancer stands before you!")
        win = start_fight(c, make_monster(NECROMANCER))
        if win:
            print("\nWith a final cry, the Necromancer falls. Ravensburg is saved!")
            add_to_hof(c.name)
            print("You return to town a hero.")
            d.player_pos = (0,0)

def make_monster(template: Dict[str, Any]) -> Monster:
    return Monster(
        name=template["name"],
        hp=roll(template["hp"]),
        ac=template["ac"],
        atk_bonus=template["atk_bonus"],
        dmg=template["dmg"],
        xp=template["xp"],
        gold=roll(template["gold"]),
    )

def resolve_trap(c: Character, content: Dict[str, Any]):
    dc = content["dc"]
    dmg = content["dmg"]
    print("A trap springs! Make a DEX save (d20 + DEX).")
    save = d20() + c.mod("DEX")
    print(f"Save: {save} vs DC {dc}")
    if save >= dc:
        print("You dodge the trap just in time.")
    else:
        harm = roll(dmg)
        c.hp = max(0, c.hp - harm)
        print(f"Trap hits for {harm} damage! HP {c.hp}/{c.max_hp}")

def resolve_fountain(c: Character, content: Dict[str, Any]):
    kind = content["type"]
    if kind == "heal":
        gain = min(c.max_hp - c.hp, roll("1d8+4"))
        c.hp += gain
        print(f"The water heals you for {gain} HP. ({c.hp}/{c.max_hp})")
    elif kind == "buff":
        c.effects.ac_buff = 1
        c.effects.ac_turns = 10
        print("You feel protected. (+1 AC for a while)")
    else:
        harm = roll("1d6")
        c.hp = max(0, c.hp - harm)
        print(f"The water was foul! You take {harm} damage. ({c.hp}/{c.max_hp})")

# --------------------------
# Chest system
# --------------------------
def describe_chest(chest: Dict[str, Any], brief: bool=False):
    if chest["opened"]:
        print("The chest here stands open and empty.")
        return
    locked = chest["locked"]
    trap = chest["trap"]
    if brief:
        print("You spot a sturdy wooden chest here.")
        return
    # Detailed describe; trap details only if known
    lock_txt = "locked" if locked else "unlocked"
    trap_txt = "unknown" if not trap["known"] else ("disarmed" if trap["disarmed"] else "armed")
    print(f"Chest: {lock_txt}. Trap status: {trap_txt}.")

def chest_examine(c: Character, chest: Dict[str, Any]):
    if chest["opened"]:
        print("The chest is already open.")
        return
    check = d20() + c.mod("PER")
    dc = 10  # basic perception DC to notice mechanisms
    print(f"You carefully examine the chest… Perception {check} vs DC {dc}")
    if check >= dc:
        chest["trap"]["known"] = True
        status = "armed" if (chest["trap"]["armed"] and not chest["trap"]["disarmed"]) else ("disarmed" if chest["trap"]["disarmed"] else "not present")
        print(f"You notice: trap status is {status}. The lock appears {'jammed' if chest['lock_jammed'] else ('present' if chest['locked'] else 'absent')}.")
    else:
        print("You don't notice anything unusual.")

def chest_disarm(c: Character, chest: Dict[str, Any]):
    trap = chest["trap"]
    if chest["opened"]:
        print("The chest is already open.")
        return
    if not trap["armed"] or trap["disarmed"]:
        print("There is no active trap to disarm.")
        return
    dc = trap["dc"]
    roll_total = d20() + c.mod("DEX")
    print(f"You attempt to disarm the trap… DEX check {roll_total} vs DC {dc}")
    if roll_total >= dc:
        trap["disarmed"] = True
        print("You deftly disable the trap.")
    elif roll_total <= dc - 5:
        print("Your tools slip—trap triggers!")
        _chest_trap_trigger(c, chest)
    else:
        print("You fail to disarm the trap, but at least you didn't set it off.")

def chest_pick_lock(c: Character, chest: Dict[str, Any]):
    if chest["opened"]:
        print("The chest is already open.")
        return
    if not chest["locked"]:
        print("The chest is already unlocked.")
        return
    if chest["lock_jammed"]:
        print("The lock is jammed—you'll have to pry it.")
        return
    dc = chest["lock_dc"]
    roll_total = d20() + c.mod("DEX")
    print(f"You try to pick the lock… DEX check {roll_total} vs DC {dc}")
    if roll_total >= dc:
        chest["locked"] = False
        print("You hear a soft click—the chest is unlocked.")
    elif roll_total <= dc - 5:
        chest["lock_jammed"] = True
        print("Snap! Your pick jams the lock. You'll need to pry it.")
    else:
        print("The lock resists your efforts.")

def chest_pry_lock(c: Character, chest: Dict[str, Any]):
    if chest["opened"]:
        print("The chest is already open.")
        return
    if not chest["locked"] and not chest["lock_jammed"]:
        print("No need to pry—it's already unlocked.")
        return
    dc = chest["lock_dc"] + 2
    roll_total = d20() + c.mod("STR")
    print(f"You wedge your blade and pry… STR check {roll_total} vs DC {dc}")
    if roll_total >= dc:
        chest["locked"] = False
        chest["lock_jammed"] = False
        print("With a crack, the lock gives way.")
    else:
        pain = roll("1d4")
        c.hp = max(0, c.hp - pain)
        print(f"The chest shifts and bites back; you take {pain} damage. HP {c.hp}/{c.max_hp}")
        # 25% chance a still-armed trap springs when prying fails
        trap = chest["trap"]
        if trap["armed"] and not trap["disarmed"] and random.random() < 0.25:
            print("As you pry, a mechanism snaps—trap triggers!")
            _chest_trap_trigger(c, chest)

def chest_open(c: Character, chest: Dict[str, Any]):
    if chest["opened"]:
        print("The chest is already open.")
        return
    # Trap check
    trap = chest["trap"]
    if trap["armed"] and not trap["disarmed"]:
        print("You lift the lid—something clicks!")
        _chest_trap_trigger(c, chest)
        if c.hp <= 0:
            return
    # Lock check
    if chest["locked"]:
        print("The lock holds fast. You'll need to pick or pry it first.")
        return
    # Award loot
    gold = chest["loot"]["gold"]
    pot = chest["loot"]["potion"]
    c.gold += gold
    txt = f"You claim {gold} gold"
    if pot:
        c.add_potion(pot, 1)
        txt += f" and a {pot}"
    txt += "."
    print(txt)
    chest["opened"] = True

def _chest_trap_trigger(c: Character, chest: Dict[str, Any]):
    trap = chest["trap"]
    dmg_roll = random.choice(["1d8", "1d10", "2d4"])
    dmg = roll(dmg_roll)
    c.hp = max(0, c.hp - dmg)
    print(f"The trap strikes for {dmg} damage! ({dmg_roll}) HP {c.hp}/{c.max_hp}")
    trap["armed"] = False
    trap["disarmed"] = True  # once sprung, it's effectively neutralized

# --------------------------
# Combat
# --------------------------
def start_fight(c: Character, m: Monster) -> bool:
    print(f"\nA {m.name} appears! HP {m.hp}, AC {m.ac}")
    turn = "player"
    c.effects.ac_turns = max(0, c.effects.ac_turns)
    while c.hp > 0 and m.hp > 0:
        if c.effects.ac_turns > 0 and turn == "player":
            c.effects.ac_turns -= 1
            if c.effects.ac_turns == 0:
                c.effects.ac_buff = 0

        if turn == "player":
            print(f"\nYour HP {c.hp}/{c.max_hp}  |  {m.name} HP {m.hp}")
            print("Actions: ATTACK HIGH/MIDDLE/LOW, DEFEND HIGH/MIDDLE/LOW, CAST <spell>, DRINK <potion>, RUN, MONSTER INFO")
            cmd = input("> ").strip()
            if not cmd:
                continue
            low = cmd.lower()
            if low.startswith("attack"):
                aim = "middle"
                if "high" in low: aim = "high"
                elif "low" in low: aim = "low"
                player_attack(c, m, aim)
                turn = "monster" if m.hp > 0 else "player"
            elif low.startswith("defend"):
                c.effects.ac_buff += 2
                c.effects.ac_turns = max(c.effects.ac_turns, 1)
                print("You brace for impact (+2 AC for the next blow).")
                turn = "monster"
            elif low.startswith("cast "):
                spell = cmd[5:].strip().title()
                cast_result = cast_spell_in_combat(c, m, spell)
                if cast_result:
                    turn = "monster" if m.hp > 0 else "player"
            elif low.startswith("drink "):
                name = cmd[6:].strip().title()
                if drink_potion(c, name):
                    turn = "monster" if m.hp > 0 else "player"
            elif low in ("monster info", "monster stats"):
                print(f"{m.name} — AC {m.ac}, Attack +{m.atk_bonus}, Damage {m.dmg}")
            elif low in ("run", "evade"):
                flee_dc = 10
                chk = d20() + c.mod("DEX")
                if chk >= flee_dc:
                    print("You slip away into the shadows!")
                    return False
                else:
                    print("You fail to escape!")
                    turn = "monster"
            else:
                print("Unrecognized combat action.")
        else:
            monster_attack(c, m)
            turn = "player"

    if c.hp <= 0:
        print("\nYou fall… Your adventure ends here.")
        return False
    else:
        print(f"\nYou defeated the {m.name}!")
        c.gold += m.gold
        c.xp += m.xp
        print(f"Gained {m.xp} XP and {m.gold} gold.")
        c.level_up_if_ready()
        return True

def player_attack(c: Character, m: Monster, aim: str):
    aim_mod = {"low": +2, "middle": 0, "high": -2}[aim]
    dmg_bonus = {"low": -1, "middle": 0, "high": +1}[aim]
    atk_total = d20() + c.attack_bonus() + aim_mod
    print(f"You strike ({aim})! Attack roll = {atk_total} vs AC {m.ac}")
    if atk_total >= m.ac:
        dmg = max(1, c.damage_roll() + dmg_bonus)
        m.hp = max(0, m.hp - dmg)
        print(f"Hit for {dmg} damage. {m.name} HP now {m.hp}.")
    else:
        print("You miss!")

def monster_attack(c: Character, m: Monster):
    atk = d20() + m.atk_bonus
    ac = c.calc_ac()
    print(f"{m.name} attacks! Roll {atk} vs AC {ac}")
    if atk >= ac:
        dmg = roll(m.dmg)
        c.hp = max(0, c.hp - dmg)
        print(f"{m.name} hits you for {dmg}! HP {c.hp}/{c.max_hp}")
    else:
        print(f"{m.name} misses.")

def cast_spell_in_combat(c: Character, m: Monster, spell: str) -> bool:
    if spell not in c.spells or spell not in SPELLS:
        print("You don't know that spell.")
        return False
    s = SPELLS[spell]
    if s["type"] == "attack":
        atk = d20() + 2 + c.mod(s["attr"])
        print(f"You cast {spell}! Spell attack {atk} vs AC {m.ac}")
        if atk >= m.ac:
            dmg = max(1, roll(s["damage"]) + c.mod(s["attr"]))
            m.hp = max(0, m.hp - dmg)
            print(f"{spell} hits for {dmg}! {m.name} HP {m.hp}")
        else:
            print(f"{spell} misses.")
        return True
    elif s["type"] == "attack_auto":
        dmg = max(1, roll(s["damage"]) + max(0, c.mod(s["attr"])))
        m.hp = max(0, m.hp - dmg)
        print(f"{spell} automatically strikes for {dmg}! {m.name} HP {m.hp}")
        return True
    elif s["type"] == "heal":
        amt = max(1, roll(s["amount"]) + c.mod(s["attr"]))
        c.hp = min(c.max_hp, c.hp + amt)
        print(f"You cast {spell} and heal {amt}. HP {c.hp}/{c.max_hp}")
        return True
    elif s["type"] == "buff_ac":
        c.effects.ac_buff += s["bonus"]
        c.effects.ac_turns = max(c.effects.ac_turns, s["turns"])
        print(f"{spell} grants +{s['bonus']} AC for {s['turns']} turns.")
        return True
    else:
        print("Spell fizzles.")
        return False

def cast_spell_out_of_combat(c: Character, spell: str):
    if spell not in c.spells or spell not in SPELLS:
        print("You don't know that spell.")
        return
    s = SPELLS[spell]
    if s["type"] == "heal":
        amt = max(1, roll(s["amount"]) + c.mod(s["attr"]))
        c.hp = min(c.max_hp, c.hp + amt)
        print(f"You cast {spell} and heal {amt}. HP {c.hp}/{c.max_hp}")
    elif s["type"] == "buff_ac":
        c.effects.ac_buff += s["bonus"]
        c.effects.ac_turns = max(c.effects.ac_turns, s["turns"])
        print(f"{spell} grants +{s['bonus']} AC for {s['turns']} turns.")
    else:
        print("That spell is best used in combat.")

def drink_potion(c: Character, name: str) -> bool:
    if name not in c.potions or c.potions[name] <= 0:
        print("You don't have that potion.")
        return False
    c.potions[name] -= 1
    effect = POTIONS.get(name, {}).get("effect")
    if effect == "heal_10":
        heal = 10
        c.hp = min(c.max_hp, c.hp + heal)
        print(f"You drink {name} and heal {heal}. HP {c.hp}/{c.max_hp}")
    elif effect == "heal_25":
        heal = 25
        c.hp = min(c.max_hp, c.hp + heal)
        print(f"You drink {name} and heal {heal}. HP {c.hp}/{c.max_hp}")
    else:
        print("It tastes… fine?")
    return True

# --------------------------
# Main
# --------------------------
def main():
    print("Type NEW to start a new adventure, LOAD to continue, or HOF to view the Hall of Fame.")
    while True:
        choice = input("> ").strip().lower()
        if choice == "new":
            c = new_character()
            d = generate_dungeon(rows=10, cols=10)
            town_menu(c, d)
        elif choice == "load":
            c, d = load_game()
            if c and d:
                town_menu(c, d)
            else:
                print("Starting a new game instead.")
                c = new_character()
                d = generate_dungeon(rows=10, cols=10)
                town_menu(c, d)
        elif choice == "hof":
            show_hof()
        else:
            print("Type NEW, LOAD, or HOF.")

if __name__ == "__main__":
    main()

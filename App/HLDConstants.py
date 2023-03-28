# constant values for names/IDs used by the game

class HLDConstants():


    # all valid savedata fields and their types.
    # types are a sequence of any of str, int, float, list, map.
    # list takes 1 arg, map takes 2
    fields = {"badass": ["float"],
              "bosses": ["map", "int", "list", "int"],
              "bossGearbits": ["list", "str"],
              "cape": ["float"],
              "cCapes": ["list", "int"],
              "CH": ["float"],
              "charDeaths": ["float"],
              "checkAmmo": ["float"],
              "checkBat": ["float"],
              "checkCID": ["float"],
              "checkHP": ["float"],
              "checkRoom": ["float"],
              "checkStash": ["float"],
              "checkX": ["float"],
              "checkY": ["float"],
              "cl": ["map", "int", "list", "int"],
              "compShell": ["float"],
              "cShells": ["list", "int"],
              "cSwords": ["list", "int"],
              "cues": ["list", "int"],
              "dateTime": ["float"],
              "destruct": ["map", "int", "list", "float"],
              "drifterkey": ["float"],
              "enemies": ["map", "int", "list", "float"], # TODO - list contains multiple types (int, float, str), needs to handle special case
              "eq00": ["float"],
              "eq01": ["float"],
              "events": ["list", "int"],
              "fireplaceSave": ["float"],
              "gameName": ["str"],
              "gear": ["float"],
              "gearReminderTimes": ["float"],
              "gunReminderTimes": ["float"],
              "halluc": ["float"],
              "hasMap": ["float"],
              "healthKits": ["list", "int"],
              "healthUp": ["float"],
              "mapMod": ["map", "int", "list", "int"],
              "newcomerHoardeMessageShown": ["float"],
              "noSpawn": ["list", "int"],
              "noviceMode": ["float"],
              "permaS": ["map", "int", "int"],
              "playT": ["float"],
              "rooms": ["list", "int"],
              "sc": ["list", "int"],
              "scUp": ["list", "int"],
              "scK": ["map", "int", "int"],
              "skill": ["list", "int"],
              "specialUp": ["float"],
              "successfulCollectTimes": ["float"],
              "successfulHealTimes": ["float"],
              "successfulWarpTimes": ["float"],
              "sword": ["float"],
              "tablet": ["list", "int"],
              "tutHeal": ["float"],
              "values": ["map", "str", "int"],
              "warp": ["list", "int"],
              "well": ["list", "int"],
              "wellMap": ["list", "int"]}

    north_modules = [
        (-1084059, "After Pink Drifter"),
        (-1047430, "Pillar Room"),
        (-932471, "Drop Spiral"),
        (-902212, "Drop Arena"),
        (-1895481, "Crush Arena"),
        (-813235, "Cathedral Arena"),
        (-767783, "Birds"),
        (-1137428, "Dark Room")
        ]
    east_modules = [
        (-255100, "Water Tunnel"),
        (-187905, "Mega Huge Lab"),
        (-167326, "Flame Room"),
        (-53392, "After Pillar"),
        (-118694, "Docks Lab Arena"),
        (-88709, "Frog Arena"),
        (-68841, "Big Bog Lab"),
        (-18778, "Flame Dash Challenge")
         ]
    south_modules = [
        (-416223, "Mimic"),
        (-417825, "Scythe"),
        (-602007, "Pre-Baker 1"),
        (-596678, "Pre-Baker 2"),
        (-555279, "Bullet Baker"),
        (-398635, "Pre-Archer 1"),
        (-386457, "Pre-Archer 2"),
        (-676357, "Dash Challenge")
        ]
    west_modules = [
        (101387, "Bridge Vault"),
        (185267, "Tanuki Arena"),
        (206139, "Dogs"),
        (266784, "Cliffside Cells"),
        (335443, "Prison Hall"),
        (353953, "Thin Forest Secret"),
        (403666, "Meadow Vault"),
        (435082, "Tanuki Trouble")
        ]

    gun_ids = [
        (1, "Pistol"),
        (2, "Zeliska"),
        (21, "Laser"),
        (23, "Railgun"),
        (41, "Diamond Shotgun"),
        (43, "Shotgun")
        ]

    area_ids = [
        (0, "East"),
        (1, "North"),
        (2, "West"),
        (3, "South"),
        (4, "Town")
        ]
    pillar_ids = area_ids[:-1] # no pillar in town

    skill_ids = [
        (1, "Charge Slash"),
        (2, "Bullet Deflect"),
        (3, "Phantom Slash"),
        (4, "Chain Dash"),
        (5, "Bullet Shield"),
        (6, "Dash Stab")
        ]

    cpstate_fields = [
        ("checkHP", "Health"),
        ("checkBat", "Gun Ammo (%)"),
        ("checkStash", "Medkits"),
        ("checkAmmo", "Grenade Ammo")
        ]
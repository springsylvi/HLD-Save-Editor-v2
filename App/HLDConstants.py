class ListMap():
    """
    A map with a defined ordering which can be indexed into. Values are assumed to be unique.
    """

    # data : list of pairs, first element of each tuple is the map key, second is the value
    def __init__(self, data):
        self.ilist = [x[1] for x in data]
        self.imap = {a:b for a,b in data}
        self.reverse_imap = {b:a for a,b in data}

    # return value from map key
    def get(self, key):
        return self.imap.get(key)

    # return key from value
    def get_key(self, value):
        return self.reverse_imap.get(value)

    # return list of values
    def get_values(self):
        return self.ilist

    # return list of pairs
    def get_pairs(self):
        return [(a,b) for a,b in self.imap.items()]

    # return value from list index
    def __getitem__(self, index):
        return self.ilist[index]


class DisplayInfo():
    """
    Contains info about how to display a type of display field.
    """

    # displaytype is what type of UI element is displayed, const_data type varies based on displaytype, row_num is only used for checkboxlist type
    # displaytype values are [int, float, checkbox, checkboxlist, dropdown, other]
    def __init__(self, displaytype, displaytitle, const_data, row_num=None):
        self.displaytype = displaytype
        self.displaytitle = displaytitle
        self.const_data = const_data
        self.row_num = row_num

    def get_displaytype(self):
        return self.displaytype

    def get_title(self):
        return self.displaytitle
    
    def get_const_data(self):
        return self.const_data

    def get_row_num(self):
        return self.row_num


# constant values
class HLDConstants():

    # dict of ids to (internal name, common name) tuples
    roomNames = {
        46: ("rm_in_01_brokenshallows", "Broken Shallows"),
        47: ("rm_in_02_tutorial", "Tutorial 1"),
        48: ("rm_in_03_tut_combat", "Tutorial Arena"),
        49: ("rm_in_horizoncliff", "Horizon Cliff"),
        50: ("rm_in_halucinationdeath", "Hallucination Death"),
        51: ("rm_in_drifterfire", "Drifter Fire"),
        52: ("rm_in_blackwaitroom", "Black Wait Room"),
        53: ("rm_in_backertablet", "Monolith Room"),
        55: ("rm_inl_secrets", "Secrets Tutorial (Unused)"),
        56: ("rm_lin_gaps", "Gaps Tutorial (Unused)"),
        57: ("rm_lin_combat", "Combat Tutorial (Unused)"),
        60: ("rm_c_drifterworkshop", "Drifter Workshop"),
        61: ("rm_c_central", "Town"),
        62: ("rm_c_dregs_n", "North Dregs"),
        63: ("rm_c_dregs_s", "South Dregs"),
        64: ("rm_c_dregs_e", "East Dregs"),
        65: ("rm_c_dregs_w", "West Dregs"),
        66: ("rm_c_ven_apoth", "Medkit Shop"),
        67: ("rm_c_ven_dash", "Dash Shop"),
        68: ("rm_c_ven_gun", "Gun Shop"),
        69: ("rm_c_ven_spec", "Grenade Shop"),
        70: ("rm_c_ven_sdojo", "Sword Shop"),
        71: ("rm_carena", "Soccer Field"),
        72: ("rm_pax_staging", "Horde Lobby"),
        73: ("rm_pax_arena1", "South Horde"),
        74: ("rm_pax_arena2", "North Horde"),
        75: ("rm_pax_arenae", "East Horde"),
        76: ("rm_pax_arenaw", "West Horde"),
        78: ("rm_c_backertabletx", "Backer Tablet"),
        79: ("rm_televatorshaft", "Elevator Cutscene"),
        84: ("rm_nl_entrancepath", "Entrance Path"),
        85: ("rm_nx_titanvista", "Titan Vista"),
        86: ("rm_nx_northhall", "North Dark Room"),
        87: ("rm_nl_cavevault", "Blue Cloak"),
        88: ("rm_nx_aftertitan", "Cliffs"),
        89: ("rm_nc_npchatchery", "NPC Hatchery"),
        90: ("rm_nx_shrinepath", "Shrine Path"),
        91: ("rm_nl_shrinepath2vault", "Shrine Path Vault"),
        92: ("rm_nx_cave01", "Cave 01"),
        93: ("rm_nx_shrinepath_2", "Shrine Path 2"),
        94: ("rm_nx_mooncourtyard", "Moon Courtyard"),
        95: ("rm_nx_towerlock", "North Pillar"),
        96: ("rm_nc_cliffcampfire", "Cliff Campfire"),
        97: ("rm_nl_tobrokenshallows", "Broken Shallows Stairs"),
        98: ("rm_nx_stairs03", "Stairs 03"),
        100: ("rm_nl_warproom", "Crusher Key"),
        101: ("rm_nl_crushwarphall", "Crush Warp Hall"),
        102: ("rm_nl_crushtransition", "Crush Transition"),
        103: ("rm_nl_crushbackloop", "Crush Loop"),
        104: ("rm_nc_crusharena", "Crush Arena"),
        106: ("rm_nl_dropspiralopen", "Drop Spiral"),
        107: ("rm_nl_droppits", "Drop Pits"),
        108: ("rm_nl_dropblockcultfight", "Drop Block Cult Fight"),
        109: ("rm_nl_droparena", "Drop Arena"),
        111: ("rm_nl_gapopening", "Waterfall 1"),
        112: ("rm_nx_gapwide", "Waterfall 2"),
        113: ("rm_nl_gaphallway", "Waterfall 3"),
        114: ("rm_nl_risingarena", "Waterfall Arena"),
        116: ("rm_nx_cathedralentrance", "Cathedral Entrance"),
        117: ("rm_nx_cathedralhall", "Cathedral Hall"),
        118: ("rm_nl_altarthrone", "Altar Throne"),
        119: ("rm_nx_spiralstaircase", "Cathedral Stairs"),
        120: ("rm_nx_librariantablet", "Librarian Tablet"),
        121: ("rm_nx_jerkpope", "Jerk Pope"),
        123: ("rm_nl_stairascent", "Birds Module"),
        124: ("rm_nl_crusharena", "Crush Arena 2 (Unused)"),
        128: ("rm_sx_southopening", "South Opening"),
        129: ("rm_ch_ctemplate", "Barrel Room"),
        130: ("rm_sx_towersouth", "South Warp"),
        131: ("rm_sx_npc", "South NPC"),
        132: ("rm_s_gauntlet_elevator", "South Dash Challenge"),
        133: ("rm_ch_bgunpillars", "Sky Factory 1"),
        134: ("rm_ch_bfinal", "Sky Factory 2"),
        135: ("rm_s_gauntletend", "Sky Factory 3"),
        137: ("rm_ch_bdirkdemolition", "South Left Elevator"),
        139: ("rm_ch_tabigone", "Baker Module 1"),
        140: ("rm_ch_cgateblock", "Baker Module 2"),
        141: ("rm_ch_bmaddash", "Baker Arena"),
        142: ("rm_ch_tlongestroad", "Baker Path 4"),
        143: ("rm_s_bulletbaker", "Bullet Baker"),
        144: ("rm_ch_cendhall", "Baker Module 3"),
        146: ("rm_ch_cturnhall", "Mimic Path 1"),
        147: ("rm_ch_bfps", "Mimic Path 2"),
        148: ("rm_ch_cbigggns", "Crusher Room"),
        149: ("rm_ch_cspawnground", "Mimic Arena"),
        150: ("rm_s_countaculard", "Mimic"),
        152: ("rm_ch_acorner", "South Right Elevator"),
        154: ("rm_ch_bdirkdeluge", "Scythe Path 1"),
        155: ("rm_ch_bpods", "Scythe Path 2"),
        156: ("rm_ch_bgundirkdash", "Scythe Arena"),
        157: ("rm_s_markscythe", "Mark Scythe"),
        158: ("rm_s_gauntletlinkup", "Gauntlet Linkup"),
        160: ("rm_ch_apillarbird", "Archer Path 1"),
        161: ("rm_ch_cspiral", "C Spiral"),
        162: ("rm_ch_tbirdstandoff", "Archer Path 3"),
        163: ("rm_ch_bleaperfall", "Leaper Fall"),
        164: ("rm_s_bennyarrow", "Archer"),
        165: ("rm_s_gauntlettitanfinale", "Gauntlet Titan"),
        171: ("rm_ea_eastopening", "East Opening"),
        172: ("rm_ec_swordbridge", "Sword Bridge"),
        173: ("rm_el_flameelevatorenter", "Flame Elevator"),
        174: ("rm_ea_watertunnellab", "Water Tunnel"),
        175: ("rm_ec_theplaza", "Plaza"),
        176: ("rm_ec_npcdrugden", "NPC Drug Den"),
        177: ("rm_ex_towereast", "Tower East"),
        178: ("rm_eb_bogstreet", "Bog Street"),
        179: ("rm_ec_plazatoloop", "Plaza to Loop"),
        181: ("rm_el_megahugelab", "Mega Huge Lab"),
        182: ("rm_eb_meltymasharena", "Melty Mash Arena"),
        183: ("rm_eb_flamepitlab", "Flame Room"),
        184: ("rm_el_flameelevatorexit", "Lab Elevator"),
        185: ("rm_eb_deadotterwalk", "Otter Walk"),
        187: ("rm_ec_plazaaccesslab", "White Cloak"),
        188: ("rm_ec_dockslab", "Docks Lab"),
        189: ("rm_ex_dockscampfire", "Docks Campfire"),
        190: ("rm_ev_docksbridge", "Docks"),
        191: ("rm_el_frogarena", "Frog Arena"),
        193: ("rm_ec_bigboglab", "Big Bog Lab"),
        194: ("rm_ea_bogtemplecamp", "Bog Temple Camp"),
        195: ("rm_ea_frogboss", "Toad"),
        196: ("rm_ec_templeishvault", "East Pillar"),
        198: ("rm_ec_eastloop", "East Loop"),
        199: ("rm_ec_looplab", "Loop Lab"),
        200: ("rm_eb_meltyleaperarena", "Loop Arena"),
        202: ("rm_ec_plazatodocks", "Plaza to Docks (Unused)"),
        203: ("rm_ea_dockfightlab", "Dock Fight Lab (Unused)"),
        204: ("rm_eb_underotterbigriflerumble", "Big Rifle Rumble (Unused)"),
        205: ("rm_eb_cleanershole", "Toad 2 (unused)"),
        209: ("rm_wa_entrance", "West Entrance"),
        210: ("rm_wl_prisonhalvault", "West Vault 1"),
        211: ("rm_wa_deadwood", "Dead Wood"),
        212: ("rm_wa_deadwoods1", "Well Room"),
        213: ("rm_wa_grotto_buffintro", "Grotto"),
        214: ("rm_wc_windingwood", "Winding Wood"),
        215: ("rm_wc_grottonpc", "Grotto NPC"),
        216: ("rm_wl_npctreehouse", "NPC Treehouse"),
        217: ("rm_wc_minilab", "Mini Lab"),
        218: ("rm_wt_thewood", "The Wood"),
        219: ("rm_wa_entswitch", "West Warp"),
        220: ("rm_wc_meadowoodcorner", "Dogs Module"),
        222: ("rm_wb_treetreachery", "Tree Treachery"),
        223: ("rm_wl_westdriftervault", "Blue-Green Outfit"),
        225: ("rm_wt_slowlab", "Slow Lab"),
        226: ("rm_wc_cliffsidecellsredux", "Cliffside Cells"),
        227: ("rm_wc_prisonhal", "Prison Arena"),
        229: ("rm_wc_thinforest", "Thin Forest"),
        230: ("rm_wc_simplepath", "Simple Path"),
        231: ("rm_wc_crystallake", "Crystal Lake"),
        232: ("rm_wc_crystallakevault", "Yellow Cloak"),
        233: ("rm_wc_prisonhallend", "Prison Hall"),
        234: ("rm_wc_thinforestlow", "Thin Forest Low"),
        235: ("rm_wc_thinforestlowsecret", "Thin Forest Secret"),
        236: ("rm_wa_titanfalls", "Titan Falls"),
        238: ("rm_wa_vale", "Vale"),
        239: ("rm_wc_bigmeadow", "Big Meadow"),
        240: ("rm_wc_bigmeadowvault", "Big Meadow Vault"),
        241: ("rm_wc_meadowcavecrossing", "Meadow Cave Crossing"),
        242: ("rm_wb_bigbattle", "Big Battle"),
        243: ("rm_wb_tanukitrouble", "Tanuki Trouble"),
        244: ("rm_wc_ruinclearing", "Ruin Clearing"),
        245: ("rm_wx_boss", "General"),
        246: ("rm_wa_towerenter", "West Pillar"),
        247: ("rm_wa_multientrancelab", "West Dark Room"),
        248: ("rm_wa_crsytaldescent", "Crystal Descent"),
        250: ("rm_wa_grottox", "Grotto X (Unused)"),
        251: ("rm_wb_crystalqueen", "Crystal Queen (Unused)"),
        252: ("rm_wt_protogrid", "Proto Grid (Unused)"),
        253: ("rm_wv_puzzlepalacenew", "Puzzle Palace (Unused)"),
        256: ("rm_a_elevatorshaftupper", "Abyss Elevator 1"),
        257: ("rm_a_elevatorshaft", "Abyss Elevator 2"),
        258: ("rm_a_predownward", "Abyss Cough"),
        259: ("rm_a_downward", "Abyss Stairs"),
        260: ("rm_a_downwarddead", "Final Room"),
        261: ("rm_a_downwarddeadrevisit", "Final Room (Drifter Dead)"),
        262: ("rm_a_emberroom", "Judgement"),
        265: ("rm_bossrush_hub", "Boss Rush Hub"),
        266: ("rm_bossrush_frogboss", "Boss Rush Toad"),
        267: ("rm_bossrush_jerkpope", "Boss Rush Pope"),
        268: ("rm_bossrush_general", "Boss Rush General"),
        269: ("rm_bossrush_bulletbaker", "Boss Rush Baker"),
        270: ("rm_bossrush_countaculard", "Boss Rush Mimic"),
        271: ("rm_bossrush_markscythe", "Boss Rush Scythe"),
        272: ("rm_bossrush_bennyarrow", "Boss Rush Archer"),
        273: ("rm_bossrush_ember", "Boss Rush Judgement")
        }

    # all valid savedata fields and their types.
    # types are a sequence of any of str, int, float, list, map, enemystruct.
    # list takes 1 arg, map takes 2.
    # used for converting between Savedata and .sav/.hlds files
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
              "enemies": ["map", "int", "enemystruct"],
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

    north_modules = ListMap([
        (-1084059, "After Pink Drifter"),
        (-1047430, "Pillar Room"),
        (-932471, "Drop Spiral"),
        (-902212, "Drop Arena"),
        (-1895481, "Crush Arena"),
        (-813235, "Cathedral Arena"),
        (-767783, "Birds"),
        (-1137428, "Dark Room")
        ])
    east_modules = ListMap([
        (-255100, "Water Tunnel"),
        (-187905, "Mega Huge Lab"),
        (-167326, "Flame Room"),
        (-53392, "After Pillar"),
        (-118694, "Docks Lab Arena"),
        (-88709, "Frog Arena"),
        (-68841, "Big Bog Lab"),
        (-18778, "Flame Dash Challenge")
         ])
    south_modules = ListMap([
        (-416223, "Mimic"),
        (-417825, "Scythe"),
        (-602007, "Pre-Baker 1"),
        (-596678, "Pre-Baker 2"),
        (-555279, "Bullet Baker"),
        (-398635, "Pre-Archer 1"),
        (-386457, "Pre-Archer 2"),
        (-676357, "Dash Challenge")
        ])
    west_modules = ListMap([
        (101387, "Bridge Vault"),
        (185267, "Tanuki Arena"),
        (206139, "Dogs"),
        (266784, "Cliffside Cells"),
        (335443, "Prison Hall"),
        (353953, "Thin Forest Secret"),
        (403666, "Meadow Vault"),
        (435082, "Tanuki Trouble")
        ])

    gun_ids = ListMap([
        (1, "Pistol"),
        (2, "Zeliska"),
        (21, "Laser"),
        (23, "Railgun"),
        (41, "Diamond Shotgun"),
        (43, "Shotgun")
        ])

    area_ids = ListMap([
        (0, "East"),
        (1, "North"),
        (2, "West"),
        (3, "South"),
        (4, "Town")
        ])
    well_ids = ListMap([
        (0, "East"),
        (1, "North"),
        (2, "West"),
        (3, "South")
        ])

    skill_ids = ListMap([
        (1, "Charge Slash"),
        (2, "Bullet Deflect"),
        (3, "Phantom Slash"),
        (4, "Chain Dash"),
        (5, "Bullet Shield"),
        (6, "Dash Stab")
        ])

    # north: 1-4, south: 5-8, east: 9-12, west: 13-16
    tablet_ids = ListMap([
        (1, "Stairs"),
        (2, "Cliffs NPC Cave"),
        (3, "Cathedral"),
        (4, "8 Module Door"),
        (5, "After Baker"),
        (6, "Right Elevator"),
        (7, "Before Mimic"),
        (8, "Before Baker"),
        (9, "Pink Drifter"),
        (10, "Plaza"),
        (11, "Before Boss"),
        (12, "8 Module Door"),
        (13, "Key Door"),
        (14, "8 Module Door"),
        (15, "Before Pink Drifter"),
        (16, "After Pillar")
        ])
    #east_tablet_ids = ListMap(tablet_ids[8:12])
    #north_tablet_ids = ListMap(tablet_ids[0:4])
    #west_tablet_ids = ListMap(tablet_ids[12:16])
    #south_tablet_ids = ListMap(tablet_ids[4:8])
    
    # TODO - remove explicit indices and turn into list of strings?
    outfit_ids = ListMap([
        (0, "Red (Default)"),
        (1, "Blue"),
        (2, "Fuschia"),
        (3, "White"),
        (4, "Yellow"),
        (5, "Orange"),
        (6, "Blue/Green"),
        (7, "Pink"),
        (8, "Black"),
        (9, "Ochre"),
        (10, "Purple"),
        (11, "New Game +")
        ])



    # list of each individual value the user can interact with through the UI (some savedata fields are split across multiple display fields or vice versa)
    # tuple elements are unique name, displayinfo obj
    # TODO - add extra elements (i.e. field names in input_fields that aren't in the savefile)
    display_fields = ListMap([
        ("badass", DisplayInfo("int", "Pink Drifter Conversations", None)),
        #("bosses", lambda sd: sd.get("bosses"), DisplayInfo("other", "Bosses Killed", None)), #TODO - creat const_data for bosses
        #"bossGearbits": ["list", "str"],
        ("cape", DisplayInfo("dropdown", "Cape", outfit_ids)),
        ("cCapes", DisplayInfo("checkboxlist", "Capes Owned", outfit_ids, 6)),
        ("CH", DisplayInfo("checkbox", "Alt Drifter", None)),
        #("charDeaths", lambda sd: sd.get("CH"), DisplayInfo("int", "Total Deaths", None)),
        ("checkAmmo", DisplayInfo("float", "Grenade Ammo", None)),
        ("checkBat", DisplayInfo("float", "Gun Ammo (%)", None)),
        #("checkCID", lambda sd: sd.get("checkCID"), DisplayInfo("index", "Checkpoint ID", None)),
        ("checkHP", DisplayInfo("int", "Health", None)),
        ("checkRoom", DisplayInfo("float", "Room ID", roomNames)),
        ("checkStash", DisplayInfo("int", "Medkits", None)),
        ("checkX", DisplayInfo("float", "X Position", None)),
        ("checkY", DisplayInfo("float", "Y Position", None)),
        #"cl": ["map", "int", "list", "int"],
        ("eastmodules", DisplayInfo("checkboxlist", "East Modules", east_modules, 8)),
        ("northmodules", DisplayInfo("checkboxlist", "North Modules", north_modules, 8)),
        ("westmodules", DisplayInfo("checkboxlist", "West Modules", west_modules, 8)),
        ("southmodules", DisplayInfo("checkboxlist", "South Modules", south_modules, 8)),
        ("compShell", DisplayInfo("dropdown", "Droid", outfit_ids)),
        ("cShells", DisplayInfo("checkboxlist", "Droids Owned", outfit_ids, 6)),
        ("cSwords", DisplayInfo("checkboxlist", "Swords Owned", outfit_ids, 6)),
        #("cCues", lambda sd: sd.get("cues"), DisplayInfo("?", "?", None)),
        #"dateTime": ["float"],
        #"destruct": ["map", "int", "list", "float"],
        ("drifterkey", DisplayInfo("int", "Keys", None)),
        #"enemies": ["map", "int", "list", "float"], # TODO - list contains multiple types (int, float, str), needs to handle special case
        #("eq00", lambda sd: sd.get("eq00"), DisplayInfo("dropdown", "Gun Slot 1", gun_ids)),
        #("eq01", lambda sd: sd.get("eq01"), DisplayInfo("dropdown", "Gun Slot 2", gun_ids)),
        #"events": ["list", "int"],
        ("fireplaceSave", DisplayInfo("checkbox", "Game Completed", None)),
        ("gameName", DisplayInfo("str", "Savefile Name", None)),
        ("gear", DisplayInfo("int", "Unspent Gearbits", None)),
        #"gearReminderTimes": ["float"],
        #"gunReminderTimes": ["float"],
        #"halluc": ["float"],
        ("hasMap", DisplayInfo("checkbox", "Map Collected", None)),
        #"healthKits": ["list", "int"],
        ("healthUp", DisplayInfo("int", "Extra Medkit Slots", None)),
        #"mapMod": ["map", "int", "list", "int"],
        #"newcomerHoardeMessageShown": ["float"],
        #"noSpawn": ["list", "int"],
        ("noviceMode", DisplayInfo("checkbox", "Novice Mode", None)),
        #"permaS": ["map", "int", "int"],
        #"playT": ["float"],
        #"rooms": ["list", "int"],
        ("sc", DisplayInfo("checkboxlist", "Guns Owned", gun_ids, 6)),
        ("scUp", DisplayInfo("checkboxlist", "Guns Upgraded", gun_ids, 6)),
        #"scK": ["map", "int", "int"],
        ("skill", DisplayInfo("checkboxlist", "Skills", skill_ids, 6)),
        ("specialUp", DisplayInfo("int", "Max Grenades", None)),
        #"successfulCollectTimes": ["float"],
        #"successfulHealTimes": ["float"],
        #"successfulWarpTimes": ["float"],
        ("sword", DisplayInfo("dropdown", "Sword", None)),
        ("tablet", DisplayInfo("checkboxlist", "Monoliths", tablet_ids, 4)),
        #"tutHeal": ["float"],
        #"values": ["map", "str", "int"],
        ("warp", DisplayInfo("checkboxlist", "Warp Points", area_ids, 5)),
        ("well", DisplayInfo("checkboxlist", "Pillars", well_ids, 4)),
        #"wellMap": ["list", "int"]
        ("outfits", DisplayInfo("checkboxlist", "Outfits", outfit_ids, 6))
        ])

"""SYNTHETIC DATA ONLY. Deterministic name, contact and contractor generator.

Names are drawn from a hash of (seed, kind, id), never from the simulation
random stream, so adding names does not change any other generated value for
the same seed. Phone numbers use the Ofcom reserved drama ranges and emails use
the reserved example.com domain, so no generated contact can reach a real
person."""
import random
import zlib

FIRST_F = {
    "uk": ["Margaret", "Susan", "Karen", "Julie", "Linda", "Carol", "Sharon", "Michelle", "Joanne", "Lisa",
           "Angela", "Donna", "Tracey", "Wendy", "Dawn", "Gillian", "Pauline", "Christine", "Jean", "Brenda",
           "Lorraine", "Hazel", "Shirley", "Maureen", "Kath", "Amy", "Sophie", "Chloe", "Emma", "Hannah",
           "Rebecca", "Natalie", "Kirsty", "Leanne", "Stacey", "Nicola", "Claire", "Gemma", "Jade", "Megan"],
    "asian": ["Aisha", "Fatima", "Priya", "Sunita", "Nasreen", "Yasmin", "Meera", "Rukhsana", "Sana", "Anjali"],
    "african": ["Grace", "Blessing", "Ngozi", "Amara", "Esther", "Joy", "Mercy", "Abena"],
    "european": ["Agnieszka", "Katarzyna", "Ioana", "Elena", "Marta", "Anna", "Dagmara", "Zofia"],
}
FIRST_M = {
    "uk": ["David", "John", "Michael", "Paul", "Peter", "Stephen", "Ian", "Gary", "Mark", "Kevin",
           "Brian", "Alan", "Keith", "Dennis", "Derek", "Trevor", "Malcolm", "Raymond", "Terry", "Colin",
           "Barry", "Neil", "Graham", "Stuart", "Lee", "Craig", "Darren", "Jamie", "Liam", "Callum",
           "Connor", "Jordan", "Ryan", "Luke", "Jack", "Daniel", "Adam", "Scott", "Ross", "Nathan"],
    "asian": ["Mohammed", "Imran", "Rajesh", "Amir", "Tariq", "Sanjay", "Ahmed", "Hamza", "Vikram", "Bilal"],
    "african": ["Emmanuel", "Samuel", "Kwame", "Chidi", "Tunde", "Kofi", "Daniel", "Isaac"],
    "european": ["Piotr", "Tomasz", "Marek", "Andrei", "Mihai", "Jakub", "Pawel", "Stefan"],
}
SURNAMES = {
    "uk": ["Robson", "Charlton", "Dodds", "Hall", "Armstrong", "Elliott", "Forster", "Hedley", "Oliver",
           "Pattinson", "Reay", "Surtees", "Telford", "Carr", "Nicholson", "Scott", "Wilson", "Taylor",
           "Brown", "Smith", "Walker", "Wright", "Thompson", "Johnson", "Graham", "Henderson", "Ramsey",
           "Lawson", "Hunter", "Bell", "Dixon", "Fenwick", "Gibson", "Hutchinson", "Jackson", "Kirkup",
           "Liddle", "Mitchell", "Nixon", "Ord", "Peacock", "Richardson", "Short", "Turnbull", "Urwin",
           "Vickers", "Watson", "Young", "Atkinson", "Brewis", "Cowell", "Dunn", "English", "Fairless",
           "Gray", "Heron", "Ingham", "Jobling", "Knox", "Lamb", "Maughan", "Noble", "Proud", "Rutter"],
    "asian": ["Khan", "Ahmed", "Hussain", "Patel", "Singh", "Begum", "Ali", "Iqbal", "Sharma", "Chaudhry"],
    "african": ["Okafor", "Mensah", "Adeyemi", "Nkomo", "Owusu", "Banda", "Osei", "Abara"],
    "european": ["Kowalski", "Nowak", "Wisniewski", "Popescu", "Ionescu", "Novak", "Kaminski", "Horvat"],
}
ORIGIN_MIX = [("uk", 0.86), ("asian", 0.06), ("african", 0.04), ("european", 0.04)]

TITLES_F = [("Mrs", 0.38), ("Ms", 0.32), ("Miss", 0.28), ("Dr", 0.02)]
TITLES_M = [("Mr", 0.97), ("Dr", 0.03)]

COMPANIES = {
    "SUP-F1": ("Tyne Fabric Insulation Ltd", "0191 498 0140", "Cavity, loft and internal wall insulation",
               ["Callum Dunn", "Rhys Pattinson", "Liam Heron", "Jordan Short", "Aaron Telford"]),
    "SUP-F2": ("Northern Facade Systems Ltd", "0191 498 0155", "External wall insulation",
               ["Gareth Lowther", "Marek Nowak", "Darren Jobling", "Ryan Kirkup", "Stefan Horvat"]),
    "SUP-HP": ("Cleveland Heat Pump Installations Ltd", "01642 496 0170", "Air source heat pump installation",
               ["Imran Hussain", "Kevin Maughan", "Sanjay Patel", "Ben Urwin", "Tomasz Kaminski"]),
    "SUP-HT": ("Wearside Heating and Gas Ltd", "0191 498 0185", "Boilers, controls and gas safety",
               ["Neil Atkinson", "Paul Fenwick", "Amir Khan", "Scott Liddle", "Lee Nixon"]),
    "SUP-RA": ("Teesdale Repairs and Maintenance Ltd", "01642 496 0190", "Remedial repairs",
               ["Mark Cowell", "Dennis Rutter", "Jamie Ord", "Colin Brewis"]),
}

STAFF_NAMES = {
    "PM-01": ("Helen", "Marsden"), "PS-01": ("Priya", "Nair"), "RC-01": ("Daniel", "Hedley"),
    "RC-02": ("Rachel", "Forster"), "RC-03": ("Tom", "Atkinson"), "RLO-01": ("Sandra", "Graham"),
    "RLO-02": ("Aisha", "Rahman"), "RLO-03": ("Gillian", "Reay"), "GEO-01": ("Michael", "Okafor"),
    "QA-01": ("Alan", "Dixon"), "BSL-01": ("Karen", "Lawson"),
}


def _rng(seed, kind, key):
    return random.Random(zlib.crc32(f"{seed}|{kind}|{key}".encode()))


def _pick(rng, pairs):
    r, acc = rng.random(), 0.0
    for value, weight in pairs:
        acc += weight
        if r < acc:
            return value
    return pairs[-1][0]


def person(seed, kind, key, gender=None):
    """Return a dict with title, first, last, full, preferred and gender."""
    rng = _rng(seed, kind, key)
    origin = _pick(rng, ORIGIN_MIX)
    gender = gender or ("F" if rng.random() < 0.58 else "M")
    first = rng.choice((FIRST_F if gender == "F" else FIRST_M)[origin])
    last = rng.choice(SURNAMES[origin])
    title = _pick(rng, TITLES_F if gender == "F" else TITLES_M)
    return {"title": title, "first": first, "last": last, "full": f"{first} {last}",
            "formal": f"{title} {last}", "gender": gender, "origin": origin}


def phone(seed, key, mobile_share=0.62):
    """Ofcom drama-range numbers: 07700 900xxx mobile, 0191 498 0xxx landline."""
    rng = _rng(seed, "phone", key)
    if rng.random() < mobile_share:
        return f"07700 900{rng.randint(0, 999):03d}"
    return f"0191 498 0{rng.randint(0, 999):03d}"


def email(person_dict, key):
    n = zlib.crc32(str(key).encode()) % 90 + 10
    local = f"{person_dict['first']}.{person_dict['last']}{n}".lower().replace("'", "")
    return f"{local}@example.com"


def resident(seed, resident_ref):
    p = person(seed, "resident", resident_ref)
    rng = _rng(seed, "resident-extra", resident_ref)
    p["phone"] = phone(seed, resident_ref)
    p["email"] = email(p, resident_ref) if rng.random() < 0.55 else ""
    p["preferred"] = p["first"]
    return p


def representative(seed, resident_ref, resident_last):
    p = person(seed, "rep", resident_ref)
    rng = _rng(seed, "rep-rel", resident_ref)
    p["relationship"] = rng.choice(["Daughter", "Son", "Carer", "Partner", "Friend", "Advocate", "Sister"])
    if p["relationship"] in ("Daughter", "Son", "Sister"):
        p["last"] = resident_last
        p["full"] = f"{p['first']} {p['last']}"
    p["phone"] = phone(seed, f"rep-{resident_ref}", 0.8)
    return p


def contractor(code):
    name, tel, scope, operatives = COMPANIES[code]
    return {"code": code, "name": name, "phone": tel, "scope": scope, "operatives": operatives}


def operative(seed, code, key):
    ops = COMPANIES[code][3]
    return ops[_rng(seed, "op", key).randrange(len(ops))]


def staff(code):
    first, last = STAFF_NAMES.get(code, ("Alex", "Morgan"))
    return {"code": code, "name": f"{first} {last}", "email": f"{first}.{last}@propernorthhomes.example".lower()}

import tomllib
import collections

with open("data.toml", "rb") as f:
    data = tomllib.load(f)

def isDict(d):
    return type(d) is dict

def isFlat(d):
    if isDict(d):
        return not any(isDict(v) for v in d.values())
    return False

# To simplify for now, a three-level data structure
def trope_generator(data):
    for genus in data.values():
        if isDict(genus):
            for family in genus.values():
                if isDict(family):
                    for member in family.values():
                        if isFlat(member):
                            yield {"genus":genus["name"]} | {"family":family["name"]} | member

keys_ref = set(["name", "similar_to", "opposite_of", "description", "wikipedia", "example", "silva_rhetoricae", "genus", "family"])

for i in trope_generator(data):
    try:
        assert i["genus"] in ["Scheme", "Trope"]
    except AssertionError as e:
        print(f"Error in {i['genus']} --> {i['family']} --> {i['name']}")
        print(f"Bad genus: {i['genus']}")
    for k in i.keys():
        try:
            assert k in keys_ref
        except AssertionError as e:
            print(f"Error in {i['genus']} --> {i['family']} --> {i['name']}")
            print(f"Extra key: {k}")
            raise e
    for k in keys_ref:
        try:
            assert k in i.keys()
        except AssertionError as e:
            print(f"Error in {i['genus']} --> {i['family']} --> {i['name']}")
            print(f"Missing key: {k}")
            raise e
    try:
        assert isinstance(i["wikipedia"], list)
    except AssertionError as e:
        print(f"Error in {i['genus']} --> {i['family']} --> {i['name']}")
        print("wikipedia is not a list")
        raise e

for i in trope_generator(data):
    print(f"What is the definition of {i['name'].lower()}?")
    print(i["description"])
    print("---")
    print(f"What is this {i['genus'].lower()} describing?\n\n{i['description']}")
    print(i["name"])
    print("---")
    for example in i["wikipedia"]:
        print(f"{example}\n\nWhat is this quote an example of?")
        print(i["name"])
        print("---")

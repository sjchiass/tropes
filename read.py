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

def family_generator(data):
    for genus in data.values():
        if isDict(genus):
            for family in genus.values():
                if isDict(family):
                    yield {"members":[x["name"] for x in family.values() if isFlat(x)]} | {"name":family["name"]} | {"genus":genus["name"]}

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

def make_by_name(d):
    for i in trope_generator(d):
        yield f"What is the definition of {i['name'].lower()}?\t{i['description']}\n"

def make_by_description(d):
    for i in trope_generator(d):
        start = f"What {i['genus'].lower()} is this describing?<br><br>{i['description']}"
        end = f"\t{i['name']}\n"
        if i["example"]:
            start += "<br><br>Examples:"
            for e in i["example"]:
                start += f"<br>{e}"
        yield start+end

def make_by_quote(d):
    for i in trope_generator(d):
        for q in i["wikipedia"]:
            yield f"{q}<br><br>What is this quote an example of?\t{i['name']}: {i['description']}\n"
        for q in i["silva_rhetoricae"]:
            yield f"{q}<br><br>What is this quote an example of?\t{i['name']}: {i['description']}\n"

def make_by_example(d):
    for i in trope_generator(d):
        if i["example"]:
            yield f"What {i['genus'].lower()} are these examples of?<br><br>{'<br>'.join([e for e in i['example']])}\t{i['name']}<br><br>{i['description']}\n"

def make_by_members(d):
    for i in family_generator(d):
        yield f"What is the family of {i['genus'].lower()}s these belong to: {', '.join([x.lower() for x in i['members']])}?\t{i['name']}\n"

def make_by_family(d):
    for i in family_generator(d):
        yield f"What are the members of the {i['genus'].lower()} family named {i['name'].lower()}?\t{', '.join([x.lower() for x in i['members']])}\n"

with open("./test.tsv", "w") as f:
    for i in make_by_name(data):
        f.write(i)
    for i in make_by_description(data):
        f.write(i)
    for i in make_by_quote(data):
        f.write(i)
    for i in make_by_example(data):
        f.write(i)
    for i in make_by_members(data):
        f.write(i)
    for i in make_by_family(data):
        f.write(i)

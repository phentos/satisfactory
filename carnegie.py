import json
import re

"""
-> mDisplayName <-
-> mIngredients <-
-> mProduct
-> mManufactoringDuration
-> mProducedIn
"""

"""
values x1000:
    /Water/
    /Alumina/
"""

def getJson(fname):
    with open(fname, "r") as f:
        return json.load(f)


def getName(item):
    return item['mDisplayName']


def getClassName(item):
    return item['mClassName']


def getIngredients(item):
    text = item['mIngredients']

    re_name = r'Desc_(\w+)\.Desc'
    re_amount = r'Amount\=(\d+)'

    names = re.findall(re_name, text)

    amounts = re.findall(re_amount, text)
    amounts = [int(_) for _ in amounts]

    return dict(zip(names, amounts)) 


def getProduct(item):
    text = item['mProduct']

    re_name = r'Desc_(\w+)\.Desc'
    re_amount = r'Amount\=(\d+)'

    names = re.findall(re_name, text)

    amounts = re.findall(re_amount, text)
    amounts = [int(_) for _ in amounts]

    return dict(zip(names, amounts))


def getDuration(item):
    return int(float(item['mManufactoringDuration']))


def getProducer(item):
    producers = {"Assembler", "Constructor", "Manufacturer", "Refinery", "Packager", "Blender", "Particle Accelerator"}

    for producer in producers:
        if producer in item['mProducedIn']: 
            return producer


def getCraftOptions(collection, text):
    return list(filter(lambda item: text in getProduct(item), collection))


def buildCraftPaths(collection) -> dict:
    product_to_recipe = {}
    for item in collection:
        for product in getProduct(item):
            if product in product_to_recipe:
                product_to_recipe[product].append(item['ClassName'])
            else:
                product_to_recipe[product] = [item['ClassName']]
    return product_to_recipe


def buildRecipePaths(collection) -> dict:
    pass


def getRecipe(collection, text) -> dict:
    return list(filter(lambda x: x['ClassName'] == text))[0]

def getInputOutput(item, oc=1):
    # 'name':amount/(duration/1 min)

    inputs = getIngredients(item)
    outputs = getProduct(item)
    duration = getDuration(item)

    ins = {name:oc*(amount/(duration/60)) for name,amount in inputs.items()}
    outs = {name:oc*(amount/(duration/60)) for name,amount in outputs.items()}

    return {'input':ins, 'output':outs}

if __name__ == "__main__":
    r = getJson("Recipes.json")

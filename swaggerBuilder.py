import sys
import getopt
from json import load
from yaml import dump, SafeDumper

schemas = {}


class NoAliasDumper(SafeDumper):
    def ignore_aliases(self, data):
        return True


def entityBuilder(label, obj):
    global schemas
    schema = {
        "type": "object",
        "description": "edit this section",
        "example": obj,
        "properties": {}
    }
    properties = schema["properties"]
    for propertyLabel, propertyValue in obj.items():
        propertyType = type(propertyValue)
        properties[propertyLabel] = {
            "descirption": "edit this section",
            "example": propertyValue,
        }
        if propertyType == dict:
            entityBuilder(propertyLabel, propertyValue)
            ref = "$ref '#components/schema/"+propertyLabel+"Entity'"
            properties[propertyLabel] = str(ref)
        elif propertyType == list:
            properties[propertyLabel]["type"] = "array"
        elif propertyType == str:
            properties[propertyLabel]["type"] = "string"
        elif propertyType == int:
            properties[propertyLabel]["type"] = "integer"
        elif propertyType == float:
            properties[propertyLabel]["type"] = "number"
        elif propertyType == bool:
            properties[propertyLabel]["type"] = "boolean"
    schemas[f"{label}Entity"] = schema


def json2yaml(rootLabel, path, outPath="output.yaml"):
    with open(path) as f:
        data = load(f)
    entityBuilder(rootLabel, data)
    # print(schemas)
    out = dump(schemas, Dumper=NoAliasDumper)
    f = open(outPath, mode="w")
    f.write(out)
    f.close()

def help():
    print("swaggerBuilder.py -l <rootlabel> -p <path> ...[-o <outpath>]")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:p:o:", ["path=", "outpath="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    path, label, outPath = None, None, "output.yaml"
    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit()
        elif opt in ("-l", "--label"):
            label = arg
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-o", "--outpath"):
            outPath = arg
    if (label is None) or (path is None):
        help()
        sys.exit()
    json2yaml(label, path, outPath)

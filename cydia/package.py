import subprocess
from xml.dom.minidom import Document

# Just calling 7zip to build Packages.bz2 for us :)
subprocess.call("7z a -tbzip2 Packages.bz2 Packages")


class DictToXML(object):
    default_list_item_name = "item"

    def __init__(self, structure, list_mappings={}):
        self.doc = Document()

        if len(structure) == 1:
            rootName = str(list(structure.keys())[0])
            self.root = self.doc.createElement(rootName)

            self.list_mappings = list_mappings

            self.doc.appendChild(self.root)
            self.build(self.root, structure[rootName])

    def build(self, father, structure):
        if type(structure) == dict:
            for k in structure:
                tag = self.doc.createElement(k)
                father.appendChild(tag)
                self.build(tag, structure[k])
        elif type(structure) == list:
            tag_name = self.default_list_item_name

            if father.tagName in self.list_mappings:
                tag_name = self.list_mappings[father.tagName]

            for l in structure:
                tag = self.doc.createElement(tag_name)
                self.build(tag, l)
                father.appendChild(tag)
        else:
            data = str(structure)
            tag = self.doc.createTextNode(data)
            father.appendChild(tag)

    def display(self):
        print(self.doc.toprettyxml(indent="  "))

    def get_string(self):
        return self.doc.toprettyxml(indent="  ")


# Set up Packages file
with open('Packages', 'r') as file:
   Packages = file.read()
   file.close()

# Sort Packages file into separate package listings
PackagesSorted = Packages.split('\n\n')
PackageListFinal = []

# Convert each package listing to a dictionary
for x in PackagesSorted:
    PackageList = {}
    data = x.replace(': ', '\n').split('\n')
    for i,k in zip(data[0::2], data[1::2]):
        PackageList[i] = k.replace('https://how-bout-no.github.io/', '')
    PackageListFinal.append(PackageList)
	
# Necessary final dictionary
AllPackages = {"package": PackageListFinal}

# Convert final dictionary to XML file
xml = DictToXML(AllPackages)
with open('Packages.xml', 'w') as file:
    file.write(xml.get_string())
    file.close()

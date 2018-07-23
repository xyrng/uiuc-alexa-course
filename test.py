import json
import xmltodict
from urllib.request import urlopen

# link = "https://courses.illinois.edu/cisapp/explorer/schedule/2019/spring/AAS/100.xml"
# f = urlopen(link)
# xmlString = f.read()
# jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
# print(jsonString)
# json_items = json.loads(jsonString)
# print("sections are: ")
# list = [(lambda x: x["#text"])(x) for x in json_items["ns2:course"]["sections"]["section"]]
# print(list)


string = "CS and STAT and ECE is my love"
subjects = {"CS", "ECE", "AAS"}
subjects.add("STAT")

print(subjects)

# def test(a, b, c = 1):
#     print(a)
#     print(b)
#     print(c)
#
# print(1 != 2)

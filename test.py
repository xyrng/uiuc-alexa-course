import json
from parse import parse
from courses import *
import xmltodict
from urllib.request import urlopen

link = "https://courses.illinois.edu/cisapp/explorer/schedule/2018/fall/CS/241/45300.xml"
f = urlopen(link)
xmlString = f.read()
jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
json_items = json.loads(jsonString)
# with open('output.json', 'w') as f:
#     f.write(jsonString)
# print("sections are: ")
# list = [(lambda x: x["#text"])(x) for x in json_items["ns2:course"]["sections"]["section"]]
# print(list)
# print(combine_course(link))
professor = json_items["ns2:section"]["meetings"]["meeting"]["instructors"]
print(professor)
print(get_professors(professor))

link2 = "https://courses.illinois.edu/cisapp/explorer/schedule/2018/fall/CS/225/35919.xml"
f = urlopen(link2)
xmlString = f.read()
jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
json_items = json.loads(jsonString)

professor = json_items["ns2:section"]["meetings"]["meeting"]["instructors"]
print(professor)
print(get_professors(professor))

# def test(a, b, c = 1):
#     print(a)
#     print(b)
#     print(c)
#
# print(1 != 2)


# def get_lectures(link):
#     lec_sections = []
#     url = link + ".xml"
#     jsonString = parse(url)
#     json_items = json.loads(jsonString)
#     sections = json_items["ns2:course"]["sections"]["section"]
#     if type(sections) == list:
#         for sec in json_items["ns2:course"]["sections"]["section"]:
#             url = sec["@href"]
#             if is_lecture(url):
#                 lec_sections.append(sec["#text"])
#     return lec_sections
#
# def get_discussions(link):
#     dis_sections = []
#     url = link + ".xml"
#     jsonString = parse(url)
#     json_items = json.loads(jsonString)
#     sections = json_items["ns2:course"]["sections"]["section"]
#     if type(sections) == list:
#         for sec in json_items["ns2:course"]["sections"]["section"]:
#             url = sec["@href"]
#             if not is_lecture(url):
#                 dis_sections.append(sec["#text"])
#     return dis_sections

# temp = get_discussions(link)
# print(temp)
# print(readable_section(temp))
import json
import urllib
from urllib.request import urlopen
from parse import parse


course_url = "https://courses.illinois.edu/cisapp/explorer/schedule"

unreadable_subjects_title = {"CS", "ECE"}
unreadable_section_title = {'AL1', 'AL2', 'AYA', 'AYB', 'AYC', 'AYD', 'AYE', 'AYF', 'AYG', 'AYH', 'AYI', 'AYJ', 'AYK', 'AYL'}

#########################  BASIC FEATURE  ##################################
def make_prelink(year, semester, subject, courseIdx, section = None):
    link = course_url + "/" + year + "/" + semester + "/" + subject + "/" + courseIdx
    if section != None:
        link += "/" + section
    return link

def make_link(link, crn):
    link += "/" + crn
    return link

def get_sections(link):
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    list = [(lambda x: x["#text"])(x) for x in json_items["ns2:course"]["sections"]["section"]]
    print("list:")
    print(list)
    return list

def get_crn(link, section):
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    sections = json_items["ns2:course"]["sections"]["section"]
    crn = next(item for item in sections if item['#text'] == section)['@id']
    return crn

#TODO: add ", and" for last one
def get_days_of_week(days):
    if days == "n.a":
        return ["unknown"]
    list_of_days = []
    for c in days:
        if c == 'M':
            list_of_days.append("Monday")
        elif c == "T":
            list_of_days.append("Tuesday")
        elif c == "W":
            list_of_days.append("Wednesday")
        elif c == "R":
            list_of_days.append("Thursday")
        elif c == "F":
            list_of_days.append("Friday")
    return list_of_days

def get_professors(prof):
    list_of_prof = []
    professors = prof["instructor"]
    if type(professors) == list:
        for item in professors:
            name = "Professor " + item['@lastName']
            list_of_prof.append(name)
    else:
        name = "Professor " + prof["instructor"]['@lastName']
        list_of_prof.append(name)
    return list_of_prof

def get_lecture_detail(link):
    dict = {}
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    print("222")
    course = json_items["ns2:section"]
    course_title = course["parents"]["course"]["#text"]
    start_date = course["startDate"][0:10]
    end_date = course["endDate"][0:10]
    start_time = course["meetings"]["meeting"]["start"]
    print("nnn")
    end_time = course["meetings"]["meeting"]["end"]
    try:
        print("aaa")
        days_of_week = course["meetings"]["meeting"]["daysOfTheWeek"]
        print(days_of_week)
        days_of_week = get_days_of_week(days_of_week)
    except KeyError:
        print("bbb")
        days_of_week = []
    professor = course["meetings"]["meeting"]["instructors"]
    location = course["meetings"]["meeting"]["buildingName"]
    print("hhh")
    professor = get_professors(professor)
    print("sss")
    dict["course_title"] = course_title
    dict["start_date"] = start_date
    dict["end_date"] = end_date
    dict["start_time"] = start_time
    dict["end_time"] = end_time
    dict["days_of_week"] = days_of_week
    dict["professor"] = professor
    dict["location"] = location

    print(dict)
    return dict

def get_course_detail(link):
    dict = {}
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)

    course_title = json_items["ns2:course"]["label"]
    description = json_items["ns2:course"]["description"]
    description = description[0: description.find("Prerequisite")]
    credit = json_items["ns2:course"]["creditHours"]
    courseSectionInformation = readable_subject(json_items["ns2:course"]["courseSectionInformation"])
    try:
        genEdCategories = json_items["ns2:course"]["sectionDegreeAttributes"]
    except:
        genEdCategories = None

    dict["course_title"] = course_title
    dict["description"] = description
    dict["credit"] = credit
    dict["courseSectionInformation"] = courseSectionInformation
    dict["genEdCategories"] = genEdCategories
    return dict

def get_diss_detail(link):
    dict = {}
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    meetings = json_items["ns2:section"]["meetings"]["meeting"]
    if type(meetings) == list:
        one_more_dis = True
        dis_type = meetings[0]["type"]["#text"]
        start_time = meetings[0]["start"]
        end_time = meetings[0]["end"]
        days_of_week = meetings[0]["daysOfTheWeek"]
        location = meetings[0]["buildingName"]
        room = meetings[0]["roomNumber"]
        days_of_week = get_days_of_week(days_of_week)
        dict["one_more_dis"] = one_more_dis
        dict["dis_type"] = dis_type
        dict["start_time"] = start_time
        dict["end_time"] = end_time
        dict["days_of_week"] = days_of_week
        dict["location"] = location
        dict["room"] = room

        dis_type1 = meetings[1]["type"]["#text"]
        start_time1 = meetings[1]["start"]
        end_time1 = meetings[1]["end"]
        days_of_week1 = meetings[1]["daysOfTheWeek"]
        location1 = meetings[1]["buildingName"]
        room1 = meetings[1]["roomNumber"]
        days_of_week1 = get_days_of_week(days_of_week1)
        dict["dis_type1"] = dis_type1
        dict["start_time1"] = start_time1
        dict["end_time1"] = end_time1
        dict["days_of_week1"] = days_of_week1
        dict["location1"] = location1
        dict["room1"] = room1

        return dict

    else:
        one_more_dis = False
        dis_type = meetings["type"]["#text"]
        start_time = meetings["start"]
        end_time = meetings["end"]
        days_of_week = meetings["daysOfTheWeek"]
        location = meetings["buildingName"]
        room = meetings["roomNumber"]
        days_of_week = get_days_of_week(days_of_week)
        dict["one_more_dis"] = one_more_dis
        dict["dis_type"] = dis_type
        dict["start_time"] = start_time
        dict["end_time"] = end_time
        dict["days_of_week"] = days_of_week
        dict["location"] = location
        dict["room"] = room

    return dict


def readable_subject(string):
    for str in unreadable_subjects_title:
        if str in string:
            string = string.replace(str, '.'.join(str))
    return string

#########################  ADVANCED FEATURE  ##################################
def get_lectures(link):
    lec_sections = []
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    sections = json_items["ns2:course"]["sections"]["section"]
    if type(sections) == list:
        for sec in json_items["ns2:course"]["sections"]["section"]:
            url = sec["@href"]
            if is_lecture(url):
                lec_sections.append(sec["#text"])
    return lec_sections

def get_discussions(link, lect):
    dis_sections = []
    filter = lect[0]
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    sections = json_items["ns2:course"]["sections"]["section"]
    if type(sections) == list:
        for sec in json_items["ns2:course"]["sections"]["section"]:
            url = sec["@href"]
            if not is_lecture(url):
                if sec["#text"][0] == filter:
                    dis_sections.append(sec["#text"])
    return dis_sections

def combine_course(link):
    url = link + ".xml"
    jsonString = parse(url)
    json_items = json.loads(jsonString)
    if 'classScheduleInformation' in json_items["ns2:course"].keys():
        return True
    return False

def is_lecture(link):
    jsonString = parse(link)
    json_items = json.loads(jsonString)
    meetings = json_items["ns2:section"]["meetings"]["meeting"]
    if type(meetings) == list:
        for m in meetings:
            if m["type"]["#text"] == "Lecture":
                return True
    else:
        if meetings["type"]["#text"] == "Lecture":
            return True
    return False

def readable_section(sec_list):
    temp = []
    for sec in sec_list:
        if sec in unreadable_section_title:
            temp.append(sec.replace(sec, '.'.join(sec)))
        else:
            temp.append(sec)
    return temp
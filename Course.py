import json
import xmltodict
import urllib
from urllib.request import urlopen
from flask import render_template

#TODO: check value existence/validity
#TODO: Combined section

class Course:
    course_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    unreadable_subjects_title = {"CS", "ECE"}
    #TODO: More
    unreadable_section_title = {'AL1', 'AL2', 'AYA', 'AYB', 'AYC', 'AYD', 'AYE', 'AYF', 'AYG', 'AYH', 'AYI', 'AYJ',
                                'AYK', 'AYL', 'BL1', 'BL2', 'Q3', 'Q4'}

    # checked
    def __init__(self, year="2018", semester="fall"):
        self.year = year
        self.link_to_year = self.course_url + "/" + self.year + ".xml"
        self.semester = semester
        self.link_to_semester = self.course_url + "/" + self.year + "/" + self.semester + ".xml"
        self.combined_course = False
        self.course_description = False
        self.link_to_subject = None
        self.link_to_course_num = None
        self.link_to_crn = None
        self.subject = None
        self.course_num = None
        self.lec_section = None
        self.crn = None
        self.all_sections = None
        self.lec_sections = []
        self.lecture_dict = {}
        self.course_dict = {}

    # checked
    def reset(self):
        self.__init__()

    # checked
    def set_year(self, year):
        self.year = year
        if year is not None:
            self.make_link_to_year()

    # checked
    def make_link_to_year(self):
        self.link_to_year = self.course_url + "/" + self.year + ".xml"

    # checked
    def get_year(self):
        return self.year

    # checked
    def set_semester(self, semester):
        self.semester = semester
        if self.semester is not None:
            self.make_link_to_semester()

    # checked
    def make_link_to_semester(self):
        self.link_to_semester = self.course_url + "/" + self.year + "/" + self.semester + ".xml"

    # checked
    def get_semester(self):
        return self.semester

    # checked
    def set_subject(self, subject):
        self.subject = subject
        if self.subject is not None:
            self.subject = subject.upper()
            self.make_link_to_subject()

    # checked
    def make_link_to_subject(self):
        self.link_to_subject = self.course_url + "/" + self.year + "/" + self.semester + "/" + self.subject + ".xml"

    # checked
    def get_subject(self):
        return self.subject

    # checked
    def set_course_num(self, courseNum):
        self.course_num = courseNum
        if self.course_num is not None:
            self.make_link_to_course_num()

    # checked
    def make_link_to_course_num(self):
        self.link_to_course_num = self.course_url + "/" + self.year + "/" + self.semester + "/" + self.subject + "/" + self.course_num + ".xml"

    # checked
    def get_course_num(self):
        return self.course_num

    # checked
    def set_lec_section(self, lec_section):
        self.lec_section = lec_section
        if self.lec_sections is not None:
            self.make_link_to_crn()
            self.get_lecture_details()

    # checked
    def get_lect_dict(self):
        return self.lecture_dict

    # checked
    def get_lec_sections(self):
        return self.lec_sections

    def get_course_dict(self):
        return self.course_dict

    #TODO: check
    def need_parameter(self):
        if self.subject is None or self.course_num is None:
            return render_template('ask-course')
        elif self.lec_section is None:
            if self.course_description is False:
                self.course_description = True
                return render_template('ask-course-descp')
            else:
                if len(self.lec_sections) == 0:
                    self.set_lecture_sections()
                return render_template('ask-lect-section', combined_course=self.combined_course,
                                       subject=self.subject, course_num=self.course_num,
                                       sections=self.lec_sections)
        else:
            return None

    # checked
    def get_crn(self):
        json_string = self.parse(self.link_to_course_num)
        json_items = json.loads(json_string)
        sections = json_items["ns2:course"]["sections"]["section"]
        self.crn = next(item for item in sections if item['#text'] == self.lec_section)['@id']

    # checked
    def make_link_to_crn(self):
        self.get_crn()
        self.link_to_crn = self.course_url + "/" + self.year + "/" + self.semester + "/" \
                           + self.subject + "/" + self.course_num + "/" + self.crn + ".xml"


    # checked
    def get_all_sections(self):
        json_string = self.parse(self.link_to_course_num)
        json_items = json.loads(json_string)
        self.all_sections = [(lambda x: x["#text"])(x) for x in json_items["ns2:course"]["sections"]["section"]]
        return json_items

    # checked
    def set_lecture_sections(self):
        json_items = self.get_all_sections()
        self.lec_sections = []
        if len(self.all_sections) > 1:
            for sec in json_items["ns2:course"]["sections"]["section"]:
                url = sec["@href"]
                if self.is_lecture(url):
                    self.lec_sections.append(sec["#text"])

    # checked
    def is_lecture(self, link):
        jsonString = self.parse(link)
        json_items = json.loads(jsonString)
        meetings = json_items["ns2:section"]["meetings"]["meeting"]
        if type(meetings) == list:
            for m in meetings:
                if m["type"]["#text"] == "Lecture":
                    return True
        else:
            if "Lecture" in meetings["type"]["#text"]:
                return True
        return False

    # checked
    def parse(self, link):
        try:
            f = urlopen(link)
            xmlString = f.read()
            json_string = json.dumps(xmltodict.parse(xmlString), indent=4)
            return json_string
        except Exception as e:
            print(e)

#########################################################################################
    #TODO: Exception or if-else to solve key problem
    def get_lecture_details(self):
        json_string = self.parse(self.link_to_crn)
        json_items = json.loads(json_string)
        course = json_items["ns2:section"]
        course_title = course["parents"]["course"]["#text"]
        start_date = course["startDate"][0:10]
        end_date = course["endDate"][0:10]
        start_time = course["meetings"]["meeting"]["start"]
        end_time = course["meetings"]["meeting"]["end"]
        days_of_week = course["meetings"]["meeting"]["daysOfTheWeek"]
        days_of_week = self.get_days_of_week(days_of_week)
        professor = course["meetings"]["meeting"]["instructors"]
        professor = self.get_professors(professor)
        location = course["meetings"]["meeting"]["buildingName"]
        self.lecture_dict["course_title"] = course_title
        self.lecture_dict["start_date"] = start_date
        self.lecture_dict["end_date"] = end_date
        self.lecture_dict["start_time"] = start_time
        self.lecture_dict["end_time"] = end_time
        self.lecture_dict["days_of_week"] = days_of_week
        self.lecture_dict["professor"] = professor
        self.lecture_dict["location"] = location
        self.lecture_dict['year'] = self.year
        self.lecture_dict['semester'] = self.semester
        self.lecture_dict['subject'] = self.subject
        self.lecture_dict['course_num'] = self.course_num
        self.lecture_dict['lec_section'] = self.lec_section
        self.lecture_dict['combined_course'] = self.combined_course


    def get_days_of_week(self, days):
        if days == "n.a" or days == None or days == "":
            return ["web or unknown days"]
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
        if len(list_of_days) > 1:
            list_of_days[-1] = "and " + list_of_days[-1]
        return list_of_days

    def get_professors(self, prof):
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

    # checked
    def get_course_detail(self):
        json_string = self.parse(self.link_to_course_num)
        json_items = json.loads(json_string)
        course = json_items["ns2:course"]
        course_title = course["label"]
        description = course["description"]
        description = description[0: description.find("Prerequisite")]
        credit = course["creditHours"]
        courseSectionInformation = self.readable_subject(course["courseSectionInformation"])
        self.course_dict["subject"] = self.subject
        self.course_dict["course_num"] = self.course_num
        self.course_dict["course_title"] = course_title
        self.course_dict["description"] = description
        self.course_dict["credit"] = credit
        self.course_dict["courseSectionInformation"] = courseSectionInformation
        self.course_dict['combined_course'] = self.combined_course

    def readable_subject(self, string):
        for str in self.unreadable_subjects_title:
            if str in string:
                string = string.replace(str, '.'.join(str))
        return string

    # def require_combined_section(self):
    #     jsonString = self.parse(self.link_to_course_num)
    #     json_items = json.loads(jsonString)
    #     if 'classScheduleInformation' in json_items["ns2:course"].keys():
    #         #TODO: May need to be more specific
    #         self.combined_course = True
    #     self.set_lecture_sections()
    #     return self.combined_course


    def readable_section(self, sec_list):
        temp = []
        for sec in sec_list:
            if sec in self.unreadable_section_title:
                if sec == 'ONL':
                    temp.append('Online')
                else:
                    temp.append(sec.replace(sec, '.'.join(sec)))
            else:
                temp.append(sec)
        return temp

    def check_course_num_validity(self):
        print("self.link_to_subject: {}".format(self.link_to_subject))
        jsonString = self.parse(self.link_to_subject)
        json_items = json.loads(jsonString)
        for item in json_items['ns2:subject']['courses']['course']:
            if item['@id'] == self.course_num:
                return None
        return render_template('invalid-course-num', subject=self.subject, course_num=self.course_num)

    def check_subject_validity(self):
        jsonString = self.parse(self.link_to_semester)
        json_items = json.loads(jsonString)
        for item in json_items['ns2:term']['subjects']['subject']:
            if item['@id'].lower() == self.subject.lower():
                return None
        return render_template('invalid-subject')


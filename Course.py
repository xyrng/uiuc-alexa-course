import json
import xmltodict
import urllib
from urllib.request import urlopen
from flask import render_template

#TODO: check value existence/validity

class Course:
    course_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    unreadable_subjects_title = {"CS", "ECE", "AAS"}

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
        self.description = None
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

    def get_course_dict(self):
        return self.course_dict

    def need_parameter(self):
        if self.subject is None or self.course_num is None:
            return render_template('ask-course')
        elif self.year is None:
            return render_template('ask-year')
        elif self.semester is None:
            return render_template('ask-semester', year=self.year)
        else:
            return render_template('ask-course-descp', subject=self.subject, course_num=self.course_num, year=self.year, semester=self.semester)

    # checked
    def parse(self, link):
        try:
            f = urlopen(link)
            xmlString = f.read()
            json_string = json.dumps(xmltodict.parse(xmlString), indent=4)
            return json_string
        except Exception as e:
            print(e)

    # checked
    def get_course_detail(self):
        print("I've been here")
        print("self.link_to_course_num: {}".format(self.link_to_course_num))
        json_string = self.parse(self.link_to_course_num)
        print("json_string: {}".format(json_string is None))
        json_items = json.loads(json_string)
        course = json_items["ns2:course"]
        course_title = course["label"]
        descp = course["description"]
        pre = descp.find("Prerequisite")
        if pre != -1:
            description = descp[0: pre]
            prerequisite = descp[pre: -1]
            prerequisite = self.readable_subject(prerequisite)
        else:
            description = descp
            prerequisite = None
        credit = course["creditHours"]
        self.course_dict["subject"] = self.subject
        self.course_dict["course_num"] = self.course_num
        self.course_dict["course_title"] = course_title
        self.course_dict["description"] = description
        self.course_dict["credit"] = credit
        self.course_dict["prerequisite"] = prerequisite


    def readable_subject(self, string):
        for str in self.unreadable_subjects_title:
            if str in string:
                string = string.replace(str, '.'.join(str))
        return string

    # TODO: Need
    # def require_combined_section(self):
    #     jsonString = self.parse(self.link_to_course_num)
    #     json_items = json.loads(jsonString)
    #     if 'classScheduleInformation' in json_items["ns2:course"].keys():
    #         self.combined_course = True
    #     self.set_lecture_sections()
    #     return self.combined_course

    def check_course_num_validity(self):
        if self.course_num is None:
            return render_template('none-course-num')
        jsonString = self.parse(self.link_to_subject)
        json_items = json.loads(jsonString)
        for item in json_items['ns2:subject']['courses']['course']:
            if item['@id'] == self.course_num:
                return None
        return render_template('invalid-course-num', subject=self.subject, course_num=self.course_num, year=self.year, semester=self.semester)

    def check_subject_validity(self):
        if self.subject is None:
            return render_template('none-subject')
        jsonString = self.parse(self.link_to_semester)
        json_items = json.loads(jsonString)
        for item in json_items['ns2:term']['subjects']['subject']:
            if item['@id'].lower() == self.subject.lower():
                return None
        return render_template('invalid-subject')

    def check_year_validity(self):
        if self.year >= "2004" and self.year <= "2019":
            return None
        else:
            self.year = "2018"
            self.semester = "Fall"
            return render_template('invalid-year')

    def check_semester_validity(self):
        if self.year == "2019" and self.semester != "Spring":
            self.semester = "Spring"
            return render_template('invalid-semester', year="2019", semester=self.semester)
        else:
            return None


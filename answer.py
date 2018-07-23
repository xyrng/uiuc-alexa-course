import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request

from courses import *

# get all sections of corresponding course
# return a list of string
def answer_sections():
    year = session.attributes['year']
    semester = session.attributes['semester']
    subject = session.attributes['subject']
    course_num = session.attributes['course_num']
    link = make_link(year, semester, subject, course_num)
    temp_list = get_sections(link)
    return temp_list

# get all details of lectures
# return a statement / question
def answer_class_details():
    year = session.attributes['year']
    semester = session.attributes['semester']
    subject = session.attributes['subject']
    course_num = session.attributes['course_num']
    section = session.attributes['section']
    link = make_prelink(year, semester, subject, course_num)
    crn = get_crn(link, section)
    link = make_link(link, crn)
    print("111")
    result_dict = get_lecture_detail(link)
    combine_course = session.attributes["combine_course"]
    print("333")
    course_title    =       result_dict['course_title']
    start_date      =       result_dict['start_date']
    end_date        =       result_dict['end_date']
    start_time      =       result_dict['start_time']
    end_time        =       result_dict['end_time']
    days_of_week    =       result_dict['days_of_week']
    professor       =       result_dict['professor']
    location        =       result_dict['location']

    answer_msg = render_template('answer-lec-section-details', section=section, semester=semester, year=year,
                                 course_title=course_title, start_date=start_date,
                                 end_date=end_date, start_time=start_time, end_time=end_time,
                                 days_of_week=days_of_week, professor=professor, location=location, combine_course=combine_course)
    print("444")
    return question(answer_msg)

def answer_dis_details():
    year = session.attributes['year']
    semester = session.attributes['semester']
    subject = session.attributes['subject']
    course_num = session.attributes['course_num']
    labsection = session.attributes['labsection']
    link = make_prelink(year, semester, subject, course_num)
    crn = get_crn(link, labsection)
    link = make_link(link, crn)
    result_dict = get_diss_detail(link)
    one_more_dis = result_dict["one_more_dis"]
    if one_more_dis:
        dis_type = result_dict["dis_type"]
        start_time = result_dict["start_time"]
        end_time = result_dict["end_time"]
        days_of_week = result_dict["days_of_week"]
        location = result_dict["location"]
        room = result_dict["room"]

        dis_type1 = result_dict["dis_type1"]
        start_time1 = result_dict["start_time1"]
        end_time1 = result_dict["end_time1"]
        days_of_week1 = result_dict["days_of_week1"]
        location1 = result_dict["location1"]
        room1 = result_dict["room1"]

        answer_msg = render_template('answer-dis-section-details1', dis_type=dis_type, subject=subject, course_num=course_num,
                                     start_time=start_time, end_time=end_time, days_of_week=days_of_week, location=location, room=room,
                                     dis_type1=dis_type1, start_time1=start_time1, end_time1=end_time1, days_of_week1=days_of_week1,
                                     location1=location1, room1=room1)
    else:
        dis_type = result_dict["dis_type"]
        start_time = result_dict["start_time"]
        end_time = result_dict["end_time"]
        days_of_week = result_dict["days_of_week"]
        location = result_dict["location"]
        room = result_dict["room"]

        answer_msg = render_template('answer-dis-section-details', dis_type=dis_type, subject=subject, course_num=course_num,
                                     start_time=start_time, end_time=end_time, days_of_week=days_of_week, location=location, room=room)
    return question(answer_msg)


def answer_course_details():
    year = session.attributes['year']
    semester = session.attributes['semester']
    subject = session.attributes['subject']
    course_num = session.attributes['course_num']

    link = make_prelink(year, semester, subject, course_num)
    result_dict = get_course_detail(link)

    course_title = result_dict['course_title']
    description = result_dict['description']
    credit = result_dict['credit']
    courseSectionInformation = result_dict['courseSectionInformation']
    genEdCategories = result_dict['genEdCategories']


    #TODO: answer-course-details template
    answer_msg = render_template('answer-course-details', subject=subject, course_num=course_num,
                                 course_title=course_title, description=description, credit=credit,
                                 courseSectionInformation=courseSectionInformation, genEdCategories=genEdCategories)
    return question(answer_msg)
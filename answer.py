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
    result_dict = get_lecture_detail(link)

    course_title    =       result_dict['course_title']
    start_date      =       result_dict['start_date']
    end_date        =       result_dict['end_date']
    start_time      =       result_dict['start_time']
    end_time        =       result_dict['end_time']
    days_of_week    =       result_dict['days_of_week']
    professor       =       result_dict['professor']
    location        =       result_dict['location']

    session.attributes = {}

    answer_msg = render_template('answer-lec-section-details',
                                 course_title=course_title, start_date=start_date,
                                 end_date=end_date, start_time=start_time, end_time=end_time,
                                 days_of_week=days_of_week, professor=professor, location=location, crn=crn)
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
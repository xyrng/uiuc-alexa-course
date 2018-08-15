import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request


# get all details of lectures
# return a statement / question
#TODO: unfinished
def answer_lec_details(lect_dict):

    year            =       lect_dict['year']
    semester        =       lect_dict['semester']
    subject         =       lect_dict['subject']
    course_num      =       lect_dict['course_num']
    section         =       lect_dict['lec_section']
    course_title    =       lect_dict['course_title']
    start_date      =       lect_dict['start_date']
    end_date        =       lect_dict['end_date']
    start_time      =       lect_dict['start_time']
    end_time        =       lect_dict['end_time']
    days_of_week    =       lect_dict['days_of_week']
    professor       =       lect_dict['professor']
    location        =       lect_dict['location']

    answer_msg = render_template('answer-lec-section-details', section=section, subject=subject, course_num=course_num, semester=semester, year=year,
                                 course_title=course_title, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time,
                                 days_of_week=days_of_week, professor=professor, location=location)
    return question(answer_msg)

# checked
def answer_course_details(course_dict):
    subject = course_dict['subject']
    course_num = course_dict['course_num']
    course_title = course_dict['course_title']
    description = course_dict['description']
    credit = course_dict['credit']
    courseSectionInformation = course_dict['courseSectionInformation']

    answer_msg = render_template('answer-course-details', subject=subject, course_num=course_num,
                                 course_title=course_title, description=description, credit=credit,
                                 courseSectionInformation=courseSectionInformation)
    return question(answer_msg)
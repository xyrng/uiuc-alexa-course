import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request

# checked
def answer_detailed_course_descrp(course_dict):
    subject = course_dict['subject']
    course_num = course_dict['course_num']
    course_title = course_dict['course_title']
    description = course_dict['description']
    credit = course_dict['credit']
    print("prerequisite problem")
    prerequisite = course_dict['prerequisite']

    print("prerequisite: {}".format(prerequisite))

    answer_msg = render_template('answer-course-detailed-descp', subject=subject, course_num=course_num,
                                 course_title=course_title, description=description, credit=credit, prerequisite=prerequisite)
    return question(answer_msg)


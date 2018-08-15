import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request


from answer import *
from Course import Course

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


course = Course()


def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)


@ask.launch
def welcome():
    # init
    welcome_msg = render_template('welcome') #TODO: welcome template
    return question(welcome_msg)


@ask.intent("AMAZON.HelpIntent")
def help():
    help_msg = render_template('help')  #TODO: help template
    return question(help_msg)


@ask.intent("AMAZON.FallbackIntent")
def fallback():
    fallback_msg = render_template('error-not-understand') #TODO: fallback template
    return question(fallback_msg)


@ask.intent('AMAZON.CancelIntent')
@ask.intent("AMAZON.StopIntent")
def stop():
    goodbye_msg = render_template('goodbye') #TODO: goodbye template
    return statement(goodbye_msg)

#########################SELF MADE FUNCTION##############################

# User says year (2018), and then will be redirected to AnswerSemesterIntent
@ask.intent('AnswerYearIntent', mapping={'year': 'year'})
def answer_year(year):
    try:
        # get year from request
        year = request.intent.slots.year.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['id']
        # store year as course attribute
        course.set_year(year)
        # ask other not answered specs
        ask_msg = course.need_parameter()
        if ask_msg is None:
            return answer_lec_details(course.lecture_dict)
        else:
            return question(ask_msg)
    except KeyError:
        err_msg = render_template("error-not-understand")
        return question(err_msg)

# User says semester (fall), and then will be redirected to AnswerCourseNameIntent or AnswerSubjectIntent
@ask.intent('AnswerSemesterIntent', mapping={'semester': 'semester'})
def answer_semester(semester):
    try:
        # get semester from request
        semester = request.intent.slots.semester.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['id']
        # store semester as course attribute
        course.set_semester(semester)
        # ask other not answered specs
        ask_msg = course.need_parameter()
        if ask_msg is None:
            return answer_lec_details(course.lecture_dict)
        else:
            return question(ask_msg)
    except KeyError:
        ask_msg = render_template('error-not-understand')
        return question(ask_msg)


# User says course name (CS 225), and then will be redirected to AnswerSectionIntent
@ask.intent("AnswerCourseNameIntent", mapping={"subject": "subject", "courseNum": "course_num"})
def answer_course_name(subject, course_num):
    try:
        # get subject and course_num from request
        subject = request.intent.slots.subject['value']
        course_num = request.intent.slots.courseNum['value']
        # store as course attributes
        course.set_subject(subject)
        course.set_course_num(course_num)
        print(1)
        print(course.get_subject())
        print(course.get_course_num())
        ask_msg = course.check_subject_validity()
        if ask_msg is not None:
            course.set_subject(None)
            course.set_course_num(None)
            return question(ask_msg)
        ask_msg = course.check_course_num_validity()
        print(2)
        print(course.get_subject())
        print(course.get_course_num())
        if ask_msg is not None:
            course.set_subject(None)
            course.set_course_num(None)
            return question(ask_msg)
        # ask other not answered specs
        ask_msg = course.need_parameter()
        if ask_msg is None:
            return answer_lec_details(course.lecture_dict)
        else:
            return question(ask_msg)
    except KeyError:
        err_msg = render_template("error-not-understand")
        return question(err_msg)


@ask.intent("AnswerCourseDescriptionIntent")
def answer_course_des():
    try:
        course.get_course_detail()
        return answer_course_details(course.get_course_dict())
    except KeyError:
        err_msg = render_template("error-not-understand")
        return question(err_msg)

@ask.intent("IntermediateIntent")
def ask_section():
    course.set_lecture_sections()
    #TODO: section template
    ask_msg = render_template('ask-lect-section', subject=course.get_subject(),
                              course_num=course.get_course_num(), sections=course.get_lec_sections())
    return question(ask_msg)


# What user says will be section number and I have to find corresponding crn
@ask.intent("AnswerSectionIntent", mapping={"section": "section"})
def answer_section():
    try:
        # get course_num from request
        section = request.intent.slots.section.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
        # store year into session
        course.set_lec_section(section)
        ask_msg = course.need_parameter()
        print("AnswerSectionIntent here")
        if ask_msg is not None:
            print("ask_msg")
            return question(ask_msg)
        print("pass")
        print("set_lec_section")
        return answer_lec_details(course.get_lect_dict())
    except KeyError:
        err_msg = render_template("error-other")

        return question(err_msg)

@ask.intent("RestartIntent")
def restart():
    try:
        # clean the session attributions
        course.reset()
        answer_msg = render_template("restart")
        return question(answer_msg)
    except KeyError:
        err_msg = render_template("ask-restart")
        return question(err_msg)


if __name__ == '__main__':
    app.run(debug=True)
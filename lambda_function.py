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

@ask.intent('AnswerYearIntent', mapping={'year': 'year'})
def answer_year(year):
    try:
        # get year from request
        year = request.intent.slots.year['value']
        # store year as course attribute
        course.set_year(year)
        #TODO: check year validity
        ask_msg = course.check_year_validity()
        if ask_msg is not None:
            return question(ask_msg)
        # ask other not answered specs
        ask_msg = render_template('ask-semester', year=course.get_year())
        return question(ask_msg)
    except KeyError:
        err_msg = render_template("error-not-understand")
        return question(err_msg)

# User says semester (fall), and then will be redirected to AnswerCourseNameIntent or AnswerSubjectIntent
@ask.intent('AnswerSemesterIntent', mapping={'semester': 'semester'})
def answer_semester(semester):
    try:
        # get semester from request
        semester = request.intent.slots.semester.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
        print("lambda semester: {}".format(semester))
        # store semester as course attribute
        course.set_semester(semester)
        # TODO: check semester validity
        ask_msg = course.check_semester_validity()
        if ask_msg is not None:
            return question(ask_msg)
        # ask other not answered specs
        ask_msg = render_template('ask-course', year=course.get_year(), semester=course.get_semester())
        return question(ask_msg)
    except KeyError:
        ask_msg = render_template('error-not-understand')
        return question(ask_msg)


# User says course name (CS 225)
@ask.intent("AnswerCourseNameIntent", mapping={"subject": "subject", "courseNum": "course_num"})
def answer_course_name(subject, course_num):
    try:
        # get subject and course_num from request
        subject = request.intent.slots.subject.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
        course_num = request.intent.slots.courseNum['value']
        # store as course attributes
        course.set_subject(subject)
        course.set_course_num(course_num)
        ask_msg = course.check_subject_validity()
        if ask_msg is not None:
            course.set_subject(None)
            course.set_course_num(None)
            return question(ask_msg)
        ask_msg = course.check_course_num_validity()
        if ask_msg is not None:
            course.set_subject(None)
            course.set_course_num(None)
            return question(ask_msg)
        # ask other not answered specs
        ask_msg = course.need_parameter()
        return question(ask_msg)
    except KeyError:
        err_msg = render_template("error-not-understand")
        return question(err_msg)


@ask.intent("AnswerDescriptionIntent")
def answer_course_des():
    try:
        ask_msg = course.check_course_num_validity()
        if ask_msg is not None:
            course.set_subject(None)
            course.set_course_num(None)
            return question(ask_msg)
        course.get_course_detail()
        return answer_detailed_course_descrp(course.get_course_dict())
    except KeyError:
        err_msg = render_template("error-not-understand")
        return question(err_msg)


@ask.intent("RestartIntent")
def restart():
    try:
        # clean the attributions
        course.reset()
        answer_msg = render_template("restart")
        return question(answer_msg)
    except KeyError:
        err_msg = render_template("hello")
        return question(err_msg)


if __name__ == '__main__':
    app.run(debug=True)
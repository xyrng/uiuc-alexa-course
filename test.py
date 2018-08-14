import json
from parse import parse
import xmltodict
from urllib.request import urlopen
from Course import Course

course = Course()
course.set_subject("CS")
course.set_course_num("411")
course.get_course_detail()
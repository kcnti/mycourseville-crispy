import requests
import os
from bs4 import BeautifulSoup
from utils.mycourseville import *
from dotenv import load_dotenv

load_dotenv()

userid = os.environ.get('ID')
password = os.environ.get('PASSWD')

mcv = MCV(userid, password)
session = mcv.login()

assignments = mcv.getAssignments()
print(assignments)

# courses = mcv.getCourses()
# print(courses)

# fileLinks = mcv.getFileLink()
# print(fileLinks)

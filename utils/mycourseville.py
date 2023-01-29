from cgitb import html
import requests
import re
from bs4 import BeautifulSoup

class MCV:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None

    def login(self):
        oauthURL = 'https://www.mycourseville.com/api/oauth/authorize?response_type=code&client_id=mycourseville.com&redirect_uri=https://www.mycourseville.com&login_page=itchula'
        s = requests.Session()
        s.get(oauthURL)

        chulaLogin = 'https://www.mycourseville.com/api/chulalogin'
        r = s.get(chulaLogin)
        html_doc = r.text
        token = re.findall('<input type="hidden" name="_token" value="(.+?)">', html_doc)[0]

        data = {
            '_token': token,
            'username': self.username,
            'password': self.password,
            'remember': 'on'
        }

        req = s.post(chulaLogin, data=data) # login session
        if req.status_code == 200:
            self.session = s
            return 1

        return 0

    def getAssignments(self):
        URL = 'https://www.mycourseville.com/?q=courseville/ajax/getactivepanelcontent'
        r = self.session.post(URL)
        resp = r.json()
        html_doc = resp['html']
        homeworks = re.findall('<strong>&ldquo;(.+?)&rdquo;</strong>(.+?)<strong>(.+?)</strong>', html_doc)

        output = [''.join(x) for x in homeworks]
        return ('\n'.join(output))


    def getChildID(self):
        mcv = 'https://www.mycourseville.com/?q=courseville'
        r = self.session.get(mcv)

        childID = re.findall('class="cv-fa-collapse-control"[^.]*child_id="(.+?)"', r.text)[0]
        return childID

    def getCourses(self):
        URL = 'https://www.mycourseville.com/?q=courseville/ajax/cvhomepanel_get'

        childID = self.getChildID()


        data = {
            'content': childID
        }
        r = self.session.post(URL, data=data)
        resp = r.json()
        html_doc = ' '.join(resp['html'].split())
        courses = re.findall('<a href="(.+?)" aria-label="(.+?)"', html_doc)
        coursesName = list(map(lambda x: x[1], courses))

        return '\n'.join(coursesName)

    def getFileLink(self):
        URL = 'https://www.mycourseville.com/?q=courseville/ajax/cvhomepanel_get'

        childID = self.getChildID()

        data = {
            'content': childID
        }
        r = self.session.post(URL, data=data)
        resp = r.json()
        html_doc = ' '.join(resp['html'].split())
        courses = re.findall('<a href="(.+?)"', html_doc)
        print(courses)
        # not done
        return

if __name__ == '__main__':

    pass

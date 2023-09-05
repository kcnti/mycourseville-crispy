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
        # print(html_doc)
        courseLinks = [i.split('/')[2] for i in re.findall('<a target="_blank" href="(.+?)">', html_doc)]
        homeworks = re.findall(r'<strong>&ldquo;(.+?)&rdquo;</strong>(.+?)<strong>(.+?)</strong>', html_doc)
        
        courseInfo = self.getCourses()['courseInfo']
        print(courseInfo)
        output = [''.join(homeworks[x]) + ' (' + courseInfo[courseLinks[x]] + ')' for x in range(len(homeworks))]
        return ('\n'.join(output))


    def getChildID(self):
        mcv = 'https://www.mycourseville.com/?q=courseville'
        r = self.session.get(mcv)

        childID = re.findall('class="cv-fa-collapse-control"[^.]*child_id="(.+?)"', r.text)[0]
        # print(re.findall('class="cv-fa-collapse-control"[^.]*child_id="(.+?)"', r.text))
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
        courses = re.findall('<a href="(.+?)" aria-label="(.+?)".cv_cid="(.+?)"', html_doc)
        coursesName = list(map(lambda x: x[1], courses))
        courseInfo = {}
        for i in courses:
            courseInfo[i[2]] = i[1].split('"')[0]

        return {'courseText': '\n'.join(coursesName), 'courseInfo': courseInfo}

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

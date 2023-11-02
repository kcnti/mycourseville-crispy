import os
from utils.mycourseville import *
from dotenv import load_dotenv

load_dotenv()

userid = os.environ.get('ID')
password = os.environ.get('PASSWD')

mcv = MCV(userid, password)
session = mcv.login()

# assignments = mcv.getAssignments()

# courses = mcv.getCourses()

fileLinks = mcv.getFileLink()
# print(fileLinks)

# Downloading Files
def download(fileLinks, parentFolder):
    if (not os.path.isdir(parentFolder)):
        os.makedirs(parentFolder)

    for subject in fileLinks:
        print(subject.upper())
        subFolder = parentFolder + '/' + subject
        if (not os.path.isdir(subFolder)):
            os.makedirs(subFolder)

        for materialFolder in fileLinks[subject]:
            matFolder = subFolder + '/' + materialFolder

            for data in fileLinks[subject][materialFolder]:
                extension = '.' + data['fileUrl'].split('.')[-1]
                if (not os.path.isdir(matFolder)):
                    os.makedirs(matFolder)
                save = matFolder + '/' + data['fileName'] + extension
                if (os.path.exists(save)):
                    print(data['fileName'], 'exists')
                    continue
                dl = requests.get(data['fileUrl'], allow_redirects=True)
                open(save, 'wb').write(dl.content)
                print(data['fileName'], 'saved')

# download(fileLinks, 'courseMaterials')



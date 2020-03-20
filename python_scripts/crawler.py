import os
import re
import json
import hashlib
import requests
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

base_url = "https://www.uc3m.es/"
masters_url = os.path.join(base_url,"postgraduate/school-of-engineering")
unique_url = os.path.join(base_url,"{u}")


def soupify(resource, txt=False):
    # Handler for return soup object given url or html code
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {"User-Agent":user_agent}
    if not txt:
        response = requests.get(resource, headers=headers)
        content = response.text
    else: 
        content = resource  
    soup = BeautifulSoup(content, "html.parser")
    return soup
            

def get_masters_ref():
    # Get minimum masters charateristics and return the results
    masters = []
    soup = soupify(masters_url)
    results = soup.select(".row.marcoLiso.texto")

    # Only select Research Masters for now
    masters_kind_li = ["", "regulated", "academic/professional", "research", "double"]
    kind = "research"
    research = results[masters_kind_li.index(kind)]
    
    li = research.findChildren("li" , recursive=True)
    for element in li:
        has_grant = "Grant" in element.getText()
        a = element.findChildren("a")
        a = a[0]
        link = a.get("href").lstrip("/")
        url = unique_url.format(u=link)
        # name = a.getText()
        # name = name.replace(" ","_")
        masters.append({"url":url, "grant":has_grant, "type":kind})
    return masters

def extract_masters_info(masters):
    # Extract characteristics for every master and store in json file
    lang = "dd.idiomas"
    mod = "dd.modalidad"
    credits = "dd.creditos"
    location = "dd.campus"
    p = "dd.plazoadmision p strong"
    n = ".contTitulo.row h1"

    new_masters_list = []
    for master in masters:
        link = master["url"]
        soup = soupify(link)

        language = soup.select(lang)[0].getText()
        modality = soup.select(mod)[0].getText()
        creds = soup.select(credits)[0].getText().split()[0]
        loc = soup.select(location)[0].getText().strip()
        places = soup.select(p)[1].getText().split(": ")[1]
        name = soup.select(n)[0].getText()
        id = get_hash(name)
        
        if int(creds) >= 60:
            courses = "1"
        else: 
            courses = "1.5"

        eu_studs = soup.find(string=re.compile("EU students:"))
        neu_studs = soup.find(string=re.compile("Non EU students:"))
        pat = re.compile(r"€(\d,\d+(\.\d+)?)\s")
        eu = pat.search(eu_studs).group(1)
        neu = pat.search(neu_studs).group(1)

        master.update({"id":id, "name": name,"lang":language, "modality":modality, "creds":creds, 
        "location":loc, "places":places, "courses":courses, "price":{"eu":eu, "neu":neu}})
        new_masters_list.append(master)

    return new_masters_list

def get_hash(string):
    # Convert master name in hash for unique id
    bytes_conver = bytes(string, "utf-8")
    h = hashlib.sha1(bytes_conver)
    return h.hexdigest()


def get_subjects(masters):
    # For every master link, go and extract the subjects basic info
    subjects_list = []
    for master in masters:
        url = master["url"] + "#curriculum"
        soup = soupify(url) 

        # Gather the curriculum section of the master page
        li = soup.find_all(id=re.compile("curriculum_curriculum"))[0].prettify()
        soup = soupify(li, txt=True)

        subject_attr = 'td[data-label="Subject"] a'
        creds_attr = 'td[data-label="ECTS"]'
        type_attr = 'td[data-label="TYPE"]'
        lang_attr = ".listaIdiomas img"

        subjects = soup.select(subject_attr)
        creds = soup.select(creds_attr)
        Type = soup.select(type_attr)
        language = soup.select(lang_attr)

        for subject, cred, t, lang in zip(subjects,creds,Type,language):
            # Extract subjects basic info
            subject_name = subject.getText().strip()
            subject_name = re.subn("\s+", " ", subject_name)[0]
            subject_link = subject["href"]
            credits = cred.getText().strip()
            type = t.getText().strip()
            lang = lang["alt"]

            # This is given that there is garbage in subjects tables in some masters
            if not (credits and type and lang):
                continue
            
            # Store subjects
            subjects_list.append({"name":subject_name, "url":subject_link,
            "credits":credits, "type":type, "language":lang, "master":master["id"]})

    return subjects_list
         


def extract_subject_info(subjects):
    # Extract in depth information of subjects
    subjects_list = []

    for subject in subjects:
        soup = soupify(subject["url"])
        
        # Collect course, semester, id, and schedule link
        s = soup.select("div.col.izquierda")
        _, _, course, semester = s
        course = course.getText()
        semester = semester.getText()
        semester = re.search("\d", semester)
        course = re.search("\d", course)
        if semester != None:
            semester = semester.group()
        if course != None:
            course = course.group()
            
        id = soup.find("div", {"class":"asignatura"}, string=re.compile("(\d{5})"))
        id = re.subn(r"[()]", "", id.getText())[0]

        try:
            # If subject has no schedule in the course skip it
            schedule_link = soup.find("a", href=re.compile("https://aplicaciones.uc3m.es/consultaHorarios/porAsignatura.htm?"))["href"]
        except TypeError:
            continue

        # Get schedule
        schedule = get_schedule(schedule_link)

        # Save the results
        subject.update({"course":course, "semester":semester, "id":id, "schedule":schedule})
        subjects_list.append(subject)

    return subjects_list
    
def get_schedule(link):
    # Conform schedule
    schedule = []

    soup = soupify(link)
    schedule_table = "table.horario tr"

    # Select every entry in the schedule table
    table_items = soup.select(schedule_table)
    for tr in table_items:
        children = tr.findChildren("td")

        day = children[0].getText().split(",")
        day = conevert_to_date(day)
        start_hour = children[1].getText().split("-")[0]
        weeks_unformat = children[2].getText().split(": ")[1].split(",")
        room = children[3].getText().split(":")[1].strip()

        # Process weeks "<td>Weeks: 4-11, 16-17, 20</td>"
        weeks = []
        for value in weeks_unformat:
            interval = value.split("-")
            if len(interval) > 1:
                lower = interval[0]
                upper = interval[1]
                r = list(range(int(lower), int(upper)+1))
                weeks.extend(r)
            else:
                weeks.append(int(value))
        schedule.append({"weeks":weeks, "day":day, "time": start_hour, "room":room})
    return schedule

def conevert_to_date(date_list):
    date_dict = {"Mon":1, "Tue":2, "Wed":3, "Thu":4, "Fri":5, "Sat":6, "Sun":7}
    days = []
    for date in date_list:
        d = date.strip()
        days.append(date_dict[d])
    return days


## Store masters in json file
# m = get_masters_ref()
# masters = extract_masters_info(m)
# with open("masters.json","w") as master_js:
#     json.dump(masters, master_js)

## Load masters info to get subjects
# with open("masters.json","r") as master_js:
#     masters = json.load(master_js)

## Extract subjects info
# subjects = get_subjects(masters)
# with open("subjects.json","w") as subject_js:
#     json.dump(subjects, subject_js)

## Load subjects
with open("subjects.json","r") as subject_js:
    subjects = json.load(subject_js)

subjects_info = extract_subject_info(subjects)

with open("subjects_full.json","w") as subject_js:
    json.dump(subjects_info, subject_js)

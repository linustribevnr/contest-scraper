import textwrap
import requests as req
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw
from dateutil import parser
from datetime import datetime, timedelta
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class ImageGenerator:
    fontDirectory = "src/resources/fonts/RobotoBlack.ttf"
    storyTemplateDirectory = "src/resources/templates/storyTemplate.jpg"

    def generateImage(self, contest):
        MAX_W = 1080
        font = ImageFont.truetype(self.fontDirectory, 50)
        image = Image.open(self.storyTemplateDirectory)
        draw = ImageDraw.Draw(image)
        w, h = font.getsize("Platform : " + contest.platform)
        draw.text((((MAX_W - w) / 2), 900), "Platform : " +
                  contest.platform, fill="white", font=font, align="center")
        w, h = font.getsize("Contest code : " + contest.contestCode)
        draw.text((((MAX_W - w) / 2), 1000), "Contest code : " +
                  contest.contestCode, fill="white", font=font, align="center")
        font = ImageFont.truetype(self.fontDirectory, 70)
        lines = textwrap.wrap(contest.contestName, width=25)
        y_text = 1150
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((MAX_W - width) / 2, y_text),
                      line, font=font, fill="white")
            y_text += height
        font = ImageFont.truetype(self.fontDirectory, 50)
        draw.text((150, y_text+100), "START : ",
                  fill="white", font=font, align="left")
        timeDifference = contest.endDateTime - contest.startDateTime
        contest.startDateTime = str(
            contest.startDateTime.strftime('%d-%m-%Y %H:%M:%S'))
        contest.endDateTime = str(
            contest.endDateTime.strftime('%d-%m-%Y %H:%M:%S'))
        draw.text((400, y_text+100), contest.startDateTime,
                  fill="white", font=font, align="left")
        draw.text((150, y_text+200), "END : ", fill="white",
                  font=font, align="right")
        draw.text((400, y_text+200), contest.endDateTime,
                  fill="white", font=font, align="right")
        timeDifference = str(timeDifference)
        duration = ""
        durationList = timeDifference
        if "days" in timeDifference:
            daysList = timeDifference.split(" days, ")
            duration = daysList[0] + " days "
        if "days" in timeDifference:
            durationList = timeDifference.split(" days, ")
            durationList = durationList[1]
        durationList = durationList.split(":")
        print(durationList)
        if durationList[0] != "0" and durationList[0] != "00":
            print('ehyy')
            duration += str(durationList[0]) + " Hours "
        if durationList[1] != "00" and durationList[0] != "00":
            duration += str(durationList[1]) + " Minutes "
        w, h = font.getsize("DURATION : " + duration)
        draw.text((((MAX_W - w) / 2), y_text+300), "DURATION : " +
                  str(duration), fill="white", font=font, align="right")
        return image


class ContestsRetreiver:
    def getTodaysContestDetails(self):
        # 2020-05-11 15:00:00
        contestsJson = []
        codechefContests = self.getContestsfromCodechef()
        for contest in codechefContests:
            if ((datetime.now() + timedelta(hours=5.5)).date() == parser.parse(contest['start_time']).date()):
                contestsJson.append(contest)
        codeforcesContests = self.getContestsfromCodeforcesApi()
        for contest in codeforcesContests:
            if((datetime.now() + timedelta(hours=5.5)).date() == parser.parse(contest['start_time']).date()):
                contestsJson.append(contest)

        return contestsJson

    def getAllUpcomingContestDetails(self):
        contestsJson = []
        codechefContests = self.getContestsfromCodechef()
        for contest in codechefContests:
            contestsJson.append(contest)
        codeforcesContests = self.getContestsfromCodeforcesApi()
        for contest in codeforcesContests:
            contestsJson.append(contest)

        return contestsJson

    def getContestsfromCodechef(self):
        try:
            URL = "https://www.codechef.com/contests"
            chrome_options = Options()
            # Opens the browser up in background, this was done since codechef API loads the data in tables after sometime.
            # in future CodeChef official API should be used.
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            with Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options) as browser:
                browser.get(URL)
                html = browser.page_source
            soup = bs(html, 'lxml')
            allTables = soup.find_all('table', attrs={'class': 'dataTable'})
            presentTables = allTables[1]  # Present table is the second one
            contests = []
            allRows = presentTables.find_all('tr')
            for row in allRows:
                contest = {}
                strippedData = []
                datas = row.find_all('td')
                for data in datas:
                    strippedData.append(data.text.strip())
                if(len(strippedData) == 5):
                    contest['code'] = strippedData[0]
                    contest['name'] = strippedData[1]
                    startTime = datetime.strptime(
                        strippedData[2], '%d %b %Y  %a %H:%M')
                    contest['start_time'] = startTime.strftime(
                        "%b/%d/%Y %H:%M")
                    durationHrs = int(strippedData[3].split()[0])
                    if 'Long' in contest['name']:
                        durationHrs *= 24
                    contest['duration'] = str(timedelta(
                        hours=durationHrs, minutes=0, seconds=0))
                    contest['end_time'] = (
                        startTime + timedelta(hours=durationHrs)).strftime("%b/%d/%Y %H:%M")
                    contest['platform'] = "codechef"
                    contest['id'] = "codechef_" + strippedData[0]
                    contests.append(contest)
            return contests
        except Exception as e:
            print('Error retrieving codechef details: ', str(e))
            return []

    def getContestsfromCodeforces(self):
        try:
            URL = "http://codeforces.com/contests"
            soup = bs(req.get(URL).content, 'lxml')
            allTables = soup.find_all('div', attrs={'class': 'datatable'})
            presentTables = allTables[0]  # Present table is the first one
            contests = []
            allRows = presentTables.find_all('tr')
            for row in allRows:
                contest = {}
                strippedData = []
                datas = row.find_all('td')
                for data in datas:
                    strippedData.append(data.text.strip())
                if(len(strippedData) == 6):
                    startTime = datetime.strptime(
                        strippedData[2], "%b/%d/%Y %H:%M")
                    startTime = startTime + timedelta(hours=2, minutes=30)
                    contest['name'] = strippedData[0]
                    contest['code'] = strippedData[0].split()[2]
                    contest['start_time'] = str(startTime)
                    if(len(strippedData[3]) != 5):
                        strippedData[3] = strippedData[3].split(':', 1)[1]
                    tempDate = datetime.strptime(strippedData[3], "%H:%M")
                    contest['duration'] = str(timedelta(
                        hours=tempDate.hour, minutes=tempDate.minute, seconds=tempDate.second))
                    contest['end_time'] = str(startTime + timedelta(
                        hours=tempDate.hour+8, minutes=tempDate.minute, seconds=tempDate.second))
                    contest['platform'] = "codeforces"
                    contest['id'] = strippedData[0] + \
                        strippedData[2].split()[0]
                    contests.append(contest)
            return contests
        except:
            print('Error retrieving codeforces details')
            return []

    def getContestsfromCodeforcesApi(self):
        try:
            URL = "https://codeforces.com/api/contest.list"
            response = req.get(URL).json()
            contests = []
            for each in response["result"]:
                if each["phase"] == "FINISHED":
                    break
                contest = {}
                contest['name'] = each["name"]
                contest['code'] = str(each["id"])
                each["startTimeSeconds"] += 19800
                contest['start_time'] = (datetime.fromtimestamp(
                    each["startTimeSeconds"])).strftime("%b/%d/%Y %H:%M")
                dur = str(timedelta(
                    seconds=each["durationSeconds"]))
                if len(dur) > 9:  # yx days,xx:xx:xx
                    dur = dur[:-9]
                    contest['duration'] = dur
                else:
                    contest['duration'] = dur[:-3]
                contest['end_time'] = (datetime.fromtimestamp(
                    each["startTimeSeconds"] + each["durationSeconds"])).strftime("%b/%d/%Y %H:%M")
                contest['platform'] = "codeforces"
                contest['id'] = 'codeforces_' + str(each["id"])
                contests.append(contest)
            return contests
        except:
            print('Error retrieving codeforces details')
            return []


# print(ContestsRetreiver().getTodaysContestDetails())
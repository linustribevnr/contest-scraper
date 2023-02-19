import io
import textwrap
import requests as req
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw
from dateutil import parser
from datetime import datetime, timedelta


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
        codechefContests = self.getContestsfromCodechefApi()
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
        codechefContests = self.getContestsfromCodechefApi()
        for contest in codechefContests:
            contestsJson.append(contest)
        codeforcesContests = self.getContestsfromCodeforcesApi()
        for contest in codeforcesContests:
            contestsJson.append(contest)

        return contestsJson

    def getContestsfromCodechefApi(self):
        try:
            URL = "https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=premium"
            response = req.get(URL).json()
            response_contests = response["present_contests"] + response["future_contests"]
            contests = []
            for each in response_contests:
                contest = {}
                contest['name'] = each["contest_name"]
                contest['code'] = each["contest_code"]
                if contest['code'] == 'GAMES':
                    continue
                contest['start_time'] = datetime.fromisoformat(each["contest_start_date_iso"]).strftime("%b/%d/%Y %H:%M") 
                contest['end_time'] = datetime.fromisoformat(each["contest_end_date_iso"]).strftime("%b/%d/%Y %H:%M")
                dur = str(timedelta(minutes=int(each['contest_duration'])))
                if len(dur) > 9:  # yx days,xx:xx:xx
                    dur = dur[:-9]
                    contest['duration'] = dur
                else:
                    contest['duration'] = dur[:-3]
                contest['platform'] = "codechef"
                contest['id'] = 'codechef_' + str(each["contest_code"])
                contests.append(contest)
            return contests
        except Exception as e:
            print('Error retrieving codechef details', str(e))
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
        except Exception as e:
            print('Error retrieving codeforces details', e)
            return []

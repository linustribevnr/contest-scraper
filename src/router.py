from .services import ImageGenerator, ContestsRetreiver
from flask import(Blueprint, request)
import io
from flask import send_file
import json
from .models import Contest


bluePrint = Blueprint('router', __name__)


@bluePrint.route('/')
def index():
    response = {"data": "Index Route"}
    return response


@bluePrint.route('/download', methods=['GET', 'POST'])
def generateImage():
    imageGenerator = ImageGenerator()
    if request.method == 'POST':
        contestJson = request.json
        if(contestJson != None):
            contest = Contest.fromJson(contestJson)
            generatedImage = imageGenerator.generateImage(contest)
            imageIO = io.BytesIO()
            generatedImage.save(imageIO, 'JPEG', quality=100)
            imageIO.seek(0)
            return send_file(imageIO, mimetype='image/jpeg')
        else:
            return "No Contest Provided"
    else:
        # get contest from db using param id and send image
        return "not yet implemented"


@bluePrint.route('/allcontests')
def allcontests():
    retriver = ContestsRetreiver()
    return json.dumps(retriver.getAllUpcomingContestDetails())


@bluePrint.route('/contests')
def contests():
    retriver = ContestsRetreiver()
    return json.dumps(retriver.getTodaysContestDetails())

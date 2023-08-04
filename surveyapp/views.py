from .db import db_name
from .serializers import SurveySerializer

from rest_framework import viewsets

from rest_framework.response import Response
import datetime, pytz


class SurveyViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        print("POST Called")

        database = db_name()
        keys_collection = database['survey-keys']
        data_collection = database['survey_data']

        data = request.data
        if 'uuid' in data:
            uuid = data['uuid']
            document = keys_collection.find_one({'uuid': uuid})
            if document:
                if document.get('used', True):
                    # Document has already been used
                    return Response(data={'Error': 'Key has already been used'}, status=400)
                else:
                    print("All okay")
                    data['created_time'] = datetime.datetime.now(tz=pytz.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    result = data_collection.insert_one(data)
                    response_data = {"message":"Submitted Successfully" ,'id': str(result.inserted_id)}
                    keys_collection.update_one({'uuid': uuid}, {"$set": {"used": True}})
                    return Response(data=response_data, status=201)
            else:
                # Document not found
                return Response(data={'Error': 'Key Not Found'}, status=400)
        else: 
            return Response(data={"Error":"UUID Not provided"}, status=400)
        
    def get(self, request):

        database = db_name()
        # keys_collection = database['survey-keys']
        data_collection = database['survey_data']
        print("GET called")
        surveys = data_collection.find()
        if surveys.count() > 0:
            serializer = SurveySerializer(surveys, many=True)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data={"Error":"No Surveys found yet"}, status=404)


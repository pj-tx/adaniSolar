from .db import db_name

from rest_framework import viewsets

from rest_framework.response import Response
import datetime, pytz, uuid, re

from .serializers import UUIDSerializer

from .message_sender import email_ses_sender
from .sms_sender import sms_sender

class UUIDViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):

        print("POST Called")

        database = db_name()
        keys_collection = database['survey-keys']
        # data_collection = database['survey_data']

        data = request.data
        if 'email'and 'name' in data:
            email = data['email']
            name = data['name']
            # Validate Email using Regex
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return Response(data={"Error":"Email Not Valid"}, status=400)
            if 'phone' in data:
                phone = data['phone']
                if 'country_code' in data:
                    country_code = data['country_code']
                    if not re.match(r'^\d{2}$', country_code):
                        return Response(data={"Error":"Country Code Not Valid"}, status=400)
                else:
                    country_code = "91"
                if phone:
                    if not re.match(r'^\d{10}$', phone):
                        return Response(data={"Error":"Phone number Not Valid"}, status=400)
            else:
                phone = None
                country_code = None
            generated_uuid = str(uuid.uuid4())
            document = {
                "name":name,
                "email": email,
                "phone": phone,
                "country_code": country_code,
                "uuid": generated_uuid,
                "used": False,
                "email_sent": 0,
                "phone_sent": 0
            }
            result = keys_collection.insert_one(document)
            if (result.inserted_id):
                response = {
                    "id": str(result.inserted_id),
                    "name":name,
                    "email": email,
                    "phone": phone,
                    "country_code": country_code,
                    "uuid": generated_uuid,
                    "used": False,
                    "email_sent": 0,
                    "phone_sent": 0
                }

                return Response(data=response, status=201)
            else:
                return Response(data={"Error": "Could Not insert Document"}, status=500)

        else:
            return Response(data={"Error":"Email/ Name Not provided"}, status=400)
        
    def get(self, request):

        database = db_name()
        keys_collection = database['survey-keys']
        # data_collection = database['survey_data']
        print("GET called")
        surveys = keys_collection.find()
        if surveys.count() > 0:
            serializer = UUIDSerializer(surveys, many=True)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data={"Error":"No Records found yet"}, status=404)



class EmailSender(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        print("Email sender called")
        datas = request.data
        print(datas)
        database = db_name()
        keys_collection = database['survey-keys']
        # data_collection = database['survey_data']
        if datas:
            for data in datas:
                if "email" and "subject" and "body" in data:
                    email = data['email']
                    subject = data['subject']
                    body = data['body']
                    print("Got email -> " + email)
                    document = keys_collection.find_one({"email": email})
                    if document:
                        uuid = document['uuid']
                        print("Got uuid -> " + uuid)
                        result = email_ses_sender(email, subject, body)
                        email_sent = document.get('email_sent', 0) + 1
                        if result['success']:
                            print("Sent Email")
                            keys_collection.update_one({"email": email}, {"$set": {"email_sent": email_sent}})
                        else:
                            print("Sucess not True")
                            # return Response(data={"success": True, "message": "Email sent Successfully"}, status=201)
                        
                    else:
                        return Response(data={"Error":"No such email registered", "email": email}, status=404)
                else: 
                    return Response(data={"Error":"Please provide email, subject and body"}, status=404)
            print("Loop Completed")
            return Response(data={"success": True, "message": "Email sent Successfully"}, status=201)
        else:
            return Response(data={"Error":"Please provide email, subject and body"}, status=404)


class SmsSender(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        print("Sms sender called")
        data = request.data
        database = db_name()
        keys_collection = database['survey-keys']
        # data_collection = database['survey_data']
        if "recipients" in data:
            recipients = data['recipients']
            print("Got recipients -> " + str(recipients))
            result = sms_sender(recipients)
            if result:
                print("Sent SMS")
                return Response(data={"success": True, "message": "SMS sent Successfully"}, status=201)
                # return Response(data={"success": True, "message": "Email sent Successfully"}, status=201)
            else: 
                return Response(data={"Error":"Some error Occured"}, status=404)
            # return Response(data={"success": True, "message": "SMS sent Successfully"}, status=201)
        else:
            return Response(data={"Error":"Please provide reciepients as an array"}, status=404)
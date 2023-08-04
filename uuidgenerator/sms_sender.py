# import requests

# url = "https://control.msg91.com/api/v5/flow/"

# payload = {
#     "template_id": "1007161185523520924",
#     "sender": "TALCTY",
#     "short_url": 1,
#     "mobiles": "919050530232",
#     "VAR1": "VALUE 1",
#     "VAR2": "VALUE 2"
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authkey": "302461AJXRtdV6Fp455dc28fe8"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)


# def sms_sender(phone, body):
#     print("SMS send Function called")

#     sms = {
#         "phone": phone,
#         "message": body,
#         "success": True
#     }

#     return sms




# curl --location 'https://control.msg91.com/api/v5/flow/' \
# --header 'accept: application/json' \
# --header 'content-type: application/json' \
# --header 'authkey: 302461AJXRtdV6Fp455dc28fe8' \
# --data '{
#     "template_id": "1007168249019716721",
#     "sender": "TALCTY",
#     "recipients": [
#         {
#             "mobiles": "919050530232",
#             "var": "link"
#         }
#     ]
# }'


import requests,json

def sms_sender(recipients):

    print("Recipient Array")
    print(recipients)

    url = "https://control.msg91.com/api/v5/flow/"

    payload = {
    "template_id": "644910f0d6fc0578d135b8a3",
    "sender": "TALCTY",
    "short_url":"1",
    "recipients": recipients
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": "302461AJXRtdV6Fp455dc28fe8"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.text
    json_data = json.loads(data)
    if json_data['type'] == "success":
        success = True
        return success
    
    else:
        success = False
        return success

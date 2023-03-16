import websockets
import asyncio
import json
import requests

url = "https://api.xn--prve-hra.xn--svendeprven-ngb.dk/api/question/device?question=Hvad er svar på livet"

payload={}
headers = {
'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjMiLCJleHAiOjE3MTA1MDE4MDMsImlzcyI6InRlc3QtZXhhbS1hcGkifQ.9boMBfPswAjOZUo5ZcCLmSnNgk4elePBhGPZPVnOFrk'
}


print(str(payload))

response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
response = json.loads(response.text)

print(response["text"])
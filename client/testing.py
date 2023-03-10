import requests
import time
from matplotlib import pyplot as plt

def send_request(id):

    url = "http://127.0.0.1:8000/chatroom/post/"

    payload = {
        "message": f"Test number: {id}",
        "room_uuid": "ofqhGghh",
        "api_token": "c7a1a15ea18411951c5f0dd346f88468"
    }
    headers = {
        "Content-Type": "application/json"
    }

    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    elapsed_time = time.time() - start_time
    # print(elapsed_time)
    return elapsed_time
    # print(response.text)

dictio = {}

for i in range(10000):
    if i / 10000 == 0:
        print(f"Sending testcase {i}")
    dictio[i] = send_request(i)

#for item, times in dictio.items():
#    print(times)
lists = sorted(dictio.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.xlabel("Num. of requests")
plt.ylabel("Response time")
plt.show()
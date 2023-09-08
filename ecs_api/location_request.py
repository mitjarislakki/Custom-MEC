import requests
import json
import time


url = "https://<ip>:<port_number>/3gpp-analyticsexposure/v1/7a95e96f-18e0-479f-b38b-08e08115edb7/fetch"

timer = 300

headers = {
    "Content-Type": "application/json",
}

payload = {

    "analyEvent": "UE_MOBILITY",

    "tgtUe": {

        "gpsi": "msisdn-358440000000012"

    },

    "suppFeat": "0"

}

# Add json file saving for analytics from nwdaf or a database.
while True:
    response = requests.post(f"{url}", headers=headers, json=payload, verify=False)

    if response.status_code == 200:
        print("UE's Location successfully extracted")
        response_data = response.json()
        with open('UE-location.json', 'a') as f:
            json.dump(response_data, f)
    else:
        print("Error:", response.txt)

    print("Waiting interval: ", timer)

    time.sleep(timer)

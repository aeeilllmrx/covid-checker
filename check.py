import json
import os
import requests

from bs4 import BeautifulSoup as bs
from twilio.rest import Client

# First parse the page and check if there are any first doses in Brookyln
result = requests.get("https://nycvaccinelist.com")
src = result.content
soup = bs(src)

locations = soup.find('script', attrs={'id': "__NEXT_DATA__"})

text = json.loads(locations.contents[0])

brooklyn_locations = list(filter(
    lambda x: x.get('borough_county') == 'Brooklyn', 
    text['props']['pageProps']['locations']['locationsWithSlots']
))

first_doses = list(filter(
    lambda x: x.get('dose') != 'Second Dose',
    brooklyn_locations
))

# Just send a text saying an appointment is available.
# Account info from twilio.com/console
if len(first_doses) > 0:
    locations = [(x['name'], x['url']) for x in first_doses]

    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body="Appointments available at {}".format(locations),
            from_=os.environ['FROM_NUM'],
            to=os.environ['TO_NUM_1']
        )

    message = client.messages \
        .create(
            body="Appointments available at {}".format(locations),
            from_=os.environ['FROM_NUM'],
            to=os.environ['TO_NUM_2']
        )

else:
    print('no first doses available at this time')



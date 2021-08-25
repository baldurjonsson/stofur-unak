import requests
from bs4 import BeautifulSoup

def get_data(date, stofa):
    timestamp = int(date.replace(hour=0, minute=0).timestamp())
    url = f'https://ugla.unak.is/Yfirlit/ajax_public.php?request=Overview&date={timestamp}&type=stundaskra'
    table = []
    response = requests.get(url)
    if response and response.status_code == 200:
        json = response.json()
        if 'status' in json and json['status'] == True:
            if 'data' in json and 'html' in json['data']:
                soup = BeautifulSoup(json['data']['html'], 'html.parser')
                rows = soup.find('tbody').find_all('tr')
                timeslot = {
                    'from': '00:00',
                    'to': '00:00',
                }
                for tr in rows:
                    tds = tr.find_all('td')
                    for td in tds:
                        if 'colspan' in td.attrs:
                            times = td.text.split(' - ')
                            timeslot = {
                                'from': times[0],
                                'to': times[1],
                            }
                        else:
                            if td.text.find(stofa) != -1:
                                slot = timeslot.copy()
                                slot['comment'] = tds[5].text
                                slot['group'] = tds[0].text
                                table.append(slot)
            else:
                raise Exception('HTML missing from response')
        else:
            raise Exception('Missing status or not True from Ugla')
    else:
        raise Exception('Invalid response from Ugla')
    return table
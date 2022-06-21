import requests
import math

import graph as g
import cell_parameters

# init parameters, these determine the scoring cell that the information is taken from
# crsf, sessionid and v are used to authenticate
csrf = cell_parameters.csrf
sessionid = cell_parameters.sessionid
v = cell_parameters.v
caption_string = ""
headers = {
    'x-csrftoken': f'{csrf}',
    'referer': 'https://intel.ingress.com/',
    'cookie': f'csrftoken={csrf}; sessionid={sessionid};',
}
data = '{"latE6":%s,"lngE6":%s,"v":"%s"}' % (cell_parameters.latE6, cell_parameters.lngE6, v)

# fetch data from ingress' getRegionScoreDetails, sometimes it will not give output so there is a soft-retry mechanic
retries = 0
json_resp = None
while not json_resp and retries < 5:
    response = requests.post('https://intel.ingress.com/r/getRegionScoreDetails', headers=headers, data=data)
    json_resp = response.json()['result']
    #print(json_resp) # -> print output
    region_name = json_resp['regionName']
    retries += 1
try:
    last_checkpoint = json_resp['scoreHistory'][0][0]
except: 
    last_checkpoint = 0
remaining_checkpoints = 35 - int(last_checkpoint)

score_string = f"Score for checkpoint {last_checkpoint} in {region_name}:\n"
score_string += f"{int(json_resp['scoreHistory'][0][1])} 🐸\n{int(json_resp['scoreHistory'][0][2])} 💙"

# top agents info
top_agents_string = "Top Agents:"
for agent in json_resp['topAgents']:
    top_agents_string += f" {agent['nick']} ({agent['team'][:3]}) "

# loop through all checkpoints and make a sum
scores = json_resp['scoreHistory']
scores.reverse()
score_sum_enl, score_sum_res = 0, 0
score_list_enl, score_list_res = [], []
cumu_list_enl, cumu_list_res = [], []
diff, catchup_faction = 0, ""
for score in scores:
    score_sum_enl += int(score[1])
    score_sum_res += int(score[2])
    # append cumulatives
    cumu_list_enl.append(score_sum_enl + int(score[1]))
    cumu_list_res.append(score_sum_res + int(score[2]))
    score_list_enl.append(int(score[1]))
    score_list_res.append(int(score[2]))

# append to graph
if score_sum_enl > score_sum_res:
    catchup_faction = "RES"
    diff = score_sum_enl - score_sum_res
else:
    catchup_faction = "ENL"
    diff = score_sum_res - score_sum_enl

# combine and format caption
MU_string = f"{catchup_faction} is {diff} MU behind"
MU_string += f"\n{math.ceil(diff / remaining_checkpoints)} MU average over {remaining_checkpoints} remaining checkpoints"
caption_string += "\n" + score_string
caption_string += "\n\n" + top_agents_string
caption_string += "\n\n" + MU_string

# attach averages to caption string
caption_string += "\n\nAverage score over all checkpoints:"
caption_string += f"\n{int(json_resp['gameScore'][0])} 🐸"
caption_string += f"\n{int(json_resp['gameScore'][1])} 💙"

g.generate_plot(cumu_list_enl, cumu_list_res, 'cellscore_cumulative', region_name)
g.generate_plot(score_list_enl, score_list_res, 'cellscore_checkpoints', region_name)

# load image files
png_checkpoints_load = open('cellscore_checkpoints.png', 'rb')
png_cumulative_load = open('cellscore_cumulative.png', 'rb')
png_checkpoints = { 'photo': png_checkpoints_load }
png_cumulative = { 'photo': png_cumulative_load }

# post to telegram channel using chat id and telegram bot token
chatid = cell_parameters.chatid
bot = cell_parameters.bot
requests.post(f"https://api.telegram.org/bot{bot}/sendPhoto?chat_id={chatid}&caption={caption_string}", files=png_checkpoints)
requests.post(f"https://api.telegram.org/bot{bot}/sendPhoto?chat_id={chatid}&caption={caption_string}", files=png_cumulative)
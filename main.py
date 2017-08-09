__author__ = 'Binjih Lin'
__last_modified__ = "08/09/2017"
# In order to allow the request module, you must install the requests package. Using Pycharm (an integrated development
# IDE, you can install the requests module by going to File, Settings, and under Project Interpreter, click the +
# on the top right corner, and search for requests, and install it.
import requests

def request_summoner_data(region, summonerName, API_Key):
    # Request a Summoner's Data, used to get the JSON, eventually to get the ID
    URL = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + "?api_key=" + API_Key
    try:
        response = requests.get(URL)
    except:
        print("Could not get response from URL in request_summoner_data:", URL)
    return response.json()

def request_ranked_data(region, ID, API_Key):
    # Request the Ranked data in order to get Summoner Name, Division, and Tier
    URL = 'https://' + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + API_Key
    try:
        response = requests.get(URL)
    except:
        print("Could not get response from URL in request_ranked_data:", URL)
    return response.json()


def get_json(ID, API_Key):
    # URL = 'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/39911350' + "/entry?api_key=" + API_Key
    # Above doesnt work since match v3 not implemented yet
    URL = 'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + ID + "?api_key=" + API_Key
    try:
        response = requests.get(URL)
    except:
        print("Could not get response from URL in get_json:", URL)
    return response.json()


def get_match_IDs(json):
    # Get a list of all of your matches from the JSON file
    list_of_matches = []
    if 'matches' in json:
        for match in json['matches']:
            list_of_matches.append(match['gameId'])
        print("Number of Ranked Games: " + str(len(list_of_matches)))
        return list_of_matches


def overlapping_games(json1, json2):
    # returns list of matches that overlap between first player's json and second player's json
    overlap_game_IDs = []
    matches1 = get_match_IDs(json1)
    matches2 = get_match_IDs(json2)
    if matches1:
        for x in matches1:
            if matches2:
                if x in matches2:
                    overlap_game_IDs.append(x)
        return overlap_game_IDs


def analyze_games(ID1, ID2, overlap_game_IDs, API_Key):
    # run through the list of matches, call Riot's API to get the participant ID, which in turn we can find the
    # win for that participant. Currently set to the first ID called, but it doesn't matter
    count_wins = 0
    count_losses = 0
    for match in overlap_game_IDs:
        json1 = find_match_info(match, API_Key)
        pID = get_participant_ID(ID1, json1)
        if 'participants' in json1:
            for part in json1['participants']:
                if part['participantId'] == pID:
                    if part['stats']['win']:
                        count_wins += 1
                    else:
                        count_losses += 1
    return count_wins, count_losses


def get_participant_ID(ID1, json1):
    # Get the participant ID number from the
    # called in analyze_games to get the participant ID
    if 'participantIdentities' in json1:
        for player in json1['participantIdentities']:
            play_ID = player['player']['summonerId']
            if str(play_ID) == ID1:
                part_ID = player['participantId']
                return part_ID


def find_match_info(match_ID, API_Key):
    URL = 'https://na1.api.riotgames.com/lol/match/v3/matches/' + str(match_ID) + "?api_key=" + API_Key
    try:
        response = requests.get(URL)
        return response.json()
    except:
        print("Could not get response from URL in find_match_info:", URL)


def main():
    print("Welcome! br1, eun1, euw1, jp1, kr, la1, la2, na1, oc1, tr1, ru")
    region = input("Enter your region: ")
    # region = 'na1'
    summonerName1 = input("Enter your username: ")
    summonerName1 = ''.join(letter for letter in summonerName1 if letter.isalnum())
    summonerName2 = input("Enter your friend's username: (Must be ranked this season) ")
    summonerName2 = ''.join(letter for letter in summonerName2 if letter.isalnum())
    API_Key = input("Enter your API Key: ")
    try:
        response_json_get_id1 = request_summoner_data(region, summonerName1, API_Key)
        response_json_get_id2 = request_summoner_data(region, summonerName2, API_Key)
        ID1 = str(response_json_get_id1['id'])
        ID2 = str(response_json_get_id2['id'])
    except KeyError:
        print("Check your API Key to see if it is valid, or check if the summoner name is valid."
              + "If the summoner name and API Key are valid, then Riot can't handle the API calls. It is limited to "
              + "100 queries every two minutes. Wait before rerunning.")
    accountID1 = str(response_json_get_id1['accountId'])
    accountID2 = str(response_json_get_id2['accountId'])
    print("Your summoner ID's are: " + summonerName1 + ": " + ID1 + ", " + summonerName2 + ": " + ID2)

    print("Your account ID's are: " + summonerName1 + ": " + accountID1 + ", " + summonerName2 + ": " + accountID2)
    response_json_get_ranked_data1 = request_ranked_data(region, ID1, API_Key)
    try:
        print("Season 7: " + response_json_get_ranked_data1[0]['tier'] + " " + response_json_get_ranked_data1[0]['rank'] \
            + " " + str(response_json_get_ranked_data1[0]['leaguePoints']))
        print("W: " + str(response_json_get_ranked_data1[0]['wins']) + " L: " + \
              str(response_json_get_ranked_data1[0]['losses']))
    except KeyError:
        print(summonerName1 + " is not ranked this season.")


    response_json_get_ranked_data2 = request_ranked_data(region, ID2, API_Key)
    print(summonerName2 + ": " + ID2)
    try:
        print("Season 7: " + response_json_get_ranked_data2[0]['tier'] + " " + response_json_get_ranked_data2[0]['rank'] \
            + " " + str(response_json_get_ranked_data2[0]['leaguePoints']))
        print("W: " + str(response_json_get_ranked_data2[0]['wins']) + " L: " + \
              str(response_json_get_ranked_data2[0]['losses']))
    except IndexError:
        print(summonerName2 + " is not ranked this season.")
    json_1 = get_json(accountID1, API_Key)
    json_2 = get_json(accountID2, API_Key)
    print("Analyzing Games...")
    (num_wins, num_losses) = analyze_games(ID1, ID2, overlapping_games(json_1, json_2), API_Key)
    print("Number of Wins: " + str(num_wins))
    print("Number of Losses: " + str(num_losses))
    try:
        win_percent = 100 * (float(num_wins) / float(num_wins + num_losses))
        print("Win Percentage: %.2f" % win_percent)
    except ZeroDivisionError:
        print("No Games Played Together")


if __name__ == "__main__":
    main()

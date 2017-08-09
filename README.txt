Make sure you have Python 3 installed for this to work.
If you require an API key, please visit https://developer.riotgames.com/ sign in and get an API Key.
This program searches through Riot API, by entering your region, username, and friends username. It outputs your summoner IDs and account IDs,
along with current rank and W/L this season. It also outputs your total number of games, and then analyzes them to see any overlap between you and your friend.
It analyzes up to 94 of the past games, due to Riot limiting API requests to 100 every 2 minutes. 
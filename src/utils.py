import requests


def get_user_info(user_id):
    """
    Функция для получения информации о пользователе с помощью Steam API.
    """
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={user_id}"
    response = requests.get(url)

    return response.json()['response']['players'][0]

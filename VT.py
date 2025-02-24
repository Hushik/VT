import requests
import time

# Твой API-ключ и данные игрока
API_KEY = "RGAPI-af661b08-101e-45f8-bcf9-aa7c2c9ecbde"
NICKNAME = "Hush"
TAG = "JKK0"

# Функция для получения PUUID
def get_puuid(api_key, nickname, tag):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/{tag}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            puuid = data['puuid']
            print(f"PUUID для {nickname}#{tag}: {puuid}")
            return puuid
        else:
            print(f"Ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None

# Функция для получения списка последних матчей
def get_match_history(api_key, puuid):
    url = f"https://europe.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            matches = response.json()
            print(f"\nПоследние матчи для PUUID {puuid}:")
            for match in matches['matches']:
                print(f"- Match ID: {match['matchId']}, Режим: {match['queueId']}")
        else:
            print(f"Ошибка: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при запросе: {e}")

# Функция для получения ранга игрока
def get_player_rank(api_key, puuid):
    url = f"https://europe.api.riotgames.com/val/ranked/v1/leaderboards/by-puuid/{puuid}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            rank_data = response.json()
            print(f"\nРанг игрока с PUUID {puuid}:")
            print(f"- Текущий ранг: {rank_data['tier']}")
            print(f"- Рейтинг: {rank_data['rankedRating']}")
        else:
            print(f"Ошибка: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при запросе: {e}")

# Функция для получения информации о текущем матче
def get_current_match(api_key, puuid):
    url = f"https://europe.api.riotgames.com/val/spectator/v1/active-games/by-puuid/{puuid}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            match_data = response.json()
            print(f"\nТекущий матч для PUUID {puuid}:")
            print(f"- Режим: {match_data['gameMode']}")
            print(f"- Карта: {match_data['mapId']}")
            print("Игроки:")
            for player in match_data['participants']:
                print(f"- {player['gameName']}#{player['tagLine']} (Уровень: {player['level']})")
        else:
            print(f"Ошибка: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при запросе: {e}")

# Основная функция
def main():
    # Получаем PUUID
    puuid = get_puuid(API_KEY, NICKNAME, TAG)
    if not puuid:
        print("Не удалось получить PUUID. Проверь API-ключ и данные игрока.")
        return

    # Основной цикл программы
    while True:
        print("\nВыбери действие:")
        print("1. Получить список последних матчей")
        print("2. Получить информацию о ранге")
        print("3. Получить информацию о текущем матче")
        print("4. Выйти")
        choice = input("Введи номер действия: ")

        if choice == "1":
            get_match_history(API_KEY, puuid)
        elif choice == "2":
            get_player_rank(API_KEY, puuid)
        elif choice == "3":
            get_current_match(API_KEY, puuid)
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуй еще раз.")

        # Пауза перед следующим запросом
        time.sleep(1)

if __name__ == "__main__":
    main()

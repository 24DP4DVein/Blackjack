import random
import json
import os


suits = ['♠', '♥', '♦', '♣']
ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
         'J': 10, 'Q': 10, 'K': 10, 'A': 11}

deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
players_data_file = "players.json"

def load_players():

    if os.path.exists(players_data_file):
        with open(players_data_file, "r") as file:
            return json.load(file)
    return {}

def save_players(players):

    with open(players_data_file, "w") as file:
        json.dump(players, file)

def register_player():

    players = load_players()
    username = input("Введите ваше имя: ").strip()

    if username in players:
        print(f"Добро пожаловать, {username}! Ваш текущий баланс: {players[username]['balance']} кредитов.")
    else:
        players[username] = {"balance": 100}  
        print(f"Новый игрок зарегистрирован: {username}. Начальный баланс: 100 кредитов.")
        save_players(players)

    return username, players[username]

def deal_card():

    return deck.pop(random.randint(0, len(deck) - 1))

def calculate_score(hand):

    score = sum(ranks[card[:-1]] for card in hand)
    num_aces = sum(1 for card in hand if card.startswith('A'))

    while score > 21 and num_aces:
        score -= 10  
        num_aces -= 1

    return score
def display_hand(player, hand):

    print(f"{player}: {' '.join(hand)} (Очки: {calculate_score(hand)})")

def place_bet(balance):

    while True:
        try:
            bet = int(input(f"Введите вашу ставку (доступно {balance} кредитов): "))
            if 1 <= bet <= balance:
                return bet
            else:
                print("Некорректная ставка. Попробуйте снова.")
        except ValueError:
            print("Введите число!")

def blackjack():
    global deck
    deck = [f"{rank}{suit}" for suit in suits for rank in ranks]  
    random.shuffle(deck)

    username, player_data = register_player()
    balance = player_data["balance"]

    if balance <= 0:
        print("У вас недостаточно кредитов для игры. Пополните баланс!")
        return

    bet = place_bet(balance)

    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    display_hand("Игрок", player_hand)
    print(f"Дилер: {dealer_hand[0]} ?")


    while calculate_score(player_hand) < 21:
        move = input("Взять карту (h) или остановиться (s)? ").lower()
        if move == 'h':
            player_hand.append(deal_card())
            display_hand("Игрок", player_hand)
        else:
            break


    if calculate_score(player_hand) > 21:
        print("Вы проиграли! Перебор.")
        balance -= bet
        player_data["balance"] = balance
        save_players(load_players() | {username: player_data})
        return

    print("\nХод дилера...")
    display_hand("Дилер", dealer_hand)

    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())
        display_hand("Дилер", dealer_hand)


    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if dealer_score > 21 or player_score > dealer_score:
        print(f"Поздравляем, {username}, вы выиграли!")
        balance += bet
    elif player_score < dealer_score:
        print("Вы проиграли!")
        balance -= bet
    else:
        print("Ничья!")


    player_data["balance"] = balance
    save_players(load_players() | {username: player_data})

    print(f"Ваш новый баланс: {balance} кредитов.")


blackjack()
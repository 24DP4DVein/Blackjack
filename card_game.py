import random

#Klass loading (Galvenais logs vai logo)

#Klass with all users and save in file

class BlackjackDeck: #Galvna dala
    def init(self):
        self.cards = self._create_deck()
        random.shuffle(self.cards)
        self.hand = []

    def _create_deck(self):

        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠️', '♥️', '♦️', '♣️']
        deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
        return deck

    def deal_card(self):
        if not self.cards:
            print("Колода пуста! Перемешиваем заново.")
            self.cards = self._create_deck()
            random.shuffle(self.cards)

        card = self.cards.pop()
        self.hand.append(card)
        print(f"Вы получили карту: {card['rank']} {card['suit']}")
        self._check_score()

    def _calculate_score(self):
        score = 0
        aces = 0

        for card in self.hand:
            rank = card['rank']
            if rank in 'JQK':
                score += 10
            elif rank == 'A':
                aces += 1
                score += 11
            else:
                score += int(rank)

        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score

    def _check_score(self):
        score = self._calculate_score()
        print(f"Ваш счёт: {score}")

        if score > 21:
            print("Вы проиграли! Перебор.")

    def get_hand(self):
        return ', '.join([f"{card['rank']} {card['suit']}" for card in self.hand])


game = BlackjackDeck()

while True:
    action = input("Введите 'hit', чтобы взять карту, или 'stop', чтобы выйти: ").strip().lower()
    if action == 'hit':
        game.deal_card()
    elif action == 'stop':
        print(f"Ваши карты: {game.get_hand()}. Итоговый счёт: {game._calculate_score()}")
        break
    else:
        print("Неверная команда! Введите 'hit' или 'stop'.")

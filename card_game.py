
#Klass loading (Galvenais logs vai logo)

#Klass with all users and save in file

import random

class BlackjackGame:
    def __init__(self):
        self.deck = self._create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []

    def _create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠️', '♥️', '♦️', '♣️']
        return [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

    def _deal_card(self, hand):
        if not self.deck:
            print("Колода пуста! Перемешиваем заново.")
            self.deck = self._create_deck()
            random.shuffle(self.deck)

        card = self.deck.pop()
        hand.append(card)
        return card

    def _calculate_score(self, hand):
        score = 0
        aces = 0

        for card in hand:
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

    def _show_hand(self, hand):
        return ', '.join([f"{card['rank']} {card['suit']}" for card in hand])

    def _player_turn(self):
        while True:
            print(f"Ваши карты: {self._show_hand(self.player_hand)} (Счёт: {self._calculate_score(self.player_hand)})")
            action = input("Введите 'hit', чтобы взять карту, или 'stand', чтобы остановиться: ").strip().lower()
            if action == 'hit':
                self._deal_card(self.player_hand)
                if self._calculate_score(self.player_hand) > 21:
                    print(f"Ваши карты: {self._show_hand(self.player_hand)} (Счёт: {self._calculate_score(self.player_hand)})")
                    print("Вы проиграли! Перебор.")
                    return False  
            elif action == 'stand':
                return True  
            else:
                print("Неверная команда! Введите 'hit' или 'stand'.")

    def _dealer_turn(self):
        print("\nХод дилера...")
        while self._calculate_score(self.dealer_hand) < 17:
            self._deal_card(self.dealer_hand)

        dealer_score = self._calculate_score(self.dealer_hand)
        print(f"Карты дилера: {self._show_hand(self.dealer_hand)} (Счёт: {dealer_score})")
        return dealer_score

    def play(self):
        print("Добро пожаловать в Блэк Джек!")

        # Раздаём карты
        self._deal_card(self.player_hand)
        self._deal_card(self.player_hand)
        self._deal_card(self.dealer_hand)
        self._deal_card(self.dealer_hand)

        # Показываем карты
        print(f"\nВаши карты: {self._show_hand(self.player_hand)} (Счёт: {self._calculate_score(self.player_hand)})")
        print(f"Первая карта дилера: {self.dealer_hand[0]['rank']} {self.dealer_hand[0]['suit']}")

        # Ход игрока
        if not self._player_turn():
            return

        # Ход дилера
        dealer_score = self._dealer_turn()
        player_score = self._calculate_score(self.player_hand)

        # победител
        if dealer_score > 21 or player_score > dealer_score:
            print("Поздравляем! Вы победили!")
        elif player_score < dealer_score:
            print("Дилер победил! Вы проиграли.")
        else:
            print("Ничья!")

# Запуск игры
if __name__ == "__main__":
    while True:
        game = BlackjackGame()
        game.play()
        again = input("\nХотите сыграть ещё раз? (yes/no): ").strip().lower()
        if again != "yes":
            print("Спасибо за игру!")
            break
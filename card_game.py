
from random import randint


suits = ['♠', '♥', '♦', '♣']
ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

def diler():
    diler_card = []
    diler_card.append(randint(0,10))
    diler_card.append(randint(0,10))
    print(diler_card)

diler()


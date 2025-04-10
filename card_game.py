import random
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


#izveidot klase ar logu "hello our casino"


#izveidot klasse ar top player


class Registration:
    def __init__(self):
        self.players = {}

    def register_player(self):
        clear_screen()
        print("Laipni lūdzam reģistrācijā!")
        while True:
            username = input("Ievadiet savu lietotājvārdu: ").strip()
            if username in self.players:
                print("Šis lietotājvārds jau ir reģistrēts. Lūdzu, izvēlieties citu.")
            else:
                self.players[username] = 1000  # Start with $1000
                print(f"Lietotājvārds '{username}' veiksmīgi reģistrēts! Jūsu sākuma bilance ir $1000.")
                return username
            

    #pievienot saglabatus datus csv faila

class Balance:
    def __init__(self, username, registration):
        self.username = username
        self.registration = registration

    def get_balance(self):
        return self.registration.players[self.username]

    def update_balance(self, amount):
        self.registration.players[self.username] += amount

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"Jūsu bilance ir ${self.get_balance()}. Ievadiet savu likmi: "))
                if bet > self.get_balance():
                    print("Jums nav pietiekami daudz līdzekļu šai likmei.")
                elif bet <= 0:
                    print("Likmei jābūt pozitīvai summai.")
                else:
                    self.update_balance(-bet)
                    print(f"Likme ${bet} pieņemta. Atlikusī bilance: ${self.get_balance()}.")
                    return bet
            except ValueError:
                print("Lūdzu, ievadiet derīgu summu.")

    def deposit(self):
        while True:
            try:
                amount = int(input("Ievadiet summu, kuru vēlaties iemaksāt: "))
                if amount <= 0:
                    print("Iemaksai jābūt pozitīvai summai.")
                else:
                    self.update_balance(amount)
                    print(f"Jūs veiksmīgi iemaksājāt ${amount}. Jūsu jaunā bilance ir ${self.get_balance()}.")
                    break
            except ValueError:
                print("Lūdzu, ievadiet derīgu summu.")

class Blackjack:
    def __init__(self):
        self.kava = self.sagatavot_kavu()
        random.shuffle(self.kava)
        self.speletaja_kartis = []
        self.dilera_kartis = []

    def sagatavot_kavu(self):
        rangi = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        mastis = ['♠', '♥', '♦', '♣']
        return [{'rangs': r, 'masts': m} for r in rangi for m in mastis]

    def dod_karti(self, roka):
        if not self.kava:
            self.kava = self.sagatavot_kavu()
            random.shuffle(self.kava)
        karte = self.kava.pop()
        roka.append(karte)
        return karte

    def aprekinat_punktus(self, roka):
        punkti = 0
        aces = 0
        for karte in roka:
            if karte['rangs'] in 'JQK':
                punkti += 10
            elif karte['rangs'] == 'A':
                aces += 1
                punkti += 11
            else:
                punkti += int(karte['rangs'])
        while punkti > 21 and aces:
            punkti -= 10
            aces -= 1
        return punkti

    def paradit_kartis(self, roka):
        return ' '.join([f"[{karte['rangs']}{karte['masts']}]" for karte in roka])

    def paradit_kartis_ascii(self, roka):
        lines = ["", "", "", "", ""]
        for karte in roka:
            rangs = karte['rangs']
            masts = karte['masts']
            lines[0] += "┌─────┐ "
            lines[1] += f"│{rangs:<2}   │ "  # Left-aligned rank
            lines[2] += f"│  {masts}  │ "  # Suit in the middle
            lines[3] += f"│   {rangs:>2}│ "  # Right-aligned rank
            lines[4] += "└─────┘ "
        return "\n".join(lines)

    def speletaja_gajiens(self, balance):
        while True:
            clear_screen()
            print(f"Jūsu bilance: ${balance.get_balance()}")
            print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
            print(f"Dīlera pirmā kārts: [{self.dilera_kartis[0]['rangs']}{self.dilera_kartis[0]['masts']}]")
            darbiba = input("'hit' - ņemt kārti, 'stand' - pietiek: ").strip().lower()
            if darbiba == 'hit':
                self.dod_karti(self.speletaja_kartis)
                if self.aprekinat_punktus(self.speletaja_kartis) > 21:
                    clear_screen()
                    print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
                    print("Jūs zaudējāt! Pārsniegts 21.")
                    a = str(input("vvod: "))
                    if a == "t":
                        return False
                    else:
                        print("ievadi pareizi")

                    
                    
            elif darbiba == 'stand':
                self.paradit_kartis_ascii(self.speletaja_kartis)
                a = str(input("vvod: "))
                if a == "t":
                    return True
                else:
                    print("ievadi pareizi")
                

    def dilera_gajiens(self):
        clear_screen()
        print("Dīlera gājiens...")
        while self.aprekinat_punktus(self.dilera_kartis) < 17:
            self.dod_karti(self.dilera_kartis)
        print(f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {self.aprekinat_punktus(self.dilera_kartis)})")
        return self.aprekinat_punktus(self.dilera_kartis)

    def spelet(self, balance):
        clear_screen()
        print(f"Jūsu bilance: ${balance.get_balance()}")
        print("Laipni lūdzam Blackjack spēlē!")
        bet = balance.place_bet()
        self.dod_karti(self.speletaja_kartis)
        self.dod_karti(self.speletaja_kartis)
        self.dod_karti(self.dilera_kartis)
        self.dod_karti(self.dilera_kartis)
        if not self.speletaja_gajiens(balance):
            print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
            print(f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {self.aprekinat_punktus(self.dilera_kartis)})")
            print(f"Jūs zaudējāt likmi ${bet}.")
            print(f"Jūsu aktuālā bilance: ${balance.get_balance()}")
            return
        dilera_punkti = self.dilera_gajiens()
        speletaja_punkti = self.aprekinat_punktus(self.speletaja_kartis)
        print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {speletaja_punkti})")
        print(f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {dilera_punkti})")
        if dilera_punkti > 21 or speletaja_punkti > dilera_punkti:
            print(f"Apsveicam! Jūs uzvarējāt! Jūs saņemat ${bet * 2}.")
            balance.update_balance(bet * 2)
        elif speletaja_punkti < dilera_punkti:
            print(f"Dīleris uzvarēja! Jūs zaudējāt likmi ${bet}.")
            a = input("Write 't' lai turpinat:")
            if a == "t":
                print("ejam talak")
            else:
                print("ievadiet pareizi")

        else:
            print(f"Neizšķirts! Jūsu likme ${bet} tiek atgriezta.")
            balance.update_balance(bet)
        print(f"Jūsu aktuālā bilance: ${balance.get_balance()}")

if __name__ == "__main__":
    registration = Registration()
    username = registration.register_player()
    balance = Balance(username, registration)
    while True:
        clear_screen()
        print(f"Jūsu bilance: ${balance.get_balance()}")
        action = input("Izvēlieties darbību: 'play' - spēlēt, 'deposit' - iemaksāt, 'exit' - iziet: ").strip().lower()
        if action == "play":
            spele = Blackjack()
            spele.spelet(balance)
        elif action == "deposit":
            balance.deposit()
        elif action == "exit":
            print(f"Paldies par spēli! Jūsu galīgā bilance ir ${balance.get_balance()}.")
            break
        else:
            print("Nederīga izvēle. Lūdzu, mēģiniet vēlreiz.")
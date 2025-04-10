import random
import os
import csv

CSV_FILE = "blackjack_players.csv"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Registration:
    def __init__(self):
        self.stats = {}  # username: {'games': x, 'wins': y, 'losses': z}
        self.load_data()

    def load_data(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    username, games, wins, losses = row
                    self.stats[username] = {
                        'games': int(games),
                        'wins': int(wins),
                        'losses': int(losses)
                    }

    def save_data(self):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for user, data in self.stats.items():
                writer.writerow([user, data['games'], data['wins'], data['losses']])

    def register_player(self):
        clear_screen()
        print("Laipni lūdzam reģistrācijā!")
        while True:
            username = input("Ievadiet savu lietotājvārdu: ").strip()
            if username in self.stats:
                print(f"Laipni atpakaļ, {username}!")
                return username
            else:
                self.stats[username] = {'games': 0, 'wins': 0, 'losses': 0}
                print(f"Lietotājvārds '{username}' veiksmīgi reģistrēts!")
                return username

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

    def paradit_kartis_ascii(self, roka):
        lines = ["", "", "", "", ""]
        for karte in roka:
            rangs = karte['rangs']
            masts = karte['masts']
            lines[0] += "┌─────┐ "
            lines[1] += f"│{rangs:<2}   │ "
            lines[2] += f"│  {masts}  │ "
            lines[3] += f"│   {rangs:>2}│ "
            lines[4] += "└─────┘ "
        return "\n".join(lines)

    def speletaja_gajiens(self):
        while True:
            clear_screen()
            print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
            print(f"Dīlera pirmā kārts: [{self.dilera_kartis[0]['rangs']}{self.dilera_kartis[0]['masts']}]")
            darbiba = input("'hit' - ņemt kārti, 'stand' - pietiek: ").strip().lower()
            if darbiba == 'hit':
                self.dod_karti(self.speletaja_kartis)
                if self.aprekinat_punktus(self.speletaja_kartis) > 21:
                    clear_screen()
                    print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
                    print("Jūs zaudējāt! Pārsniegts 21.")
                    return False
            elif darbiba == 'stand':
                return True

    def dilera_gajiens(self):
        clear_screen()
        print("Dīlera gājiens...")
        while self.aprekinat_punktus(self.dilera_kartis) < 17:
            self.dod_karti(self.dilera_kartis)
        print(f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {self.aprekinat_punktus(self.dilera_kartis)})")
        return self.aprekinat_punktus(self.dilera_kartis)

    def spelet(self):
        clear_screen()
        print("Laipni lūdzam Blackjack spēlē!")
        self.speletaja_kartis = []
        self.dilera_kartis = []
        self.dod_karti(self.speletaja_kartis)
        self.dod_karti(self.speletaja_kartis)
        self.dod_karti(self.dilera_kartis)
        self.dod_karti(self.dilera_kartis)

        if not self.speletaja_gajiens():
            return "lose"

        dilera_punkti = self.dilera_gajiens()
        speletaja_punkti = self.aprekinat_punktus(self.speletaja_kartis)
        print(f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {speletaja_punkti})")
        print(f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {dilera_punkti})")

        if dilera_punkti > 21 or speletaja_punkti > dilera_punkti:
            print("Apsveicam! Jūs uzvarējāt!")
            return "win"
        elif speletaja_punkti < dilera_punkti:
            print("Dīleris uzvarēja! Jūs zaudējāt.")
            return "lose"
        else:
            print("Neizšķirts!")
            return "draw"

if __name__ == "__main__":
    registration = Registration()

    while True:
        clear_screen()
        print("===== Blackjack =====")
        print("1. Spēlēt")
        print("2. Spēlētāja statistika")
        print("3. Iziet")
        choice = input("Izvēlies opciju (1/2/3): ").strip()

        if choice == "1":
            username = registration.register_player()

            while True:
                clear_screen()
                stats = registration.stats[username]
                print(f"Jūs esat pieslēdzies kā: {username}")
                print(f"Aizvadītās spēles: {stats['games']} | Uzvaras: {stats['wins']} | Zaudējumi: {stats['losses']}")
                action = input("Izvēlieties darbību: 'play' - spēlēt, 'exit' - iziet: ").strip().lower()

                if action == "play":
                    spele = Blackjack()
                    result = spele.spelet()

                    stats['games'] += 1
                    if result == "win":
                        stats['wins'] += 1
                    elif result == "lose":
                        stats['losses'] += 1

                    registration.save_data()
                    input("Nospiediet Enter, lai turpinātu...")

                elif action == "exit":
                    print("Paldies par spēli!")
                    registration.save_data()
                    break
                else:
                    print("Nederīga izvēle.")
        elif choice == "2":
            clear_screen()
            print("===== Spēlētāju statistika pēc winrate =====\n")
            print(f"{'Lietotājs':<15} {'Spēles':<7} {'Uzvaras':<8} {'Zaud.':<7} {'Winrate':<8}")
            print("-" * 50)
            sorted_players = sorted(
                registration.stats.items(),
                key=lambda item: (item[1]['wins'] / item[1]['games']) if item[1]['games'] > 0 else 0,
                reverse=True
            )
            for username, data in sorted_players:
                games = data['games']
                wins = data['wins']
                losses = data['losses']
                winrate = (wins / games * 100) if games > 0 else 0
                print(f"{username:<15} {games:<7} {wins:<8} {losses:<7} {winrate:.1f}%")
            input("\nNospiediet Enter, lai atgrieztos uz galveno izvēlni...")

        elif choice == "3":
            print("Uz redzēšanos!")
            break
        else:
            print("Nederīga izvēle.")

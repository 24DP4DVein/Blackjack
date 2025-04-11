import random
import os
import csv
import re
from colorama import init, Fore

# Инициализация colorama
init(autoreset=True)

CSV_FILE = "blackjack_players.csv"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Registration:
    def __init__(self):
        self.stats = {}  # username: {'games': x, 'wins': y, 'losses': z, 'balance': n, 'password': password}
        self.load_data()

    def load_data(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 6:
                    username, games, wins, losses, balance, password = row
                    self.stats[username] = {
                        'games': int(games),
                        'wins': int(wins),
                        'losses': int(losses),
                        'balance': float(balance),
                        'password': password
                    }

    def save_data(self):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for user, data in self.stats.items():
                writer.writerow([user, data['games'], data['wins'], data['losses'], data['balance'], data['password']])

    def register_player(self):
        clear_screen()
        print(Fore.GREEN + "Laipni lūdzam reģistrācijā!")
        while True:
            username = input("Ievadiet savu lietotājvārdu: ").strip()

            # Проверка имени пользователя
            if len(username) < 5:
                print(Fore.RED + "Lietotājvārds jābūt vismaz 5 rakstzīmēm garam!")
                continue
            if not re.match("^[A-Za-z]+$", username):  # Только буквы
                print(Fore.RED + "Lietotājvārds var saturēt tikai burtiem!")
                continue

            if username in self.stats:
                print(Fore.YELLOW + f"Laipni atpakaļ, {username}!")
                password = input("Ievadiet paroli: ").strip()
                if self.stats[username]['password'] == password:
                    print(Fore.GREEN + "Pieslēdzoties...")
                    return username
                else:
                    print(Fore.RED + "Nepareiza parole.")
            else:
                password = input("Izvēlieties paroli: ").strip()
                self.stats[username] = {'games': 0, 'wins': 0, 'losses': 0, 'balance': 100.0, 'password': password}  # Начальный баланс 100
                print(Fore.GREEN + f"Lietotājvārds '{username}' veiksmīgi reģistrēts!")
                return username

    def find_user_by_name(self, name):
        if name in self.stats:
            return self.stats[name]
        else:
            print(Fore.RED + "Lietotājs ar šo vārdu netika atrasts.")
            return None

    def get_sorted_players(self, sort_by="games", reverse=True):
        """
        Sort players based on a specific attribute (games, wins, losses, balance, or winrate).
        Default is by 'games'.
        """
        if sort_by not in ["games", "wins", "losses", "balance", "winrate"]:
            print(Fore.RED + "Nederīgs sortēšanas kritērijs!")
            return []

        sorted_players = sorted(
            self.stats.items(),
            key=lambda item: (
                item[1][sort_by] if sort_by != "winrate" else (
                    item[1]['wins'] / item[1]['games'] if item[1]['games'] > 0 else 0
                )
            ),
            reverse=reverse
        )
        return sorted_players

    def filter_players(self, min_games=0, min_wins=0, min_balance=0):
        """
        Filter players based on minimum games played, minimum wins and minimum balance.
        """
        filtered_players = [
            (username, data) for username, data in self.stats.items()
            if data['games'] >= min_games and data['wins'] >= min_wins and data['balance'] >= min_balance
        ]
        return filtered_players

    def deposit(self, username, amount):
        if amount <= 0:
            print(Fore.RED + "Depozīts nevar būt nulle vai negatīvs!")
            return False
        self.stats[username]['balance'] += amount
        print(Fore.GREEN + f"Depozīts veiksmīgi veikts. Jaunais bilance: {self.stats[username]['balance']:.2f}")
        self.save_data()
        return True

    def get_top_deposits(self):
        sorted_players = sorted(
            self.stats.items(),
            key=lambda item: item[1]['balance'],
            reverse=True
        )
        return sorted_players

    def get_top_wins(self):
        sorted_players = sorted(
            self.stats.items(),
            key=lambda item: item[1]['wins'],
            reverse=True
        )
        return sorted_players


class Blackjack:
    def __init__(self, user_data):
        self.kava = self.sagatavot_kavu()
        random.shuffle(self.kava)
        self.speletaja_kartis = []
        self.dilera_kartis = []
        self.user_data = user_data  # Сохраняем данные игрока (баланс и другие параметры)

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
            print(Fore.CYAN + f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
            print(Fore.YELLOW + f"Dīlera pirmā kārts: [{self.dilera_kartis[0]['rangs']}{self.dilera_kartis[0]['masts']}]")
            darbiba = input(Fore.GREEN + "'hit' - ņemt kārti, 'stand' - pietiek: ").strip().lower()
            if darbiba == 'hit':
                self.dod_karti(self.speletaja_kartis)
                if self.aprekinat_punktus(self.speletaja_kartis) > 21:
                    clear_screen()
                    print(Fore.CYAN + f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
                    print(Fore.RED + "Jūs zaudējāt! Pārsniegts 21.")
                    return False
            elif darbiba == 'stand':
                return True

    def dilera_gajiens(self):
        clear_screen()
        print(Fore.YELLOW + "Dīlera gājiens...")
        while self.aprekinat_punktus(self.dilera_kartis) < 17:
            self.dod_karti(self.dilera_kartis)
        print(Fore.YELLOW + f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {self.aprekinat_punktus(self.dilera_kartis)})")
        return self.aprekinat_punktus(self.dilera_kartis)

    def spelet(self, username, bet):
        # Проверка ставки
        if bet <= 0 or bet > self.user_data['balance']:  # Теперь используем баланс из user_data
            print(Fore.RED + "Nevar veikt šo likmi. Pārbaudiet, vai likme nav negatīva vai lielāka par bilanci.")
            return "invalid"
        
        clear_screen()
        print(Fore.GREEN + "Laipni lūdzam Blackjack spēlē!")
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
        print(Fore.CYAN + f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {speletaja_punkti})")
        print(Fore.YELLOW + f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {dilera_punkti})")

        if dilera_punkti > 21 or speletaja_punkti > dilera_punkti:
            print(Fore.GREEN + "Apsveicam! Jūs uzvarējāt!")
            self.user_data['balance'] += bet * 2  # Победа - удваиваем ставку
            return "win"
        elif speletaja_punkti < dilera_punkti:
            print(Fore.RED + "Dīleris uzvarēja! Jūs zaudējāt.")
            self.user_data['balance'] -= bet  # Проигрыш - теряем ставку
            return "lose"
        else:
            print(Fore.YELLOW + "Neizšķirts!")
            return "draw"


if __name__ == "__main__":
    registration = Registration()

    while True:
        clear_screen()
        print(Fore.GREEN + "===== Blackjack =====")
        print(Fore.YELLOW + "1. Spēlēt (Reģistrēties / Ienākt)")
        print(Fore.YELLOW + "2. Spēlētāja statistika")
        print(Fore.YELLOW + "3. Iziet")
        choice = input(Fore.GREEN + "Izvēlies opciju (1/2/3): ").strip()

        if choice == "1":
            username = registration.register_player()

            while True:
                clear_screen()
                stats = registration.stats[username]
                print(Fore.GREEN + f"Jūs esat pieslēdzies kā: {username}")
                print(Fore.YELLOW + f"Aizvadītās spēles: {stats['games']} | Uzvaras: {stats['wins']} | Zaudējumi: {stats['losses']} | Bilance: {stats['balance']:.2f}")

                action = input(Fore.GREEN + "Izvēlieties darbību: 'play' - spēlēt, 'exit' - iziet, 'deposit' - depozīts: ").strip().lower()

                if action == "play":
                    bet = float(input(Fore.GREEN + f"Ievadiet likmi (Balanss: {stats['balance']:.2f}): ").strip())
                    
                    if bet > stats['balance']:
                        print(Fore.RED + "Likme ir lielāka par bilanci! Lūdzu, veiciet depozītu.")
                        continue
                    
                    spele = Blackjack(stats)
                    result = spele.spelet(username, bet)

                    stats['games'] += 1
                    if result == "win":
                        stats['wins'] += 1
                    elif result == "lose":
                        stats['losses'] += 1

                    registration.save_data()
                    input(Fore.GREEN + "Nospiediet Enter, lai turpinātu...")
                
                elif action == "exit":
                    print(Fore.GREEN + "Uz redzēšanos!")
                    break

                elif action == "deposit":
                    deposit_amount = float(input(Fore.GREEN + "Ievadiet depozīta summu: ").strip())
                    if deposit_amount > 0:
                        registration.deposit(username, deposit_amount)
                else:
                    print(Fore.RED + "Nederīga izvēle.")
        elif choice == "2":
            clear_screen()
            print(Fore.GREEN + "===== Spēlētāju statistika pēc winrate =====\n")
            print(Fore.YELLOW + f"{'Lietotājs':<15} {'Spēles':<7} {'Uzvaras':<8} {'Zaud.':<7} {'Bilance':<8}")
            print("-" * 50)

            sort_criteria = input(Fore.GREEN + "Izvēlieties sortēšanas kritēriju (games, wins, losses, balance): ").strip()
            reverse_order = input(Fore.GREEN + "Vai vēlaties šķirot augošā secībā? (y/n): ").strip().lower() != "y"

            sorted_players = registration.get_sorted_players(sort_by=sort_criteria, reverse=reverse_order)
            for username, data in sorted_players:
                games = data['games']
                wins = data['wins']
                losses = data['losses']
                balance = data['balance']
                print(Fore.YELLOW + f"{username:<15} {games:<7} {wins:<8} {losses:<7} {balance:.2f}")
            input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz galveno izvēlni...")

        elif choice == "3":
            print(Fore.GREEN + "Uz redzēšanos!")
            break
        else:
            print(Fore.RED + "Nederīga izvēle.")

import random
import os
import csv
import re
from colorama import init, Fore
from datetime import datetime
import sys
import time

# Инициализация colorama
init(autoreset=True)

CSV_FILE = "blackjack_players.csv"
DEPOSITS_FILE = "deposits.csv"
GAME_HISTORY_FILE = "game_history.csv"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class BlackjackLoader:
    def __init__(self, total_steps=40, delay=0.04):
        self.total_steps = total_steps
        self.delay = delay

    def animate(self):
        print("\n" * 2)
        print(Fore.GREEN + r'''
+==============================================+
| ____  _            _       _            _    |
|| __ )| | __ _  ___| | __  | | __ _  ___| | __|
||  _ \| |/ _` |/ __| |/ /  | |/ _` |/ __| |/ /|
|| |_) | | (_| | (__|   < |_| | (_| | (__|   < |
||____/|_|\__,_|\___|_|\_\___/ \__,_|\___|_|\_\|
+==============================================+
''')
        print("\n")

        bar_length = 40

        for i in range(self.total_steps + 1):
            progress = i / self.total_steps
            filled_length = int(bar_length * progress)
            bar = "[" + "=" * filled_length + " " * (bar_length - filled_length) + "]"
            percent = int(progress * 100)

            sys.stdout.write(" " * 10 + f"\r{bar} {percent}%")
            sys.stdout.flush()
            time.sleep(self.delay)

        print("\n\n" + " " * 10 + "Loading complete! Starting game...\n")
        time.sleep(1)

# Класс для игры Blackjack
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
            darbiba = input(Fore.GREEN + "'h' - ņemt kārti, 's' - pietiek: ").strip().lower()
            if darbiba == 'h':
                self.dod_karti(self.speletaja_kartis)
                if self.aprekinat_punktus(self.speletaja_kartis) > 21:
                    clear_screen()
                    print(Fore.CYAN + f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {self.aprekinat_punktus(self.speletaja_kartis)})")
                    print(Fore.RED + "Jūs zaudējāt! Pārsniegts 21.")
                    return False
            elif darbiba == 's':
                return True

    def dilera_gajiens(self):
        clear_screen()
        print(Fore.YELLOW + "Dīlera gājiens...")
        while self.aprekinat_punktus(self.dilera_kartis) < 17:
            self.dod_karti(self.dilera_kartis)
        print(Fore.YELLOW + f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {self.aprekinat_punktus(self.dilera_kartis)})")
        return self.aprekinat_punktus(self.dilera_kartis)

    def spelet(self, username, bet):
        if bet <= 0 or bet > self.user_data['balance']:
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
            print(Fore.RED + "Jūs pārsniedzāt 21! Jūs zaudējāt.")
            self.user_data['balance'] -= bet
            result = "lose"

            game_date = str(datetime.now())
            self.user_data['games'] += 1
            self.user_data['losses'] += 1

            if username not in registration.game_history:
                registration.game_history[username] = []
            registration.game_history[username].append((game_date, result, bet, self.user_data['balance']))
            registration.save_data()

            return result

        dilera_punkti = self.dilera_gajiens()
        speletaja_punkti = self.aprekinat_punktus(self.speletaja_kartis)
        print(Fore.CYAN + f"Jūsu kārtis:\n{self.paradit_kartis_ascii(self.speletaja_kartis)} (Punkti: {speletaja_punkti})")
        print(Fore.YELLOW + f"Dīlera kārtis:\n{self.paradit_kartis_ascii(self.dilera_kartis)} (Punkti: {dilera_punkti})")

        if dilera_punkti > 21 or speletaja_punkti > dilera_punkti:
            print(Fore.GREEN + "Apsveicam! Jūs uzvarējāt!")
            self.user_data['balance'] += bet
            result = "win"
        elif speletaja_punkti < dilera_punkti:
            print(Fore.RED + "Dīleris uzvarēja! Jūs zaudējāt.")
            self.user_data['balance'] -= bet
            result = "lose"
        else:
            print(Fore.YELLOW + "Neizšķirts!")
            result = "draw"

        game_date = str(datetime.now())
        self.user_data['games'] += 1
        if result == "win":
            self.user_data['wins'] += 1
        elif result == "lose":
            self.user_data['losses'] += 1

        if username not in registration.game_history:
            registration.game_history[username] = []
        registration.game_history[username].append((game_date, result, bet, self.user_data['balance']))
        registration.save_data()
        return result


# Класс регистрации и управления пользователями
class Registration:
    def __init__(self):
        self.stats = {}  # username: {'email': email, 'games': x, 'wins': y, 'losses': z, 'balance': n, 'password': password}
        self.deposits = {}  # username: [('date', amount), ...]
        self.game_history = {}  # username: [('game_date', result, bet, new_balance), ...]
        self.load_player_data()
        self.load_deposit_data()
        self.load_game_history_data()

    def load_player_data(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 7:
                    username, email, games, wins, losses, balance, password = row
                    self.stats[username] = {
                        'email': email,
                        'games': int(games),
                        'wins': int(wins),
                        'losses': int(losses),
                        'balance': float(balance),
                        'password': password
                    }

    def load_deposit_data(self):
        if not os.path.exists(DEPOSITS_FILE):
            return
        with open(DEPOSITS_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    username, deposit_date, amount = row
                    if username not in self.deposits:
                        self.deposits[username] = []
                    self.deposits[username].append((deposit_date, float(amount)))

    def load_game_history_data(self):
        if not os.path.exists(GAME_HISTORY_FILE):
            return
        with open(GAME_HISTORY_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 5:
                    username, game_date, result, bet, new_balance = row
                    if username not in self.game_history:
                        self.game_history[username] = []
                    self.game_history[username].append((game_date, result, float(bet), float(new_balance)))

    def save_data(self):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for user, data in self.stats.items():
                writer.writerow([user, data['email'], data['games'], data['wins'], data['losses'], data['balance'], data['password']])
        
        with open(DEPOSITS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for user, deposits in self.deposits.items():
                for deposit in deposits:
                    writer.writerow([user, deposit[0], deposit[1]])  # [username, deposit_date, amount]
        
        with open(GAME_HISTORY_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for user, history in self.game_history.items():
                for game in history:
                    writer.writerow([user, game[0], game[1], game[2], game[3]])

    def register_player(self):
        clear_screen()
        print(Fore.GREEN + "Laipni lūdzam reģistrācijā!")
        while True:
            username = input("Ievadiet savu lietotājvārdu: ").strip()

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
                email = input("Ievadiet savu e-pasta adresi: ").strip()
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    print(Fore.RED + "E-pasta adrese nav pareiza!")
                    continue
                password = input("Izvēlieties paroli: ").strip()
                self.stats[username] = {
                    'email': email,
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'balance': 100.0,
                    'password': password
                }
                print(Fore.GREEN + f"Lietotājvārds '{username}' veiksmīgi reģistrēts!")
                return username

    def display_game_history(self, username):
        while True:
            clear_screen()
            print(Fore.GREEN + "===== Spēlētāja spēļu vēsture =====\n")
            
            if username not in self.game_history or not self.game_history[username]:
                print(Fore.RED + "Nav spēļu vēstures!")
                input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz galveno izvēlni...")
                return

            for game in self.game_history[username]:
                game_date, result, bet, new_balance = game
                print(Fore.YELLOW + f"{game_date:<20} {result:<10} {bet:<10} {new_balance:<10.2f}")
            
            print(Fore.CYAN + "\nIzvēlieties kā šķirot spēļu vēsturi:")
            print("  [1] Pēc likmes")
            print("  [2] Pēc bilances")
            print("  [Enter] Atgriezties uz galveno izvēlni")

            choice = input(Fore.GREEN + "\nIevadiet savu izvēli: ").strip()

            if choice == "1-":
                sorted_history = sorted(self.game_history[username], key=lambda x: x[0])  # pēc datuma
            elif choice == "2-":
                sorted_history = sorted(self.game_history[username], key=lambda x: x[1])  # pēc rezultāta
            elif choice == "1":
                sorted_history = sorted(self.game_history[username], key=lambda x: x[2], reverse=True)  # pēc likmes
            elif choice == "2":
                sorted_history = sorted(self.game_history[username], key=lambda x: x[3], reverse=True)  # pēc bilances
            elif choice == "":
                break
            else:
                continue

            clear_screen()
            print(Fore.GREEN + "===== Sašķirota spēļu vēsture =====\n")
            for game in sorted_history:
                game_date, result, bet, new_balance = game
                print(Fore.YELLOW + f"{game_date:<20} {result:<10} {bet:<10} {new_balance:<10.2f}")
            input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz izvēlni...")

    def display_deposits(self, username):
        clear_screen()
        print(Fore.GREEN + "===== Spēlētāja depozītu vēsture =====\n")
        if username in self.deposits:
            for deposit in self.deposits[username]:
                deposit_date, amount = deposit
                print(Fore.YELLOW + f"{deposit_date:<20} {amount:<10.2f}")
        else:
            print(Fore.RED + "Nav depozītu vēstures!")
        input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz galveno izvēlni...")

    def display_statistics(self):
        while True:
            clear_screen()
            print(Fore.GREEN + "===== Kopējā statistika =====\n")

            sorted_players = sorted(self.stats.items(), key=lambda item: item[1]['games'], reverse=True)
            
            print(Fore.YELLOW + f"{'Lietotājs':<15} {'Spēles':<7} {'Uzvaras':<8} {'Zaud.':<7} {'Bilance':<8}")
            print("-" * 50)

            for username, data in sorted_players:
                games = data['games']
                wins = data['wins']
                losses = data['losses']
                balance = data['balance']
                print(Fore.YELLOW + f"{username:<15} {games:<7} {wins:<8} {losses:<7} {balance:.2f}")

            print(Fore.CYAN + "\nIzvēlieties, kā filtrēt statistiku:")
            print("  [1] Spēles vairāk nekā X")
            print("  [2] Uzvaras vairāk nekā X")
            print("  [3] Bilance lielāka nekā X")
            print("  [Enter] Atgriezties uz galveno izvēlni")

            choice = input(Fore.GREEN + "\nIevadiet savu izvēli: ").strip()

            if choice == "":
                break

            try:
                threshold = float(input(Fore.CYAN + "Ievadiet slieksni (X vērtību): ").strip())
            except ValueError:
                print(Fore.RED + "Nepareizs ievads! Jāievada skaitlis.")
                input(Fore.GREEN + "\nNospiediet Enter, lai turpinātu...")
                continue

            if choice == "1":
                filtered_players = [(username, data) for username, data in self.stats.items() if data['games'] >= threshold]
            elif choice == "2":
                filtered_players = [(username, data) for username, data in self.stats.items() if data['wins'] >= threshold]
            elif choice == "3":
                filtered_players = [(username, data) for username, data in self.stats.items() if data['balance'] >= threshold]
            else:
                continue

            clear_screen()
            print(Fore.GREEN + "===== Filtrētā statistika =====\n")

            if filtered_players:
                print(Fore.YELLOW + f"{'Lietotājs':<15} {'Spēles':<7} {'Uzvaras':<8} {'Zaud.':<7} {'Bilance':<8}")
                print("-" * 50)
                for username, data in filtered_players:
                    games = data['games']
                    wins = data['wins']
                    losses = data['losses']
                    balance = data['balance']
                    print(Fore.YELLOW + f"{username:<15} {games:<7} {wins:<8} {losses:<7} {balance:.2f}")
            else:
                print(Fore.RED + "Nav atrastu lietotāju ar norādītajiem kritērijiem.")

            input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz izvēlni...")

    
    def display_all_players(self):
        while True:
            column_index1 = 0  # Имя пользователя
            column_index2 = 2  # Кол-во игр
            clear_screen()
            print(Fore.GREEN + "===== Visi lietotaji =====\n")

            print(Fore.YELLOW + f"{'Lietotājs':<15} {'Spēles':<7}")
            print("-" * 50)

            players = []
            with open('blackjack_players.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    players.append(row)
                    print(Fore.YELLOW + f"{row[column_index1]:<20} {row[column_index2]:<10}")
            
            print()
            print("  [1] Lai meklet lietotaju...")
            print("  [Enter] Atgriezties uz galveno izvēlni")
            choice = input(Fore.GREEN + "\nIevadiet savu izvēli: ").strip()

            if choice == "1":
                search_name = input("Ievadiet lietotājvārdu, kuru vēlaties atrast: ").strip().lower()
                found = False
                print(Fore.CYAN + "\n--- Meklēšanas rezultāti ---\n")
                for row in players:
                    if search_name in row[column_index1].lower():
                        print(Fore.GREEN + f"Lietotājs: " + f"{row[column_index1]:<20} Spēles:  {row[column_index2]:<10}")
                        found = True
                        a = input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz galveno izvēlni...")
                if not found:
                    print(Fore.RED + "Lietotājs nav atrasts.")
                    a = input(Fore.GREEN + "\nNospiediet Enter, lai atgrieztos uz galveno izvēlni...")
            else:
                break


if __name__ == "__main__":

    loader = BlackjackLoader()
    loader.animate()

    registration = Registration()

    username = None  # Начальное значение переменной username

    while True:
        clear_screen()
        print(Fore.GREEN + "===== Blackjack =====")
        print(Fore.YELLOW + "1. Spēlēt (Reģistrēties / Ienākt)")
        print(Fore.YELLOW + "2. Kopējā statistika")
        print(Fore.YELLOW + "3. Iziet")
        choice = input(Fore.GREEN + "Izvēlies opciju (1/2/3): ").strip()

        if choice == "1":
            username = registration.register_player()

            while True:
                clear_screen()
                stats = registration.stats[username]
                print(Fore.GREEN + f"Jūs esat pieslēdzies kā: {username}")
                print(Fore.YELLOW + f"Aizvadītās spēles: {stats['games']} | Uzvaras: {stats['wins']} | Zaudējumi: {stats['losses']} | Bilance: {stats['balance']:.2f}")

                action = input(Fore.GREEN + "Izvēlieties darbību: 'h' - spēlēt, 'd' - depozīts, 'g' - mana spēļu statistika, 'p' - mana depozītu statistika, 'v' - paradit visus lietotajus, 'e' - iziet: ").strip().lower()

                if action == "h":
                    bet = float(input(Fore.GREEN + f"Ievadiet likmi (Balanss: {stats['balance']:.2f}): ").strip())
                    if bet > stats['balance']:
                        print(Fore.RED + "Likme ir lielāka par bilanci! Lūdzu, veiciet depozītu.")
                        continue
                    
                    spele = Blackjack(stats)
                    result = spele.spelet(username, bet)

                   
                    registration.save_data()
                    input(Fore.GREEN + "Nospiediet Enter, lai turpinātu...")

                elif action == "d":
                    deposit_amount = float(input(Fore.GREEN + "Ievadiet depozīta summu: ").strip())
                    if deposit_amount > 0:
                        # Добавляем депозит в память
                        deposit_date = str(datetime.now())
                        if username not in registration.deposits:
                            registration.deposits[username] = []
                        registration.deposits[username].append((deposit_date, deposit_amount))

                        # Обновляем баланс пользователя
                        stats['balance'] += deposit_amount

                        # Сохраняем изменения
                        registration.save_data()

                        print(Fore.GREEN + f"Depozīts veikts: {deposit_amount:.2f} EUR")

                elif action == "g":
                    registration.display_game_history(username)

                elif action == "p":
                    registration.display_deposits(username)

                elif action == "e":
                    print(Fore.RED + "Uz redzēšanos!")
                    break

                elif action == "v":
                    registration.display_all_players()

                else:
                    print(Fore.RED + "Nederīga izvēle.")
        elif choice == "2":
            registration.display_statistics()
        elif choice == "3":
            print(Fore.RED + "Uz redzēšanos!")
            break
        else:
            print(Fore.RED + "Nederīga izvēle.")

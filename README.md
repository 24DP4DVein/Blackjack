# Daniels Veinbergs un Artjoms Semjonovs  
## Blackjack – Konsoles spēle Python valodā

---

## 🎲 Projekta apraksts

Šis projekts ir Blackjack spēles konsoles versija, izstrādāta Python valodā ar uzlabotu funkcionalitāti, tostarp:

- Reģistrācijas un autorizācijas sistēma
- Kredītu bilance un likmes
- Vairāku spēļu atbalsts vienlaikus ar lietotāja vēstures saglabāšanu
- Spēles pārtraukšanas un turpināšanas iespēja
- Statistikas apkopošana

---

## 🕹 Spēles iespējas

### ✅ Reģistrācija un autorizācija
- Katram spēlētājam tiek izveidots konts ar lietotājvārdu.
- Lietotāja dati tiek saglabāti `blackjack_players.csv` failā.
- Bilance tiek saglabāta un atjaunināta starp spēlēm.

### 💰 Bilance un likmes
- Katram spēlētājam ir sākuma bilance.
- Likmes tiek veiktas pirms katras spēles.
- Laimesta aprēķins atkarīgs no spēles iznākuma.

### ♠️ Spēles gaita
- Spēlētājs sāk ar 2 kārtīm.
- Var izvēlēties: `ņemt` vai `apstāties`.
- Dīleris ņem kārtis, kamēr viņa punkti < 17.
- Uzvar tas, kurš ir tuvāk 21 punktam, nepārsniedzot to.

### 🃏 Kāršu vērtības
- Dūzis (A): 1 vai 11 (automātiski izvēlēts)
- 2–10: attiecīgā skaitliskā vērtība
- J, Q, K: 10 punkti

### 💾 Datu saglabāšana
- Visi spēlētāju dati (bilance, statistika) tiek saglabāti `.csv` failos.
- Nepabeigta spēle tiek saglabāta, un to var turpināt vēlāk.
- Tiek uzskaitītas uzvaras, zaudējumi, un Blackjack gadījumi.

---

## 📊 Statistika

Pēc katras spēles spēlētājs var:
- Apskatīt savu spēles vēsturi
- Redzēt, cik reizes uzvarēts, zaudēts, un cik reizes iegūts Blackjack
- Pārbaudīt savu aktuālo bilanci

---

## 🛠 Kā palaist spēli?

1. **Instalē Python (ja vēl nav)**
   - [Lejupielādē Python](https://www.python.org/downloads/) un instalē.

2. **Lejupielādē projektu**
   ```bash
   git clone https://github.com/24DP4DVein/two_deer_casino_with_sex_narkotiki_and_rock_n_roll
   cd blackjack

## 🧠 Kā darbojas saglabāšana?

Visi spēlētāju dati tiek uzglabāti `blackjack_players.csv`.

Ja spēle tiek pārtraukta (Ctrl+C vai izvēlne), to var turpināt vēlāk.

Bilance un statistika tiek atjaunināta automātiski pēc katras partijas.

## 💡 Ko varētu uzlabot nākotnē?

- 🔹 Grafiskais interfeiss (piemēram, ar pygame vai tkinter)
- 🔹 1.5x laimests par Blackjack
- 🔹 Tiešsaistes režīms pret citiem spēlētājiem
- 🔹 Vairāku kārtu turnīru režīms

Ja tev ir idejas vai vēlme piedalīties projektā – droši pievienojies GitHub!

## 📂 Licencēšana

Projekts ir izstrādāts mācību nolūkiem un ir brīvi izmantojams un uzlabojams.

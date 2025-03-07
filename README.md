# two_deer_casino_with_sex_drugs_and_rock_n_roll
# Daniels Veinbergs un Atrjoms Semjonovs

Blackjack – Konsoles spēle Python valodā

Projekta apraksts

Šis projekts ir Blackjack konsoles versija ar reģistrāciju, bilances sistēmu un likmēm. Spēlētājs spēlē pret dīleri, veicot likmes un pieņemot lēmumus – ņemt karti vai apstāties.


---

Spēles funkcijas

Reģistrācija un autorizācija – pirmajā startā spēlētājs izveido kontu, un bilance tiek saglabāta starp spēlēm.
Bilance un likmes – katram spēlētājam ir kredītu bilance, kuru var izmantot likmēm.
Spēles process – klasiski Blackjack noteikumi:

Spēlētājs saņem 2 kārtis un izlemj, vai ņemt vēl vai apstāties.

Dīleris ņem kārtis, kamēr viņam ir mazāk par 17 punktiem.

Uzvar tas, kurš ir tuvāk 21 punktam, nepārsniedzot to.
Datu saglabāšana – spēlētāju bilances tiek saglabātas players.json failā.



---

Spēles noteikumi

Mērķis – savākt 21 punktu vai būt tuvāk tam nekā dīleris.

Pārpirkšana (vairāk nekā 21 punkts) – automātisks zaudējums.

Dūzis (A) – var būt 1 vai 11 punkti, atkarībā no situācijas.

Kārtis J, Q, K – katra dod 10 punktus.

Likme – pirms spēles spēlētājam jāizdara likme.



---

🛠 Kā palaist spēli?

Instalē Python (ja vēl nav)

Lejupielādē Python no oficiālās mājaslapas un instalē to.

Lejupielādē projekta kodu

git clone https://github.com/24DP4DVein/two_deer_casino_with_sex_narkotiki_and_rock_n_roll
cd blackjack

Vai arī lejupielādē .zip failu un atarhivē to.

Palaid spēli

python blackjack.py


---

Kā darbojas saglabāšana?

Pēc pirmās spēles tiek izveidots fails players.json, kur tiek glabātas spēlētāju bilances.

Ja spēlētājs jau ir reģistrējies, viņš turpina spēli ar to pašu bilanci.

Bilance tiek automātiski atjaunināta pēc katras spēles.



---

Ko varētu uzlabot?

🔹 Grafiskais interfeiss (tkinter vai pygame)
🔹 1.5x laimests par Blackjack (21 ar divām kārtīm)
🔹 Tiešsaistes režīms ar spēli pret citiem spēlētājiem


---




---

Ja tev ir idejas, kā uzlabot spēli, droši piedalies izstrādē! 

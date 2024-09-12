# Tema 2 - Implementarea CUDA a algoritmului de consens Proof of Work din cadrul Bitcoin

cerinta 2024 ocw asc: https://ocw.cs.pub.ro/courses/asc/teme/tema2

## Enunț
Implementarea unui algoritm de consens distribuit Proof of Work pe blockchain folosind programare pe GPU în CUDA.

Disclaimer: Această temă a pornit de la algoritmul Bitcoin descris în whitepaper (https://bitcoin.org/bitcoin.pdf), însă nu replică în totalitate algoritmul și structurile de date.

## Introducere

Blockchain-ul este o tehnologie care a devenit cunoscută odată cu apariția criptomonedelor, precum Bitcoin-ul, Ethereum, etc. Este o formă de înregistrare descentralizată și distribuită a tranzacțiilor și datelor, care funcționează pe baza unui lanț de blocuri. Fiecare bloc înregistrează o serie de tranzacții și este legat de blocurile anterioare printr-un proces de criptare și verificare, cunoscut sub numele de “hashing”.

**Descentralizare**: Datele sunt stocate și gestionate de o rețea descentralizată de noduri, eliminând astfel nevoia de o autoritate centrală.

**Imutabilitate**: Datele înregistrate în blocurile blockchain-ului sunt imutabile și nu pot fi modificate sau șterse ulterior.

**Transparență**: Tranzacțiile și înregistrările sunt publice și transparente, iar oricine poate să le verifice.

**Securitate**: Criptografia și algoritmii de consens asigură securitatea și integritatea datelor stocate în blockchain.


## Obiectivele temei

În cadrul acestei teme veți participa ca nod într-un blockchain, unde execuția tranzacțiilor se va face pe GPU. Obiectivele temei:

- Înțelegerea conceptelor de bază ale blockchain-ului;
- Înțelegerea algoritmului de consens distribuit;
- Participarea la algoritmul de consens din perspectiva unui nod;
- Programarea pe GPU și folosirea limbajului CUDA;

## Algoritmul de consens

Calculatoarele participante la consens se numesc noduri (sau mineri în cazul PoW). Aceste noduri nu se cunosc și nu au încredere unele în altele. Scopul unui mecanism de consens este de a aduce toate nodurile în acord, adică de a avea încredere unul în celălalt, într-un mediu în care nodurile nu au încredere unul în celălalt.

Minerii (aceștia veți fi voi) efectuează lucrări de calcul în rezolvarea unei probleme matematice complexe. Demonstrarea rezolvării problemei aduce de la sine și încredere.
Problema matematică poate deveni mai complexă, în funcție de numărul de participanți la consens.
Minerul care a rezolvat primul problema, va propaga răspunsul în rețea, iar acest va fi validat de către ceilalți participanți la rețea. Astfel, problema are 2 proprietăți:

Este greu de calculat răspunsul;
Este ușor de verificat răspunsul.
Minerul care a rezolvat primul problema va fi recompensat. În cazul vostru, veți primi punctaj 

## Structura unui bloc

Un bloc este format din:

Hash-ul blocului anterior - o valoare predefinită;
Root hash-ul tranzacțiilor - o valoare calculată de host, tranzactiile avand valori predefinite;
Nonce (Number used only once) - un număr întreg random, pozitiv, pe 32 biți, pe care minerii încearcă să îl găsească, astfel încât hash-ul block-ului rezultat să fie mai mic decât o dificultate threshold (un alt hash, ales în funcție de numărul de 0-uri consecutive din prefix). Acest număr trebuie să îl găsiți, prin metoda trial-and-error.

Hash-ul rezultat al blocului se va folosi în continuare pentru crearea unui alt bloc. De aici vine denumirea de blockchain: se creează un lanț de blocuri, iar fiecare bloc depinde de cel anterior.

## Rezolvarea problemei
Problema de rezolvat este găsirea unei nonce care, atunci când se aplică o funcție hash, cum ar fi SHA-256, hash-ul începe cu un număr de zero biți. Munca medie necesară este exponențială în funcție de numărul de biți zero necesari și poate fi verificată prin executarea unui singur hash.

De exemplu, pornim de la “Hello world” și trebuie să găsim un nonce astfel încât hash-ul să înceapă cu un 0. Pentru nonce = 4, aplicând sha256(“Hello world4”) obținem un hash ce începe cu un 0:

”Hello world4” → 09b044fe014a500edc4358d55e4b59d595b7a2c9d01143ae37c577d1f68378e4

Considerăm această problemă ca având dificultatea = 1. Pentru o problemă cu dificultatea = 3, hash-ul rezultat va începe cu trei de 0: “000”.


## Cerințe ale temei
### Înțelegerea algoritmului de consens pe CPU
Veți porni de la directorul cpu_miner, ce conține implementarea deja făcută pe CPU. Acesta nu face parte din rezolvarea temei. Scopul codului este de a înțelege funcționalitatea pe CPU, ca apoi să optimizați căutarea nonce-ului pe GPU, folosind CUDA.
Acesta conține 5 teste:
4 pentru a vă familiariza cu funcțiile folosite.
al 5-lea este efectiv implementarea miner-ului pe CPU
Căutarea nonce-ului din testul 5 ar trebui să dureze ~2s pe xl, pentru o dificultate de 5 leading 0s.
Aceasta este o abordare simplistă a calculării unui block hash, cu complexitate redusă. Nu reflectă implementarea reală a algoritmilor de consens POW, având scop pur educativ.
Pași pentru rulare:
To compile: make
To run: make run
To clean: make clean

### Implementarea algoritmului de consens pe GPU
Veți porni de la directorul gpu_miner, în care veți realiza implementarea în CUDA a logicii din cpu_miner.
Veți implementa funcția device findNonce, care va paraleliza căutarea nonce-ului, folosind CUDA Threads. Aceasta trebuie implementată astfel încât să caute prin toate numerele de la 1 la MAX_NONCE.
Pentru a va ajută, aveți deja implementate funcții ajutătoare în utils.cu. Vă recomandăm să va folosiți de ele în implementarea voastră.
Nonce-ul găsit, hash-ul block-ului, precum și timpul rulării kernel-ului, vor fi scrise într-un fișier results.csv, în urmă apelarii funcției printResult din utils.cu.
Pași pentru rulare:
To compile: make
To run: make run
To clean: make clean

###Evaluarea performanței
Punctajul se va acorda în funcție de durata rulării kernel-ului findNonce. Pentru a testa eficiența implementării, în cazul valorilor predefinte în utils (previous block hash și cele 4 tranzacții, pentru o dificultate de 5 zero-uri), timpii rezultați sunt considerați:
100% pct implementare: t < 1s.
75% pct implementare: t < 1.5s.
50% pct implementare: t < 2s (durata rulării pe CPU).
0% pct implementare: t >= 2s SAU Nonce/Block hash incorect.
Unde t este timpul minim înregistrat în urma a 5 rulări succesive. Motivul pentru care rulăm de mai multe ori este că timpul poate fi diferit cu câteva zecimi de la o rulare la alta.




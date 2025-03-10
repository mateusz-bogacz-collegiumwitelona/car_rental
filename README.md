# Car Rent
Wypożyczalnia samochodów napisana w PHP, wykorzystująca bazę danych.  

### Jak uruchomić?
Najpierw zmień nazwę pliku `.env.example` na `.env`.  
Następnie w polu `MYSQL_ROOT_PASSWORD` ustaw dowolne inne hasło.  

**P.S. Jeśli nie masz Dockera, to polecam go zainstalować teraz.**  

Otwórz konsolę w folderze z plikami projektu i wykonaj następujące czynności:  

```sh
docker-compose build
```
To buduje obraz Dockera. Teraz wystarczy tylko uruchomić kontener za pomocą komendy:  
```sh
docker-compose up -d
```

Jeżeli chcemy wyłączyć kontenery, wykonujemy:  
```sh
docker-compose down
```

### Ważne info
W katalogu `src` trzymamy pliki HTML i PHP. Pliki JavaScript i CSS znajdują się w odpowiednich folderach.  
Najważniejszy jest katalog `src` – jeśli nie będzie tam plików, strona się nie wyświetli.  

## Szybki poradnik Gita
Git jest trudny. To prawda. Dlatego tutaj masz instrukcję, jak przygotować folder i pobrać repozytorium ze wszystkimi plikami. Po prostu kopiuj i wklej:  

```sh
git init # Inicjalizacja repozytorium
git branch -M main # Ustawienie głównej gałęzi
git remote add origin https://github.com/mateusz-bogacz-collegiumwitelona/car_rental.git # Ustawienie adresu repozytorium
git pull -u origin main # Pobranie zawartości repozytorium
```

A propos `git pull`... jeśli coś się zepsuje, to nie naprawi on Twojego repozytorium. Wtedy trzeba działać inaczej.  

**Uwaga! Dwa razy się zastanów, zanim użyjesz tej komendy.**  

```sh
git reset --hard origin/main # Resetuje całą gałąź – usuwa wszystkie lokalne zmiany i przywraca stan z serwera
````

W razie w pisz.

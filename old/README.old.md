# Car Rent
Wypożyczalnia samochodów napisana w Django, wykorzystująca bazę danych PostgresSQL.

## Co jest potrzebne?
- [Docker](https://www.docker.com/)
- [Node.JS](https://nodejs.org/en)
- [Python](https://www.python.org/)
- Jakikolwiek edytor kodu dla pythona. html i css. Od siebie polecam:
  - Visual Studio Code (za free)
  - PyCharm (mamy licencje od uczelni)
- Jakikowliek program do zarządzania bazą danych. Od siebie polecam:
  - Pgadmin (za darmo i najlepiej się sprawdza do PostgresSQL)
  - DataGrip (mamy licencje od uczelni i można go użyć do wielu baz danych)
  - HeidiSQL (mały, lekki i można go użyć do wielu baz danych)
  
## Jak włączyć

### Jak przygotować pliki boostrap?

**Jeżeli jeszcze nie masz zainstlowanego Node.js to zainstaluj to przed tymi czynnościami, i najlepiej zresetuj pc**
Otwórz konsolę w folderze z plikami projektu i wykonaj następujące czynności:

```sh
npm install
```
to zainstaluje wszystkie zależności do boostrapa. Done.

### Jak uruchomić środowisko w docker?
Najpierw zmień nazwę pliku `.env.example` na `.env`.  
Następnie w polu `DATABASE_USERNAME` ustaw dowolne inną nazwę użytkownika. Oraz w polu `DATABASE_PASSWORD` wstawić dowolne inne hasło do bazy danych.

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
**Jeżeli wproadziłeś jakieś zmiany w wyglądzie html najelpiej będzie zrobić `docker-compose restart` żeby te zmiany były widoczne**

### Jak podłączyć się do bazy danych?
Zalezy od tego czego używasz. W pgadmin z którego kożystam to jest dość proste bo wysarczy

1. Kliknąć na `Servers`
2. Uzupełnić Name jako `dockerdjango` 
3. Prześć do zakładki conneciton i tam wprowadzić dane: 
   1. Host name/adress: `localhost`
   2. Port: `5432`
   3. Maintenace database: `dockerdjango`
   4. Username i password: to co ustawiłeś w .env

### Jak przywrócić dane które już testowo stworzyłem 

Stworzyłem pierwsze dwie tabele. Przywróć je żeby nie było. 

Musisz wejść w `dockerdjango` > `Databases` > `dockerdjango` i pliknąc ppm na to i wybrać opcje `Restore...`.

Po tym w kliknąc w ikonke folderu obok `Filename` i wybrać plik sql. (Jak się nie wyświtla to zmień typy plików).

Żeby sprawdzić czy to w ogóle zadziało to musisz wejść w `dockerdjango` > `Databases` > `dockerdjango` > `Schemas` > `public` > `Tabeles` i sprawdzić czy są tabele  city i users.

### Jak zrobić backup do przywrócenia

**Pamiętaj że trzeba robić bazkupy danych bym też mógł na nich popracować**

Musisz wejść w `dockerdjango` > `Databases` > `dockerdjango` i pliknąc ppm na to i wybrać opcje `Backup...`.

Po tym w kliknąc w ikonke folderu obok `Filename` i wybrać plik sql. Proszę o zawyanie plików 

databases_dzień_miesiąc_rok_godzina_minuta.sql żebysmy wiedzeili co kiedy i gdzie.

### Wprowadznie zmian w bazie danych do Django

Jak zrobisz jakiekolwiek zmiany w bazie danych typu dodanie nowej kompurki czy nowej tabeli to dobrze by było w konsoli odpalić te komendy 

```sh
docker-compose exec  django-web python manage.py inspectdb > rent_a_car/models.py
``` 
doda odpowieni kod pythona do pliku models

```sh
docker-compose exec  django-web python manage.py makemigrations
```
tworzy plik migracji potrzeby do obsługi bazy danych

```sh
docker-compose exec  django-web python manage.py migrate
```
stosuje te migracje

## Przydatne linki
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django (Tutorial od Mozilii)
- https://www.w3schools.com/django/ (z tego kożystałem tworząc stronę uczelni i ten projekt)
- https://www.w3schools.com/bootstrap5/index.php (jak zawsze w3school dowozi x6)
- https://kursbootstrap.pl/o-bootstrapie.html (polski kurs bootstrap)


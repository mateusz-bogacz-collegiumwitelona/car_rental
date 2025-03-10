# Car rent
Wypożyczalnia samochodów napisana w PHP wykożystująca baze danych. 

### Jak uruchomić?
Wpier wypełnij zmień nazwę pliku .env.example na .env.
Następnie w polu MYSQL_ROOT_PASSWORD ustaw dowolne inne hasło

**P.S Jak nie masz dockera to polecam go zainstalować teraz.**

Następnie otwieramy konsole w folderze z plikami projektu i wykonujemy następujące czynności 
````
docker-compose build
````
to buduje obraz Dockera. Teraz Wystarczy tylko włączyć sam konerner za pomocą komendy 
````
docker-compose up -d
````

Jeżeli chemy wyłączyć kontenery tpo wykonujemy 
````
docker-compose down
````

### Ważne info
W src trzymamy pliki html, php. W js i css wiadomo.
Tu naważniejszy jest src, jak nie będą tam pliki to się nie wyświetlą. 

## Szybki poradnik Gita
Git jest trudny. To prawda. Dlatego tu masz taką instrukcje jak przygorować folder i pobrać repo z tym wszystkim co w  nim jest. Po prostu kopjuj. 

````
git init #Inicializacja repo
git branch -M main #Ustawienie na właściwy branch 
git remote add origin https://github.com/mateusz-bogacz-collegiumwitelona/car_rental.git #Ustawienie właściwego adresu na repo
git pull -u origin main #Pobranie zawartości z repo.
````

A propos git pull... jak coś się zepsuje to nie naprawi on twojego repo, w tedy trzeba działać innaczej. Dokładniej rzecz ujumując.

__Uwaga. Dwa razy się zastanów zanim to użyjesz.__

````
git reset --hard origin/main #Resetuje cały gałąź, czyli usuwa wszystkie lokalne zmiany i i przywraca to co jest na serwerze 
````

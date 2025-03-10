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


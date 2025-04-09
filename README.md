# Car Rent

Wypożyczalnia samochodów napisana w Django, wykorzystująca bazę danych PostgreSQL.

## Co jest potrzebne?

- [Docker](https://www.docker.com/)
- [pgAdmin](https://www.pgadmin.org/) do zarządzania bazą danych

## Jak uruchomić aplikację

### 1. Konfiguracja pliku środowiskowego

1. Zmień nazwę pliku `.env.example` na `.env`
2. W pliku `.env` skonfiguruj następujące pola:
   - `DATABASE_USERNAME`: ustaw własną nazwę użytkownika
   - `DATABASE_PASSWORD`: ustaw własne hasło do bazy danych

### 2. Uruchomienie aplikacji w Dockerze

Otwórz konsolę w folderze z plikami projektu i wykonaj następujące komendy:

```sh
# Zbuduj obraz Dockera
docker-compose build

# Uruchom kontener
docker-compose up -d
```

Aby wyłączyć kontenery, wykonaj:

```sh
docker-compose down
```

> **Uwaga**: Jeżeli wprowadziłeś zmiany w plikach HTML, najlepiej wykonać `docker-compose build`, aby zmiany zostały uwzględnione.

### 3. Dostęp do aplikacji

Po uruchomieniu, aplikacja będzie dostępna pod adresem: `http://localhost:8000`

## Zarządzanie bazą danych

### Jak połączyć się z bazą danych (pgAdmin)

1. Otwórz pgAdmin i kliknij prawym przyciskiem myszy na `Servers`
2. Wybierz `Create` > `Server...`
3. W zakładce `General` uzupełnij `Name` dowolną nazwą
4. Przejdź do zakładki `Connection` i wprowadź następujące dane:
   - Host name/address: `localhost`
   - Port: `5433`
   - Maintenance database: `dockerdjango`
   - Username: wartość ustawiona jako `DATABASE_USERNAME` w pliku `.env`
   - Password: wartość ustawiona jako `DATABASE_PASSWORD` w pliku `.env`
5. Kliknij `Save`

### Przywracanie danych testowych

1. W pgAdmin rozwiń drzewo `Servers` > [Twoja nazwa serwera] > `Databases`
2. Kliknij prawym przyciskiem myszy na `dockerdjango` i wybierz opcję `Restore...`
3. Kliknij ikonę folderu obok pola `Filename` i wybierz plik .backup (jeśli plik nie jest widoczny, zmień filtry wyświetlania plików)
4. Kliknij `Restore`
5. Aby sprawdzić, czy przywracanie się powiodło, przejdź do `Servers` > [Twoja nazwa serwera] > `Databases` > `dockerdjango` > `Schemas` > `public` > `Tables` i sprawdź, czy tabele są widoczne

### Tworzenie kopii zapasowej bazy danych

> **Ważne**: Pamiętaj o tworzeniu regularnych kopii zapasowych, aby umożliwić współpracę nad projektem.

1. W pgAdmin rozwiń drzewo `Servers` > [Twoja nazwa serwera] > `Databases`
2. Kliknij prawym przyciskiem myszy na `dockerdjango` i wybierz opcję `Backup...`
3. Ustaw nazwę pliku i lokalizację kopii zapasowej
4. Kliknij `Backup`

## Konfiguracja początkowa

### Tworzenie konta administratora

Jeżeli baza danych została przywrócona bez danych, należy stworzyć użytkownika administratora:

1. Uruchom kontenery:
   ```sh
   docker-compose build
   docker-compose up -d
   ```

2. Wejdź w powłokę bash kontenera:
   ```sh
   docker-compose exec -it rent_a_car bash
   ```

3. Uruchom powłokę Pythona:
   ```sh
   python manage.py shell
   ```

4. Wykonaj poniższy skrypt, zastępując wartości "example" własnymi danymi:
   ```python
   from django.contrib.auth.hashers import make_password
   from rent_a_car.models import Admin
   
   nowy_admin = Admin(
       imie="example",
       nazwisko="example",
       email="example",
       password=make_password("example")
   )
   nowy_admin.save()
   print(f"Dodano administratora: {nowy_admin}")
   exit()
   ```

5. Wyjdź z powłoki bash:
   ```sh
   exit
   ```

6. Przebuduj i uruchom ponownie kontenery:
   ```sh
   docker-compose build
   docker-compose up -d
   ```

7. Panel administracyjny będzie dostępny pod adresem: `http://localhost:8000/admin-dashboard`

## Rozwiązywanie problemów

- **Problem z połączeniem do bazy danych**: Upewnij się, że Docker działa i kontenery są uruchomione (`docker ps`)
- **Nie widać zmian w interfejsie**: Wykonaj `docker-compose build` i uruchom ponownie kontenery
- **Błąd dostępu do bazy danych**: Sprawdź poprawność danych w pliku `.env`

## Autorzy

- [Paweł Kruk](https://github.com/Kruk43854) - baza danych i frontend
- [Mateusz Bogacz-Drewniak](https://github.com/mateusz-bogacz-collegiumwitelona) - baza danych i backend
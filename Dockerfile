FROM python:3.13-slim AS builder
 
RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nodejs npm

# Kopiowanie całego projektu
COPY . /app/

# Instalacja zależności npm
COPY package.json /app/
RUN npm install --ignore-scripts

# Ręczne tworzenie katalogów na pliki statyczne (jeśli jeszcze nie istnieją)
RUN mkdir -p /app/rent_a_car/static/css
RUN mkdir -p /app/rent_a_car/static/js

# Ręczne kopiowanie plików Bootstrapa
RUN cp -f node_modules/bootstrap/dist/css/bootstrap.min.css /app/rent_a_car/static/css/ || true
RUN cp -f node_modules/bootstrap/dist/js/bootstrap.bundle.min.js /app/rent_a_car/static/js/ || true

# Uruchom collectstatic
RUN python manage.py collectstatic --noinput

FROM python:3.13-slim
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Kopiuj całą aplikację
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app /app

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "car_rental.wsgi:application"]
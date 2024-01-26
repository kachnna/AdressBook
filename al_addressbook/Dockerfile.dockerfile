FROM python:3.11-alpine

# Ustaw zmienną środowiskową APP_HOME
ENV APP_HOME /app

# Ustaw katalog roboczy na /my_contacts_addressbook
WORKDIR /my_contacts_addressbook

EXPOSE 5000

# Skopiuj pliki Pipfile oraz Pipfile.lock do obecnego katalogu
COPY Pipfile Pipfile.lock ./

# Zainstaluj pipenv i pakiety z Pipfile
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# Skopiuj całą zawartość do katalogu roboczego w kontenerze
COPY . .

# Uruchom główny plik aplikacji
CMD ["python", "book/main.py"]

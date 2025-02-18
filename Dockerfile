FROM python:3.9-slim-buster

# Installer les dépendances système pour ODBC et SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    ca-certificates

# Installer Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Installer le driver Microsoft ODBC (msodbcsql18)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 && \
    rm -rf /var/lib/apt/lists/*

# Installer python-dotenv pour charger le fichier .env
RUN pip install python-dotenv

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code dans l'image
COPY . .

# Exposer le port de l'application
EXPOSE 8001

# Démarrer l'application FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

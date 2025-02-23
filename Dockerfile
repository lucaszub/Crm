# Utiliser une image Python slim
FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc-dev \
    curl \
    apt-transport-https \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Installer le pilote ODBC pour SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application
EXPOSE 8001

# Démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

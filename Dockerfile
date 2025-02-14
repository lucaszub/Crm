FROM python:3.9-slim-buster

# Installer les dépendances système pour ODBC et SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    apt-transport-https \
    unixodbc \
    unixodbc-dev

# Installer le driver Microsoft ODBC (msodbcsql18)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 && \
    rm -rf /var/lib/apt/lists/*

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



# docker run -p 8001:8001 \
#   -e AZURE_CLIENT_ID=<votre_client_id> \
#   -e AZURE_TENANT_ID=5850cff6-c715-47ec-817a-e899a75ecd04 \
#   -e AZURE_CLIENT_SECRET=<votre_client_secret> \
#   fastapi-app



  docker run -p 8001:8001 `
  -e AZURE_CLIENT_ID=e97b3181-1988-4b98-a726-8c5bc5680cef `
  -e AZURE_TENANT_ID=5850cff6-c715-47ec-817a-e899a75ecd04 `
  -e AZURE_CLIENT_SECRET=secret-crm `
  fastapi-app


  az webapp create --name weatherapp --resource-group myResourceGroup --plan myAppServicePlan --deployment-container-image-name weatherapplucasz.azurecr.io/weatherapp:latest

FROM python:3.9-slim

WORKDIR /app

# Installer les paquets nécessaires pour compiler pyodbc et le pilote ODBC SQL Server
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    unixodbc-dev \
    curl \
    apt-transport-https \
    ca-certificates \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

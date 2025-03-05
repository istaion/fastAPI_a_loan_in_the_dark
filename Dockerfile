# Utiliser Python 3.12-slim comme image de base
FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    curl \
    apt-utils \
    gnupg2 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Ajouter les clés Microsoft pour SQL Server ODBC
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && \
    env ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Créer un environnement virtuel Python
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Variables d'environnement
ENV PYTHONUNBUFFERED 1
ENV ODBCINI=/etc/odbc.ini

# Installer Python3 et pip
RUN apt-get install -y python3 python3-pip

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copier tous les fichiers de l'application
COPY . /app/

# Vérifier les fichiers copiés (par exemple alembic.ini)
RUN ls -l /app

# Exposer le port 80
EXPOSE 80

# Commande pour démarrer l'application
CMD alembic upgrade head && python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 80



# FROM python:3.12-slim

# # Installer les dépendances nécessaires
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends build-essential \
#     curl \
#     apt-utils \
#     gnupg2 &&\
#     rm -rf /var/lib/apt/lists/* && \
#     pip install --upgrade pip

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# RUN apt-get update
# RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18

# # Créer un environnement virtuel
# RUN python3 -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Variables d'environnement
# ENV PYTHONUNBUFFERED 1
# ENV ODBCINI=/etc/odbc.ini

# # Installer Python et pip
# RUN apt-get install -y python3 python3-pip

# # Copier le fichier requirements.txt et installer les dépendances Python
# COPY requirements.txt /app/
# RUN pip install -r /app/requirements.txt

# # Copier l'application dans le conteneur
# COPY . /app/

# # Exposer le port 80
# EXPOSE 80


# RUN ls -l /app

# # Commande pour démarrer l'application
# CMD alembic upgrade head && python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 80


# FROM python:3.12-24.04_stable
# WORKDIR /app

# # Installer les dépendances nécessaires et le pilote ODBC
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     unixodbc \
#     unixodbc-dev \
#     curl \
#     wget \
#     apt-transport-https \
#     ca-certificates \
#     gnupg2 \
#     && wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && wget -qO- https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
#     && rm -rf /var/lib/apt/lists/*

# # Créer un environnement virtuel
# RUN python3 -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Variables d'environnement
# ENV PYTHONUNBUFFERED=1
# ENV ODBCINI=/etc/odbc.ini

# # Copier le fichier requirements.txt et installer les dépendances Python
# COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copier l'application dans le conteneur
# COPY . /app/

# # Exposer le port 80
# EXPOSE 80

# # Commande pour démarrer l'application
# CMD ["sh", "-c", "alembic upgrade head && python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 80"]
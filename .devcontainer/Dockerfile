FROM mcr.microsoft.com/devcontainers/python:3.11-node

# Rends root temporairement pour installer
USER root

# Installation de pip + venv de manière fiable
RUN apt-get update && apt-get install -y python3-venv && \
    python3 -m ensurepip && \
    python3 -m pip install --upgrade pip && \
    apt-get clean

# Reviens à l'utilisateur vscode par défaut
USER vscode

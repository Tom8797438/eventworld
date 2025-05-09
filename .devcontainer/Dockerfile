FROM mcr.microsoft.com/devcontainers/python:3.11-node

# Ajoute les permissions root et installe pip, venv, et autres outils essentiels
USER root
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv && \
    apt-get clean

# Reviens à l'utilisateur par défaut
USER vscode

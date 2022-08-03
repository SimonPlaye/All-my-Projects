"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "client",
    version = "0.1",
    description = "Ce programme vous dit bonjour",
    executables = [Executable("client.py")],
)
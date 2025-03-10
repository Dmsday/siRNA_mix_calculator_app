# utils/file_operations.py - Fonctions pour la gestion des fichiers
import os
from tkinter import filedialog


class FileOperations:
    """Classe pour les opérations de fichiers de l'application."""

    def __init__(self, root, logger):
        """Initialise les opérations de fichiers."""
        self.root = root
        self.logger = logger
        self.last_directory = os.path.expanduser("~")  # Dossier utilisateur par défaut

    def get_save_file_path(self, title="Enregistrer le fichier", filetypes=None):
        """
        Demande à l'utilisateur de choisir un chemin pour sauvegarder un fichier.

        Args:
            title: Titre de la boîte de dialogue
            filetypes: Liste des types de fichiers à afficher

        Returns:
            Le chemin du fichier choisi, ou None si l'utilisateur a annulé
        """
        if filetypes is None:
            filetypes = [("Tous les fichiers", "*.*")]

        file_path = filedialog.asksaveasfilename(
            initialdir=self.last_directory,
            title=title,
            filetypes=filetypes
        )

        if file_path:
            # Mettre à jour le dernier répertoire utilisé
            self.last_directory = os.path.dirname(file_path)
            self.logger.info(f"Chemin de sauvegarde sélectionné: {file_path}")
            return file_path

        return None

    def get_open_file_path(self, title="Ouvrir un fichier", filetypes=None):
        """
        Demande à l'utilisateur de choisir un fichier à ouvrir.

        Args:
            title: Titre de la boîte de dialogue
            filetypes: Liste des types de fichiers à afficher

        Returns:
            Le chemin du fichier choisi, ou None si l'utilisateur a annulé
        """
        if filetypes is None:
            filetypes = [("Tous les fichiers", "*.*")]

        file_path = filedialog.askopenfilename(
            initialdir=self.last_directory,
            title=title,
            filetypes=filetypes
        )

        if file_path:
            # Mettre à jour le dernier répertoire utilisé
            self.last_directory = os.path.dirname(file_path)
            self.logger.info(f"Fichier sélectionné pour ouverture: {file_path}")
            return file_path

        return None

    def get_directory_path(self, title="Sélectionner un dossier"):
        """
        Demande à l'utilisateur de choisir un dossier.

        Args:
            title: Titre de la boîte de dialogue

        Returns:
            Le chemin du dossier choisi, ou None si l'utilisateur a annulé
        """
        directory_path = filedialog.askdirectory(
            initialdir=self.last_directory,
            title=title
        )

        if directory_path:
            self.last_directory = directory_path
            self.logger.info(f"Dossier sélectionné: {directory_path}")
            return directory_path

        return None
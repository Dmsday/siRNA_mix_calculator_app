# main.py - Point d'entrée principal de l'application
import logging
import tkinter as tk
from tkinter import ttk

from app import SiRNAMixCalculator


def setup_logging():
    """Configure le système de journalisation global."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("sirna_calculator.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("SiRNACalculator")


def main():
    """Fonction principale pour démarrer l'application."""
    logger = setup_logging()
    logger.info("Démarrage de l'application SiRNA Mix Calculator")
    
    root = tk.Tk()
    
    # Configuration du thème
    style = ttk.Style()
    try:
        style.theme_use("clam")
        logger.info("Thème 'clam' appliqué avec succès")
    except tk.TclError:
        logger.warning("Le thème 'clam' n'est pas disponible, utilisation du thème par défaut")
    
    # Création de l'application
    app = SiRNAMixCalculator(root, logger)
    
    # Lancement de l'application
    root.mainloop()


if __name__ == "__main__":
    main()
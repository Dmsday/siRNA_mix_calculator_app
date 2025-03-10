# ui/action_frame.py - Cadre pour les boutons d'action
import tkinter as tk
from tkinter import ttk


class ActionFrame(ttk.Frame):
    """Cadre contenant les boutons d'action pour l'application."""

    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller
        self.logger = controller.logger

        # Configuration de la grille
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Crée les boutons d'action."""
        # Bouton Calculer
        self.btn_calculate = ttk.Button(
            self, text="Calculer",
            command=self.controller.perform_calculation
        )
        self.btn_calculate.grid(row=0, column=0, padx=5, sticky=tk.EW)

        # Bouton Expliquer
        self.btn_explain = ttk.Button(
            self, text="Expliquer le calcul",
            command=self.controller.explain_calculation
        )
        self.btn_explain.grid(row=0, column=1, padx=5, sticky=tk.EW)

        # Boutons supplémentaires pour charger/sauvegarder
        self.btn_save = ttk.Button(
            self, text="Sauvegarder config",
            command=self.controller.save_config
        )
        self.btn_save.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

        self.btn_load = ttk.Button(
            self, text="Charger config",
            command=self.controller.load_config
        )
        self.btn_load.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
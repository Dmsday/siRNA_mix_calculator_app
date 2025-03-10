# ui/history_frame.py - Cadre pour l'historique des calculs
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class HistoryFrame(ttk.Frame):
    """Cadre affichant l'historique des calculs précédents."""

    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller
        self.logger = controller.logger

        # Configuration de la grille
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Crée les widgets pour l'affichage de l'historique."""
        # Titre
        lbl_history = ttk.Label(self, text="Historique des calculs", font=("Helvetica", 12, "bold"))
        lbl_history.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)

        # Liste des calculs
        self.history_listbox = tk.Listbox(self, height=4)
        self.history_listbox.grid(row=1, column=0, sticky=tk.NSEW)

        # Scrollbar pour la liste
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.history_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)

        # Bouton pour charger un calcul depuis l'historique
        self.btn_load = ttk.Button(
            self, text="Charger le calcul sélectionné",
            command=self.load_selected_calculation
        )
        self.btn_load.grid(row=2, column=0, pady=(5, 0), sticky=tk.EW)

        # Double-clic pour charger un calcul
        self.history_listbox.bind("<Double-1>", lambda e: self.load_selected_calculation())

    def update_history(self, history):
        """Met à jour la liste de l'historique des calculs."""
        self.history_listbox.delete(0, tk.END)

        for item in reversed(history):  # Afficher les plus récents en premier
            timestamp = item['timestamp']
            inputs = item['inputs']

            # Créer un texte descriptif pour l'entrée d'historique
            description = f"{timestamp} - Cf: {inputs.get('Cf de siRNA désiré', '-')} nM, " \
                          f"Vol: {inputs.get('Volume du milieu', '-')} {inputs.get('volume_unit', 'µL')}"

            self.history_listbox.insert(tk.END, description)

    def load_selected_calculation(self):
        """Charge le calcul sélectionné dans l'interface principale."""
        selection = self.history_listbox.curselection()
        if not selection:
            return

        # Récupérer l'index dans l'historique (inversé car affiché en ordre inverse)
        history_index = len(self.controller.calculation_history) - 1 - selection[0]
        if 0 <= history_index < len(self.controller.calculation_history):
            history_item = self.controller.calculation_history[history_index]
            self.controller.load_from_history(history_item)
            self.logger.info(f"Calcul chargé depuis l'historique: {history_item['timestamp']}")
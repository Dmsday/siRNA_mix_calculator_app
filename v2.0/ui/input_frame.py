# ui/input_frame.py - Cadre pour les entrées utilisateur
import tkinter as tk
from tkinter import ttk

from ui.custom_widgets import SelectableLabel


class InputFrame(ttk.Frame):
    """Cadre contenant les champs d'entrée pour les paramètres de calcul."""
    
    # Constantes
    DEFAULT_VALUES = {
        "cf_culture": "1",
        "volume_culture": "2000",
        "mix_volume": "200",
        "stock_conc": "20000",
        "num_samples": "1"
    }
    
    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller
        self.logger = controller.logger
        
        # Variable pour mémoriser la dernière unité de volume
        self.last_unit = "µL"
        
        # Configuration de la grille pour ce frame
        self.columnconfigure(1, weight=1)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crée les widgets d'entrée."""
        # Titre général
        lbl_title = ttk.Label(self, text="Paramètres de dilution", font=("Helvetica", 12, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Section Milieu de culture
        lbl_milieu = ttk.Label(self, text="Milieu de culture", font=("Helvetica", 10, "bold"))
        lbl_milieu.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Concentration finale
        ttk.Label(self, text="Cf de siRNA désiré (nM) :", anchor="w").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.entry_cf_culture = ttk.Entry(self)
        self.entry_cf_culture.insert(0, self.DEFAULT_VALUES["cf_culture"])
        self.entry_cf_culture.grid(row=2, column=1, columnspan=2, pady=5, sticky=tk.EW)
        
        # Volume du milieu
        ttk.Label(self, text="Volume du milieu :", anchor="w").grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.entry_volume_culture = ttk.Entry(self)
        self.entry_volume_culture.insert(0, self.DEFAULT_VALUES["volume_culture"])
        self.entry_volume_culture.grid(row=3, column=1, pady=5, sticky=tk.EW)
        
        self.volume_unit = tk.StringVar(value="µL")
        self.combobox_unit = ttk.Combobox(
            self, textvariable=self.volume_unit, values=["µL", "mL"], 
            width=5, state="readonly"
        )
        self.combobox_unit.grid(row=3, column=2, padx=5, pady=5)
        self.combobox_unit.bind("<<ComboboxSelected>>", self.on_unit_change)
        
        # Section Mix siRNA
        lbl_mix = ttk.Label(self, text="Mix siRNA", font=("Helvetica", 10, "bold"))
        lbl_mix.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Volume du mix
        ttk.Label(self, text="Volume final du mix à mettre\n dans le milieu de culture (µL) :", 
                  anchor="w").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_mix_volume = ttk.Entry(self)
        self.entry_mix_volume.insert(0, self.DEFAULT_VALUES["mix_volume"])
        self.entry_mix_volume.grid(row=5, column=1, columnspan=2, pady=5, sticky=tk.EW)
        
        # Concentration du stock
        ttk.Label(self, text="Concentration du stock de siRNA (nM) :", 
                  anchor="w").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.entry_stock_conc = ttk.Entry(self)
        self.entry_stock_conc.insert(0, self.DEFAULT_VALUES["stock_conc"])
        self.entry_stock_conc.grid(row=6, column=1, columnspan=2, pady=5, sticky=tk.EW)
        
        # Section Nombre d'échantillons
        frame_samples = ttk.Frame(self)
        frame_samples.grid(row=7, column=0, columnspan=3, pady=(10, 5), sticky=tk.W)
        ttk.Label(frame_samples, text="Mix pour", anchor="w").grid(row=0, column=0)
        self.entry_num_samples = ttk.Entry(frame_samples, width=5)
        self.entry_num_samples.insert(0, self.DEFAULT_VALUES["num_samples"])
        self.entry_num_samples.grid(row=0, column=1, padx=5)
        ttk.Label(frame_samples, text="échantillon(s)", anchor="w").grid(row=0, column=2)
        
        # Zone de résultat pour la concentration dans le mix
        self.label_conc = SelectableLabel(self, text="")
        self.label_conc.grid(row=9, column=0, columnspan=3, pady=(5, 0), sticky=tk.W+tk.E)
        
        # Zone d'erreur
        self.label_error = SelectableLabel(self, text="")
        self.label_error.grid(row=10, column=0, columnspan=3, pady=(5, 0), sticky=tk.W+tk.E)
    
    def on_unit_change(self, event):
        """Convertit la valeur dans 'Volume du milieu' lors du changement d'unité, sans décimales."""
        try:
            current_value = self.entry_volume_culture.get().strip()
            if current_value == "":
                return
            value = float(current_value)
        except ValueError:
            self.logger.warning(f"Conversion d'unité: valeur non numérique '{current_value}'")
            return

        new_unit = self.volume_unit.get()
        if new_unit != self.last_unit:
            if self.last_unit == "µL" and new_unit == "mL":
                value = value / 1000
            elif self.last_unit == "mL" and new_unit == "µL":
                value = value * 1000
            self.entry_volume_culture.delete(0, tk.END)
            self.entry_volume_culture.insert(0, f"{value:.0f}")
            self.last_unit = new_unit
            self.logger.info(f"Unité changée de {self.last_unit} à {new_unit}, nouvelle valeur: {value:.0f}")
    
    def get_validated_inputs(self):
        """
        Vérifie que tous les champs sont remplis, numériques et > 0.
        Renvoie un dictionnaire des valeurs ou un message d'erreur.
        """
        inputs = [
            ("Cf de siRNA désiré (nM)", self.entry_cf_culture.get()),
            ("Volume du milieu", self.entry_volume_culture.get()),
            ("Volume final du mix à mettre dans le milieu de culture (µL)", self.entry_mix_volume.get()),
            ("Concentration du stock de siRNA (nM)", self.entry_stock_conc.get()),
            ("Nombre d'échantillon(s)", self.entry_num_samples.get())
        ]
        
        values = {}
        for label_text, text in inputs:
            if text.strip() == "":
                return f"Erreur : le champ '{label_text}' est vide."
            try:
                if label_text == "Nombre d'échantillon(s)":
                    val = int(text)
                else:
                    val = float(text)
            except ValueError:
                return f"Erreur : le champ '{label_text}' n'est pas un nombre valide."
            if val <= 0:
                return f"Erreur : le champ '{label_text}' doit être supérieur à 0."
            
            key = label_text.split(" (")[0]
            values[key] = val
        
        # Ajouter l'unité de volume
        values["volume_unit"] = self.volume_unit.get()
        
        return values
    
    def get_input_values(self):
        """Récupère les valeurs actuelles des champs sans validation."""
        return {
            "Cf de siRNA désiré": self.entry_cf_culture.get(),
            "Volume du milieu": self.entry_volume_culture.get(),
            "volume_unit": self.volume_unit.get(),
            "Volume final du mix à mettre dans le milieu de culture": self.entry_mix_volume.get(),
            "Concentration du stock de siRNA": self.entry_stock_conc.get(),
            "Nombre d'échantillon(s)": self.entry_num_samples.get()
        }
    
    def set_input_values(self, inputs):
        """Définit les valeurs des champs à partir d'un dictionnaire."""
        if "Cf de siRNA désiré" in inputs:
            self.entry_cf_culture.delete(0, tk.END)
            self.entry_cf_culture.insert(0, inputs["Cf de siRNA désiré"])
        
        if "Volume du milieu" in inputs:
            self.entry_volume_culture.delete(0, tk.END)
            self.entry_volume_culture.insert(0, inputs["Volume du milieu"])
        
        if "volume_unit" in inputs:
            self.volume_unit.set(inputs["volume_unit"])
            self.last_unit = inputs["volume_unit"]
        
        if "Volume final du mix à mettre dans le milieu de culture" in inputs:
            self.entry_mix_volume.delete(0, tk.END)
            self.entry_mix_volume.insert(0, inputs["Volume final du mix à mettre dans le milieu de culture"])
        
        if "Concentration du stock de siRNA" in inputs:
            self.entry_stock_conc.delete(0, tk.END)
            self.entry_stock_conc.insert(0, inputs["Concentration du stock de siRNA"])
        
        if "Nombre d'échantillon(s)" in inputs:
            self.entry_num_samples.delete(0, tk.END)
            self.entry_num_samples.insert(0, inputs["Nombre d'échantillon(s)"])
    
    def update_concentration(self, concentration):
        """Met à jour l'affichage de la concentration."""
        self.label_conc.update_text(f"Concentration en siRNA dans le mix : {concentration:.2f} nM", "black")
    
    def update_error(self, error_message):
        """Met à jour l'affichage du message d'erreur."""
        self.logger.warning(f"Erreur de validation: {error_message}")
        self.label_error.update_text(error_message, "red")
    
    def clear_error(self):
        """Efface le message d'erreur."""
        self.label_error.update_text("", "red")
# app.py - Classe principale de l'application
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

from ui.input_frame import InputFrame
from ui.table_frame import TableFrame
from ui.action_frame import ActionFrame
from ui.history_frame import HistoryFrame
from ui.custom_widgets import ToolTip
from models.calculation import SiRNACalculation
from utils.file_operations import FileOperations


class SiRNAMixCalculator:
    """Classe principale de l'application SiRNA Mix Calculator."""
    
    def __init__(self, root, logger):
        self.root = root
        self.logger = logger
        self.root.title("Calculateur de Mix siRNA")
        self.root.geometry("800x780")
        self.root.minsize(600, 700)
        
        # Configuration de la grille principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)  # Table obtient plus d'espace
        
        # Initialisation du modèle de calcul
        self.calculation_model = SiRNACalculation(logger)
        
        # Initialisation de l'historique
        self.calculation_history = []
        
        # Initialisation des utilitaires
        self.file_ops = FileOperations(self.root, logger)
        
        # Création des composants UI
        self.create_ui()
        
        # Initialisation des tooltips
        self.setup_tooltips()
        
        self.logger.info("Application initialisée avec succès")
    
    def create_ui(self):
        """Crée tous les composants de l'interface utilisateur."""
        # Panneau d'entrée (en haut)
        self.input_frame = InputFrame(self.root, self)
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Panneau d'action (juste en-dessous des entrées)
        self.action_frame = ActionFrame(self.root, self)
        self.action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Panneau de résultats (tableau - milieu)
        self.table_frame = TableFrame(self.root, self)
        self.table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        # Panneau d'historique (en bas)
        self.history_frame = HistoryFrame(self.root, self)
        self.history_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
    
    def setup_tooltips(self):
        """Configure les info-bulles pour les champs principaux."""
        tooltips = {
            self.input_frame.entry_cf_culture: "Concentration finale désirée pour le siRNA dans la culture (nM)",
            self.input_frame.entry_volume_culture: "Volume total du milieu de culture",
            self.input_frame.combobox_unit: "Unité de volume (µL ou mL)",
            self.input_frame.entry_mix_volume: "Volume total du mix siRNA à ajouter au milieu de culture",
            self.input_frame.entry_stock_conc: "Concentration du stock de siRNA (nM)",
            self.input_frame.entry_num_samples: "Nombre d'échantillons pour lesquels préparer le mix",
            self.action_frame.btn_calculate: "Effectuer le calcul avec les valeurs actuelles",
            self.action_frame.btn_explain: "Afficher les explications détaillées du calcul"
        }
        
        for widget, text in tooltips.items():
            ToolTip(widget, text)
    
    def perform_calculation(self):
        """Effectue le calcul principal et met à jour l'interface."""
        try:
            # Récupération et validation des entrées
            input_values = self.input_frame.get_validated_inputs()
            if isinstance(input_values, str):
                # Erreur de validation
                self.input_frame.update_error(input_values)
                return False
            
            # Exécution du calcul
            calculation_result = self.calculation_model.calculate_mix(input_values)
            if not calculation_result['success']:
                self.input_frame.update_error(calculation_result['error'])
                return False
            
            # Mise à jour de l'interface avec les résultats
            self.input_frame.update_concentration(calculation_result['ci_mix'])
            self.input_frame.clear_error()
            self.table_frame.update_table(calculation_result['data'])
            
            # Ajout du calcul à l'historique
            self.add_to_history(input_values, calculation_result)
            
            self.logger.info("Calcul effectué avec succès")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul: {str(e)}", exc_info=True)
            self.input_frame.update_error(f"Erreur inattendue: {str(e)}")
            return False
    
    def explain_calculation(self):
        """Affiche une explication détaillée des calculs effectués."""
        try:
            # Récupération des entrées
            input_values = self.input_frame.get_validated_inputs()
            if isinstance(input_values, str):
                # Erreur de validation
                self.input_frame.update_error(input_values)
                return
            
            # Génération de l'explication
            explanation = self.calculation_model.generate_explanation(input_values)
            
            # Affichage de l'explication dans une nouvelle fenêtre
            self._show_explanation_window(explanation)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération de l'explication: {str(e)}", exc_info=True)
            messagebox.showerror("Erreur", f"Impossible de générer l'explication: {str(e)}")
    
    def _show_explanation_window(self, explanation):
        """Affiche une fenêtre avec l'explication détaillée des calculs."""
        explanation_window = tk.Toplevel(self.root)
        explanation_window.title("Explication du calcul")
        explanation_window.geometry("600x500")
        explanation_window.minsize(500, 400)
        
        # Configuration de la grille
        explanation_window.columnconfigure(0, weight=1)
        explanation_window.rowconfigure(0, weight=1)
        
        # Création du widget de texte avec défilement
        frame = ttk.Frame(explanation_window, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        text_widget = tk.Text(frame, wrap="word", padx=10, pady=10)
        text_widget.grid(row=0, column=0, sticky="nsew")
        text_widget.insert("1.0", explanation)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Bouton de fermeture
        btn_close = ttk.Button(explanation_window, text="Fermer", command=explanation_window.destroy)
        btn_close.grid(row=1, column=0, pady=10)
    
    def add_to_history(self, inputs, result):
        """Ajoute un calcul à l'historique."""
        timestamp = self.calculation_model.get_timestamp()
        history_entry = {
            'timestamp': timestamp,
            'inputs': inputs,
            'result': result
        }
        self.calculation_history.append(history_entry)
        
        # Mettre à jour l'affichage de l'historique
        self.history_frame.update_history(self.calculation_history)
        
        self.logger.info(f"Calcul ajouté à l'historique: {timestamp}")
    
    def load_from_history(self, history_item):
        """Charge les valeurs d'un calcul historique dans l'interface."""
        try:
            inputs = history_item['inputs']
            self.input_frame.set_input_values(inputs)
            
            # Recalculer pour mettre à jour l'affichage
            self.perform_calculation()
            
            self.logger.info(f"Valeurs chargées depuis l'historique: {history_item['timestamp']}")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement depuis l'historique: {str(e)}", exc_info=True)
            messagebox.showerror("Erreur", f"Impossible de charger les données: {str(e)}")
    
    def save_config(self):
        """Sauvegarde la configuration actuelle dans un fichier."""
        try:
            inputs = self.input_frame.get_input_values()
            
            file_path = self.file_ops.get_save_file_path("Sauvegarder la configuration", 
                                                         filetypes=[("Fichier JSON", "*.json"), 
                                                                    ("Tous les fichiers", "*.*")])
            if not file_path:
                return
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(inputs, f, indent=4)
            
            messagebox.showinfo("Succès", f"Configuration sauvegardée dans {file_path}")
            self.logger.info(f"Configuration sauvegardée dans {file_path}")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la configuration: {str(e)}", exc_info=True)
            messagebox.showerror("Erreur", f"Impossible de sauvegarder la configuration: {str(e)}")
    
    def load_config(self):
        """Charge une configuration depuis un fichier."""
        try:
            file_path = self.file_ops.get_open_file_path("Charger une configuration", 
                                                         filetypes=[("Fichier JSON", "*.json"), 
                                                                    ("Tous les fichiers", "*.*")])
            if not file_path:
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                inputs = json.load(f)
            
            self.input_frame.set_input_values(inputs)
            messagebox.showinfo("Succès", f"Configuration chargée depuis {file_path}")
            self.logger.info(f"Configuration chargée depuis {file_path}")
            
        except json.JSONDecodeError:
            self.logger.error(f"Format de fichier JSON invalide: {file_path}", exc_info=True)
            messagebox.showerror("Erreur", "Le fichier n'est pas un fichier JSON valide.")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la configuration: {str(e)}", exc_info=True)
            messagebox.showerror("Erreur", f"Impossible de charger la configuration: {str(e)}")
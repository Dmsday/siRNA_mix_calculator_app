# ui/table_frame.py - Cadre pour le tableau de résultats
import tkinter as tk
from tkinter import ttk, messagebox


class TableFrame(ttk.Frame):
    """Cadre contenant le tableau des résultats de calcul."""

    # Colonnes du tableau
    COLUMNS = ("Composant", "Volume par échantillon (µL)", "Volume total (µL)")

    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller
        self.logger = controller.logger

        # Variables pour la sélection et le glissement
        self.drag_start_index = None
        self.current_cell = None

        # Configuration de la grille
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # Le tableau prend tout l'espace disponible

        self.create_widgets()

    def create_widgets(self):
        """Crée le tableau et ses composants associés."""
        # Titre
        lbl_table = ttk.Label(self, text="Tableau du mix", font=("Helvetica", 12, "bold"))
        lbl_table.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Création du tableau avec Treeview
        self.tree = ttk.Treeview(self, columns=self.COLUMNS, show="headings", height=6)

        # Configuration des colonnes
        for i, col in enumerate(self.COLUMNS):
            self.tree.heading(col, text=col)
            # Largeur proportionnelle selon le contenu attendu
            if i == 0:  # Composant
                width = 160
            else:  # Valeurs numériques
                width = 140
            self.tree.column(col, width=width, anchor="center")

        # Placement du tableau avec scrollbar
        self.tree.grid(row=1, column=0, sticky=tk.NSEW)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set, selectmode="extended")

        # Association des événements
        self.tree.bind("<ButtonPress-1>", self.on_tree_button_press)
        self.tree.bind("<B1-Motion>", self.on_tree_motion)
        self.tree.bind("<Button-3>", self.on_tree_right_click)

    def update_table(self, data):
        """Met à jour le contenu du tableau avec les nouvelles données."""
        # Effacer les données existantes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insérer les nouvelles données
        for row in data:
            self.tree.insert("", tk.END, values=row)

        self.logger.debug(f"Tableau mis à jour avec {len(data)} lignes")

    def on_tree_button_press(self, event):
        """Gère l'événement de clic sur le tableau."""
        rowid = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if rowid and col:
            self.drag_start_index = self.tree.index(rowid)
            self.current_cell = (rowid, col)
            self.tree.selection_set(rowid)
        else:
            self.drag_start_index = None
            self.current_cell = None

    def on_tree_motion(self, event):
        """Gère l'événement de glissement sur le tableau."""
        if self.drag_start_index is None:
            return

        rowid = self.tree.identify_row(event.y)
        if rowid:
            current_index = self.tree.index(rowid)
            children = self.tree.get_children()

            # Sélectionner les lignes entre le début et la fin du glissement
            start = min(self.drag_start_index, current_index)
            end = max(self.drag_start_index, current_index)
            items_to_select = children[start:end + 1]

            # Effacer et redéfinir la sélection
            self.tree.selection_remove(self.tree.selection())
            for item in items_to_select:
                self.tree.selection_add(item)

    def on_tree_right_click(self, event):
        """Gère le clic droit sur le tableau pour afficher un menu contextuel."""
        selection = self.tree.selection()

        if selection:
            if len(selection) == 1 and self.current_cell is not None:
                # Clic sur une cellule spécifique
                rowid, col = self.current_cell
                col_index = int(col.replace("#", "")) - 1
                cell_value = self.tree.item(rowid)['values'][col_index]

                self._show_context_menu(event, "cell", cell_value)
            else:
                # Plusieurs lignes sélectionnées
                self._show_context_menu(event, "selection")
        else:
            # Clic en dehors d'une sélection
            region = self.tree.identify("region", event.x, event.y)

            if region == "cell":
                # Clic sur une cellule (sans sélection préalable)
                rowid = self.tree.identify_row(event.y)
                col = self.tree.identify_column(event.x)

                if rowid and col:
                    self.current_cell = (rowid, col)
                    col_index = int(col.replace("#", "")) - 1
                    cell_value = self.tree.item(rowid)['values'][col_index]

                    self._show_context_menu(event, "cell", cell_value)

            elif region == "heading":
                # Clic sur un en-tête de colonne
                col = self.tree.identify_column(event.x)

                if col:
                    # Ajout du menu pour la colonne
                    self._show_context_menu(event, "heading", col)

    def _show_context_menu(self, event, menu_type, value=None):
        """Affiche un menu contextuel basé sur le type de clic."""
        menu = tk.Menu(self, tearoff=0)

        if menu_type == "cell":
            # Menu pour une cellule
            menu.add_command(label=f"Copier la valeur",
                             command=lambda: self._copy_to_clipboard(value))

        elif menu_type == "selection":
            # Menu pour une sélection
            menu.add_command(label="Copier la sélection",
                             command=self._copy_selection)

        elif menu_type == "heading":
            # Menu pour un en-tête de colonne
            col_index = int(value.replace("#", "")) - 1
            col_name = self.COLUMNS[col_index]
            menu.add_command(label=f"Copier tous les '{col_name}'",
                             command=lambda: self._copy_column(col_index))

        # Affichage du menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            # Nettoyage
            menu.grab_release()

    def _copy_to_clipboard(self, value):
        """Copie une valeur dans le presse-papier."""
        self.clipboard_clear()
        self.clipboard_append(str(value))
        self.logger.info(f"Valeur copiée dans le presse-papier: {value}")

    def _copy_selection(self):
        """Copie les valeurs des lignes sélectionnées dans le presse-papier."""
        selection = self.tree.selection()
        if not selection:
            return

        # Extraction des valeurs
        values = []
        for item in selection:
            values.append("\t".join(str(x) for x in self.tree.item(item)['values']))

        # Création d'un texte tabulé
        text = "\n".join(values)

        # Copie dans le presse-papier
        self.clipboard_clear()
        self.clipboard_append(text)
        self.logger.info(f"Sélection copiée dans le presse-papier ({len(selection)} lignes)")

    def _copy_column(self, col_index):
        """Copie toutes les valeurs d'une colonne dans le presse-papier."""
        values = []
        for item in self.tree.get_children():
            row_values = self.tree.item(item)['values']
            if col_index < len(row_values):
                values.append(str(row_values[col_index]))

        # Création d'un texte
        text = "\n".join(values)

        # Copie dans le presse-papier
        self.clipboard_clear()
        self.clipboard_append(text)
        self.logger.info(f"Colonne '{self.COLUMNS[col_index]}' copiée dans le presse-papier")
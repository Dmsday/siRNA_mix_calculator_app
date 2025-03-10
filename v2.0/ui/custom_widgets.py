# ui/custom_widgets.py - Widgets personnalisés pour l'interface
import tkinter as tk
from tkinter import ttk


class SelectableLabel(ttk.Frame):
    """Label avec texte sélectionnable et copiable."""

    def __init__(self, parent, text="", foreground="black", **kwargs):
        super().__init__(parent, **kwargs)

        # Configuration de la grille
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Obtenir la couleur d'arrière-plan du thème actuel ou utiliser une valeur par défaut
        try:
            bg_color = parent.winfo_toplevel().tk.call('ttk::style', 'lookup', 'TFrame', '-background')
            if not bg_color:
                bg_color = "white"  # Valeur par défaut si non trouvée
        except:
            bg_color = "white"  # Fallback en cas d'erreur

        # Création d'un widget Text pour permettre la sélection
        self.text_widget = tk.Text(self, height=1, wrap="word",
                                   background=bg_color,
                                   borderwidth=0, highlightthickness=0)
        self.text_widget.grid(row=0, column=0, sticky="ew")

        # Insertion du texte initial
        self.text_widget.insert("1.0", text)
        self.text_widget.config(state="disabled", foreground=foreground)

        # Mise à jour de la hauteur en fonction du contenu
        self.update_height()

    def update_text(self, text, foreground="black"):
        """Met à jour le texte du label."""
        self.text_widget.config(state="normal", foreground=foreground)
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)
        self.text_widget.config(state="disabled")
        self.update_height()

    def update_height(self):
        """Ajuste la hauteur du widget en fonction du contenu."""
        num_lines = self.text_widget.get("1.0", "end").count('\n')
        if num_lines == 0:
            num_lines = 1
        self.text_widget.configure(height=num_lines)


class ToolTip:
    """Affiche une info-bulle lorsque la souris survole un widget."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        # Liaison des événements
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Affiche l'info-bulle."""
        # Calcul de la position
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Création de la fenêtre de l'info-bulle
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Fenêtre sans bordure
        tw.wm_geometry(f"+{x}+{y}")

        # Création du label
        label = ttk.Label(tw, text=self.text, background="#FFFFDD",
                          relief="solid", borderwidth=1, padding=(3, 2))
        label.pack()

    def hide_tip(self, event=None):
        """Cache l'info-bulle."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
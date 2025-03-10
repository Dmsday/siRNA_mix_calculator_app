# models/calculation.py - Modèle pour les calculs de mix siRNA
import datetime


class SiRNACalculation:
    """Classe pour effectuer les calculs de mix siRNA."""

    def __init__(self, logger):
        """Initialise le modèle de calcul."""
        self.logger = logger

    def calculate_mix(self, inputs):
        """
        Calcule les volumes pour un mix siRNA.

        Args:
            inputs: Dictionnaire contenant les valeurs d'entrée
                - 'Cf de siRNA désiré': concentration finale désirée (nM)
                - 'Volume du milieu': volume total du milieu de culture
                - 'volume_unit': unité du volume (µL ou mL)
                - 'Volume final du mix à mettre dans le milieu de culture': volume du mix (µL)
                - 'Concentration du stock de siRNA': concentration du stock (nM)
                - 'Nombre d'échantillon(s)': nombre d'échantillons

        Returns:
            Dictionnaire contenant:
                - 'success': booléen indiquant si le calcul a réussi
                - 'error': message d'erreur en cas d'échec
                - 'data': tableau des valeurs calculées pour chaque composant
                - 'ci_mix': concentration initiale du mix
        """
        try:
            # Extraction des valeurs d'entrée
            cf = inputs['Cf de siRNA désiré']  # Concentration finale désirée (nM)
            v_milieu = inputs['Volume du milieu']  # Volume du milieu (µL ou mL)
            v_mix = inputs['Volume final du mix à mettre dans le milieu de culture']  # Volume du mix (µL)
            c_stock = inputs['Concentration du stock de siRNA']  # Concentration du stock (nM)
            n_samples = int(inputs['Nombre d\'échantillon(s)'])  # Nombre d'échantillons

            # Conversion du volume du milieu en µL si nécessaire
            if inputs['volume_unit'] == 'mL':
                v_milieu = v_milieu * 1000

            # Calcul de la concentration initiale du mix
            ci_mix = (cf * v_milieu) / v_mix

            # Vérification de la faisabilité
            if ci_mix > c_stock:
                return {
                    'success': False,
                    'error': f"La concentration requise dans le mix ({ci_mix:.2f} nM) est supérieure à la concentration stock ({c_stock} nM). Augmentez le volume du mix ou diminuez la concentration finale désirée."
                }

            # Calcul du volume de siRNA stock à utiliser par échantillon
            v_sirna = (ci_mix * v_mix) / c_stock

            # Calcul du volume de tampon par échantillon
            v_buffer = v_mix - v_sirna

            # Calcul des volumes totaux pour tous les échantillons
            v_sirna_total = v_sirna * n_samples
            v_buffer_total = v_buffer * n_samples
            v_mix_total = v_mix * n_samples

            # Préparation des données pour l'affichage
            data = [
                ("siRNA", f"{v_sirna:.2f}", f"{v_sirna_total:.2f}"),
                ("Tampon", f"{v_buffer:.2f}", f"{v_buffer_total:.2f}"),
                ("Mix total", f"{v_mix:.2f}", f"{v_mix_total:.2f}")
            ]

            return {
                'success': True,
                'data': data,
                'ci_mix': ci_mix
            }

        except Exception as e:
            self.logger.error(f"Erreur dans le calcul du mix: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': f"Erreur de calcul: {str(e)}"
            }

    def generate_explanation(self, inputs):
        """
        Génère une explication détaillée des calculs pour les valeurs d'entrée données.

        Args:
            inputs: Dictionnaire contenant les valeurs d'entrée

        Returns:
            Texte explicatif des calculs
        """
        try:
            # Extraction des valeurs d'entrée
            cf = inputs['Cf de siRNA désiré']  # Concentration finale désirée (nM)
            v_milieu = inputs['Volume du milieu']  # Volume du milieu (µL ou mL)
            v_mix = inputs['Volume final du mix à mettre dans le milieu de culture']  # Volume du mix (µL)
            c_stock = inputs['Concentration du stock de siRNA']  # Concentration du stock (nM)
            n_samples = int(inputs['Nombre d\'échantillon(s)'])  # Nombre d'échantillons
            volume_unit = inputs['volume_unit']  # Unité de volume

            # Conversion du volume du milieu en µL si nécessaire
            v_milieu_ul = v_milieu
            if volume_unit == 'mL':
                v_milieu_ul = v_milieu * 1000

            # Calcul de la concentration initiale du mix
            ci_mix = (cf * v_milieu_ul) / v_mix

            # Calcul du volume de siRNA stock à utiliser par échantillon
            v_sirna = (ci_mix * v_mix) / c_stock

            # Calcul du volume de tampon par échantillon
            v_buffer = v_mix - v_sirna

            # Calcul des volumes totaux pour tous les échantillons
            v_sirna_total = v_sirna * n_samples
            v_buffer_total = v_buffer * n_samples
            v_mix_total = v_mix * n_samples

            # Génération de l'explication
            explanation = f"""
Explication détaillée du calcul de mix siRNA:

Valeurs d'entrée:
- Concentration finale (Cf) de siRNA désirée dans la culture: {cf} nM
- Volume du milieu de culture: {v_milieu} {volume_unit} ({v_milieu_ul} µL)
- Volume final du mix à ajouter au milieu: {v_mix} µL
- Concentration du stock de siRNA: {c_stock} nM
- Nombre d'échantillons: {n_samples}

Équations utilisées:
1) Pour calculer la concentration initiale requise dans le mix (Ci):
   Ci = (Cf * Vmilieu) / Vmix
   Ci = ({cf} nM * {v_milieu_ul} µL) / {v_mix} µL
   Ci = {ci_mix:.2f} nM

2) Pour calculer le volume de siRNA stock nécessaire:
   VsiRNA = (Ci * Vmix) / Cstock
   VsiRNA = ({ci_mix:.2f} nM * {v_mix} µL) / {c_stock} nM
   VsiRNA = {v_sirna:.2f} µL par échantillon
   Volume total de siRNA pour {n_samples} échantillon(s): {v_sirna_total:.2f} µL

3) Pour calculer le volume de tampon nécessaire:
   Vtampon = Vmix - VsiRNA
   Vtampon = {v_mix} µL - {v_sirna:.2f} µL
   Vtampon = {v_buffer:.2f} µL par échantillon
   Volume total de tampon pour {n_samples} échantillon(s): {v_buffer_total:.2f} µL

4) Volume total du mix pour {n_samples} échantillon(s):
   Vmix_total = {v_mix} µL * {n_samples} = {v_mix_total:.2f} µL

Instructions pour la préparation:
1. Dans un tube, mélanger {v_sirna_total:.2f} µL de solution stock de siRNA ({c_stock} nM)
2. Ajouter {v_buffer_total:.2f} µL de tampon
3. Mélanger doucement par pipetage
4. Ajouter {v_mix} µL de ce mix à chaque échantillon de milieu de culture

La concentration finale de siRNA dans chaque échantillon sera de {cf} nM.
"""

            return explanation

        except Exception as e:
            self.logger.error(f"Erreur dans la génération de l'explication: {str(e)}", exc_info=True)
            return f"Erreur lors de la génération de l'explication: {str(e)}"

    def get_timestamp(self):
        """Renvoie un horodatage formaté pour l'historique."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
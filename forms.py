from django import forms

class WallPaintCalculatorForm(forms.Form):
    PRODUCT_CHOICES = []
    product = forms.ChoiceField(choices=PRODUCT_CHOICES, label="Choose product", initial="weathershield")
    perimeter = forms.DecimalField(label="Perimeter (m): ", decimal_places=3, max_digits=10)
    height = forms.DecimalField(label="Height (m):", decimal_places=3, max_digits=10)
    sq_per_litre = forms.DecimalField(label="m2 per litre: ", decimal_places=1, max_digits=5, min_value=0.1, initial=16)
    num_coats = forms.DecimalField(label="Number of coats: ", decimal_places=0, max_digits=2, initial=2)

class FlooringCalculatorForm(forms.Form):
    length = forms.DecimalField(label="Length (m)", decimal_places=3, max_digits=10)
    width = forms.DecimalField(label="Length (m)", decimal_places=3, max_digits=10)
    cost_per_sq = forms.DecimalField(label="Cost per square metre: $", decimal_places=2, max_digits=7)
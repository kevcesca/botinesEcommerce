from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'label'
    
    class Meta:
        model = Producto
        fields = '__all__'  # Para incluir todos los campos del modelo en el formulario

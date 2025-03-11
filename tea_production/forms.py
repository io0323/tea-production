from django import forms
from .models import Production, Shipment

class ProductionForm(forms.ModelForm):
    """
    生産データ登録フォーム
    """
    class Meta:
        model = Production
        fields = ['tea_type', 'production_date', 'quantity', 'quality_check', 'quality_notes']
        widgets = {
            'production_date': forms.DateInput(attrs={'type': 'date'}),
            'quality_notes': forms.Textarea(attrs={'rows': 3}),
        }

class ShipmentForm(forms.ModelForm):
    """
    出荷データ登録フォーム
    """
    class Meta:
        model = Shipment
        fields = ['production', 'shipment_date', 'quantity', 'customer_name', 'customer_contact']
        widgets = {
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 在庫があるものだけを選択肢として表示
        self.fields['production'].queryset = Production.objects.filter(
            inventory__quantity__gt=0
        ) 
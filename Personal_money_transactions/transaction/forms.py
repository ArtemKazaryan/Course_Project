from django.forms import ModelForm
from .models import ProfitableTransaction, ExpenditureTransaction

class ProfitableTransactionForm(ModelForm):
    class Meta:
        model = ProfitableTransaction
        fields = ['date', 'income_type', 'name', 'description', 'amount']
        


class ExpenditureTransactionForm(ModelForm):
    class Meta:
        model = ExpenditureTransaction
        fields = ['date', 'category', 'name', 'description', 'meter', 'meter_quantity', 'price_per_meter_unit']











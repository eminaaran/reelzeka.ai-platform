from django import forms
from core.models import Topic

class TestWizardForm(forms.Form):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Konular",
        help_text="Hangi konulardan sorular seçilsin?"
    )
    num_questions = forms.IntegerField(
        min_value=1,
        label="Soru Sayısı",
        help_text="Teste eklenecek toplam soru sayısı."
    )
    # İleri seviye: Zorluk dağılımı
    easy_percentage = forms.IntegerField(
        min_value=0, max_value=100, label="Kolay Soru Yüzdesi (%)", initial=50
    )
    medium_percentage = forms.IntegerField(
        min_value=0, max_value=100, label="Orta Soru Yüzdesi (%)", initial=30
    )
    hard_percentage = forms.IntegerField(
        min_value=0, max_value=100, label="Zor Soru Yüzdesi (%)", initial=20
    )

    def clean(self):
        cleaned_data = super().clean()
        easy = cleaned_data.get("easy_percentage", 0)
        medium = cleaned_data.get("medium_percentage", 0)
        hard = cleaned_data.get("hard_percentage", 0)

        if easy + medium + hard != 100:
            raise forms.ValidationError("Zorluk yüzdelerinin toplamı 100 olmalıdır.")

        return cleaned_data

from django import forms
from .models import Animal
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class AnimalForm(forms.ModelForm):
    remover_foto = forms.BooleanField(required=False, label="Remover foto atual")

    class Meta:
        model = Animal
        fields = ["nome", "descricao", "foto", "status", "data_chegada", "data_saida"]
        widgets = {
            "foto": forms.FileInput(attrs={"class": "form-control shadow-sm"}),
            "data_chegada": forms.DateInput(
                attrs={"class": "form-control shadow-sm", "type": "date"},
                format="%Y-%m-%d"
            ),
            "data_saida": forms.DateInput(
                attrs={"class": "form-control shadow-sm", "type": "date"},
                format="%Y-%m-%d"
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["data_chegada"].input_formats = ["%Y-%m-%d"]
            self.fields["data_saida"].input_formats = ["%Y-%m-%d"]

        def clean_foto(self):
            foto = self.cleaned_data.get("foto")

            if not foto:
                return foto

            img = Image.open(foto)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((1200, 1200))

            output = BytesIO()
            img.save(output, format="JPEG", quality=75, optimize=True)
            output.seek(0)

            if output.getbuffer().nbytes >= foto.size:
                foto.seek(0)
                return foto

            nome_base, _ = os.path.splitext(foto.name)
            novo_nome = f"{nome_base}.jpg"

            foto_comprimida = InMemoryUploadedFile(
                file=output,
                field_name="foto",
                name=novo_nome,
                content_type="image/jpeg",
                size=output.getbuffer().nbytes,
                charset=None,
            )

            return foto_comprimida
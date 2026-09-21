from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token

from .models import Propietario, Mascota
from .serializers import MascotaSerializer, ConsultaVeterinariaSerializer


class ClinicaTests(TestCase):
    def setUp(self):
        self.propietario = Propietario.objects.create(
            identificacion="999",
            nombre="Propietario de prueba",
            telefono="8888-9999"
        )

        self.mascota = Mascota.objects.create(
            nombre="Mascota de prueba",
            especie="Perro",
            raza="Mestizo",
            fecha_nacimiento=date(2022, 1, 1),
            peso="10.00",
            activo=True,
            propietario=self.propietario
        )

    def test_serializer_mascota_rechaza_peso_cero(self):
        serializer = MascotaSerializer(data={
            "nombre": "Firulais",
            "especie": "Perro",
            "raza": "Mestizo",
            "fecha_nacimiento": "2023-01-01",
            "peso": "0.00",
            "activo": True,
            "propietario": self.propietario.id
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("peso", serializer.errors)

    def test_serializer_consulta_rechaza_costo_negativo(self):
        serializer = ConsultaVeterinariaSerializer(data={
            "mascota": self.mascota.id,
            "motivo": "Consulta de prueba",
            "diagnostico": "Sin diagnóstico",
            "tratamiento": "Sin tratamiento",
            "costo": "-100.00"
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("costo", serializer.errors)

    def test_perfil_anonimo_es_rechazado(self):
        response = self.client.get("/clinica/api/perfil/")

        self.assertEqual(response.status_code, 401)

    def test_perfil_autenticado_responde_200(self):
        User = get_user_model()

        usuario = User.objects.create_user(
            username="usuario_prueba",
            password="clave_segura_123"
        )

        token = Token.objects.create(user=usuario)

        response = self.client.get(
            "/clinica/api/perfil/",
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "usuario_prueba")
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.core.paginator import Paginator

from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from .models import Propietario, Mascota, ConsultaVeterinaria
from .serializers import (
    PropietarioSerializer,
    MascotaSerializer,
    ConsultaVeterinariaSerializer,
)


def inicio(request):
    return HttpResponse("API de Gestión Veterinaria activa")


@api_view(["GET", "POST"])
def api_mascotas(request):
    if request.method == "GET":
        mascotas = Mascota.objects.all().order_by("id")

        especie = request.query_params.get("especie")
        activas = request.query_params.get("activas")
        propietario = request.query_params.get("propietario")

        if especie:
            mascotas = mascotas.filter(especie=especie)

        if activas is not None:
            if activas.lower() == "true":
                mascotas = mascotas.filter(activo=True)
            elif activas.lower() == "false":
                mascotas = mascotas.filter(activo=False)

        if propietario:
            mascotas = mascotas.filter(propietario_id=propietario)

        paginator = Paginator(mascotas, 5)
        numero_pagina = request.query_params.get("page", 1)
        pagina = paginator.get_page(numero_pagina)

        serializer = MascotaSerializer(pagina, many=True)

        return Response({
            "pagina_actual": pagina.number,
            "total_paginas": paginator.num_pages,
            "total_mascotas": paginator.count,
            "resultados": serializer.data
        })

    serializer = MascotaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def detalle_mascota(request, pk):
    try:
        mascota = Mascota.objects.get(pk=pk)
    except Mascota.DoesNotExist:
        return Response(
            {"error": "Mascota no encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = MascotaSerializer(
            mascota,
            data=request.data,
            partial=(request.method == "PATCH")
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    mascota.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def api_propietarios(request):
    if request.method == "GET":
        propietarios = Propietario.objects.all().order_by("id")
        serializer = PropietarioSerializer(propietarios, many=True)
        return Response(serializer.data)

    serializer = PropietarioSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "POST"])
def api_consultas(request):
    if request.method == "GET":
        consultas = ConsultaVeterinaria.objects.all().order_by("id")
        serializer = ConsultaVeterinariaSerializer(consultas, many=True)
        return Response(serializer.data)

    serializer = ConsultaVeterinariaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def estadisticas(request):
    return Response({
        "total_propietarios": Propietario.objects.count(),
        "total_mascotas": Mascota.objects.count(),
        "mascotas_activas": Mascota.objects.filter(activo=True).count(),
        "total_consultas": ConsultaVeterinaria.objects.count(),
    })
    
@api_view(["GET"])
def contador_sesion(request):
    visitas = request.session.get("visitas", 0) + 1
    request.session["visitas"] = visitas

    return Response({
        "visitas": visitas
    })
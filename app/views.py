from django.shortcuts import render
import json
import os

DATABASE = "data/cuentas.json"


def inicializar_database():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATABASE):
        with open(DATABASE, "w") as archivo:
            json.dump([], archivo, indent=4)


def cargar_cuentas():
    if not os.path.exists(DATABASE):
        return []

    with open(DATABASE, "r") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def guardar_cuentas(cuentas):
    with open(DATABASE, "w") as archivo:
        json.dump(cuentas, archivo, indent=4)


inicializar_database()


# Index
def inicio(request):
    return render(request, "index.html")


# Cuentas
def info_cuentas(request):
    cuentas = cargar_cuentas()
    return render(request, "cuentas.html", {"cuentas": cuentas})


# Registro de cuentas
def registrar(request):

    if request.method == "POST":

        cuentaNombre = request.POST["cuentaNombre"]
        tipo = request.POST["tipo"]
        saldo = float(request.POST["saldo"])

        # Cargar cuentas existentes
        cuentas = cargar_cuentas()

        nueva_cuenta = {
            "cuentaNombre": cuentaNombre,
            "tipo": tipo,
            "saldo": saldo
        }

        cuentas.append(nueva_cuenta)

        # Guardar en JSON
        guardar_cuentas(cuentas)

        return render(request, "cuentas.html", {"cuentas": cuentas})

    return render(request, "registrar.html")

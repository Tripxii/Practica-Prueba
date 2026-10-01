
import heapq
import json
import sys


class Paciente:
    def __init__(self, id_paciente, nombre, ivmt):
        self.id = id_paciente
        self.nombre = nombre
        self.ivmt = ivmt

    def __str__(self):
        return f"[{self.id}] {self.nombre:<22} IVMT: {self.ivmt}"


def leer_pacientes(ruta):
    # Lee el json y va entregando los pacientes de a uno
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    for d in datos["pacientes"]:
        yield Paciente(d["id"], d["nombre"], d["ivmt"])


def seleccionar_top_k(pacientes, k):
    if k <= 0:
        raise ValueError("K debe ser un entero positivo")

    heap = []  # la raiz siempre es el paciente con menor IVMT de los K elegidos

    for orden, paciente in enumerate(pacientes):
        # Se guarda (ivmt, -orden, paciente). El -orden sirve para los empates:
        # si dos tienen el mismo IVMT, el que llegó después queda más abajo y es
        # el primero en salir. Ademas evita que Python compare objetos Paciente.
        elemento = (paciente.ivmt, -orden, paciente)

        if len(heap) < k:
            heapq.heappush(heap, elemento)
        elif elemento > heap[0]:
            # Es más vulnerable que el peor de los K actuales: lo reemplaza
            heapq.heapreplace(heap, elemento)

    # Para dejarlos ordenados se sacan todos del heap (salen de menor a mayor)
    resultado = []
    while len(heap) > 0:
        resultado.append(heapq.heappop(heap)[2])

    resultado.reverse()  # ahora quedan de mayor a menor IVMT
    return resultado


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else "pacientes.json"
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    seleccionados = seleccionar_top_k(leer_pacientes(ruta), k)

    print(f"Top {k} pacientes con mayor IVMT")
    print("-" * 46)
    for i, p in enumerate(seleccionados, start=1):
        print(f"{i:>2}. {p}")


if __name__ == "__main__":
    main()
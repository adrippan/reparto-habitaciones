#!/usr/bin/env python3
import heapq

def greedy(h, g):
    """
    Heurístico greedy first-fit minimizando la capacidad remanente.
    Devuelve tupla ((asig, habs), vacias)
    """
    n = len(h)
    asig = []
    habs = h.copy()
    usados_chicos = set()
    usados_chicas = set()
    for idx, size in enumerate(g):
        es_chico = (idx % 2 == 0)
        best = None
        best_rem = None
        for i in range(n):
            if habs[i] >= size:
                if es_chico and i in usados_chicas:
                    continue
                if not es_chico and i in usados_chicos:
                    continue
                rem = habs[i] - size
                if best is None or rem < best_rem:
                    best, best_rem = i, rem
        if best is None:
            # No cabe este grupo
            return (asig, habs), 0
        asig.append(best)
        habs[best] -= size
        if es_chico:
            usados_chicos.add(best)
        else:
            usados_chicas.add(best)
    vacias = len(h) - len(set(asig))
    return (asig, habs), vacias


def repartoHabitaciones(h, g):
    """
    Branch & Bound para asignar grupos g (alternando chico/chica)
    en habitaciones con capacidades h, maximizando habitaciones libres.
    Se arranca usando una solución greedy como cota inicial.
    Devuelve ((asig, rem_caps), num_vacias).
    """
    # 1) Solución inicial greedy para tener fx
    (asig0, habs0), fx = greedy(h, g)
    best = (asig0, habs0)

    def cota_optimista(estado):
        asig, habs = estado
        return len(habs) - len(set(asig))

    def branch(estado):
        asig, habs = estado
        idx = len(asig)
        # Separar previas por sexo
        habs_chicos = [hab for pos, hab in enumerate(asig) if pos % 2 == 0]
        habs_chicas = [hab for pos, hab in enumerate(asig) if pos % 2 != 0]
        hijos = []
        for i, cap in enumerate(habs):
            if g[idx] <= cap:
                es_chico = (idx % 2 == 0)
                if (es_chico and i in habs_chicas) or (not es_chico and i in habs_chicos):
                    continue
                nh = habs.copy()
                nh[i] -= g[idx]
                opt = cota_optimista((asig + [i], nh))
                hijos.append((opt, (asig + [i], nh)))
        return hijos

    def is_complete(estado):
        return len(estado[0]) == len(g)

    # 2) Inicializar heap
    A = []
    inicial = ([], h.copy())
    heapq.heappush(A, (-cota_optimista(inicial), inicial))

    # 3) Bucle de ramificación y poda
    while A and -A[0][0] > fx:
        _, estado = heapq.heappop(A)
        for opt, child in branch(estado):
            if is_complete(child):
                if opt > fx:
                    fx, best = opt, child
            else:
                if opt > fx:
                    heapq.heappush(A, (-opt, child))
    return best, fx


if __name__ == "__main__":
    # Instancia por defecto: habitaciones y grupos
    room_names = ["C", "A", "B", "R", "I", "LL", "A2", "S"] + [f"M{i}" for i in range(1, 9)]
    # Capacidades: 20 cada habitación
    h = [20] * len(room_names)
    # Grupos: 12 grupos con 10 chicos y 10 chicas cada uno (lista alternada)
    g = []
    for _ in range(12):
        g.extend([10, 10])
    # Ejecutar algoritmo
    (asig, rem), vacias = repartoHabitaciones(h, g)
    # Mostrar resultados
    print("Asignación de habitaciones:")
    for idx, hab in enumerate(asig):
        grupo = idx // 2 + 1
        sexo = "CHICOS" if idx % 2 == 0 else "CHICAS"
        print(f"Grupo {grupo:2d} {sexo:6s} → Habitación {room_names[hab]}")
    print(f"\nNúmero de habitaciones vacías: {vacias}")
    print("Capacidades restantes:")
    for name, cap in zip(room_names, rem):
        print(f"  {name:3s}: {cap}")

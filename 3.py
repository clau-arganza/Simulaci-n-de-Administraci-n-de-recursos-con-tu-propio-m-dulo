MATERIALES = ["ladrillo", "ventanas", "rejas", "cemento", "madera"]

recursos = [800, 100, 120, 500, 500]
edificios = {
    "zara":             [200, 10, 1,   100, 50],
    "tienda de cómics": [100,  2, 5,    50, 25],
    "manicomio":        [300, 30, 100, 150, 100],
}
edificios_creados = []

# === GRAFO DE DEPENDENCIAS (lista de adyacencia) ===
# Para construir una clave, deben existir antes todos los valores de su lista.
dependencias = {
    "zara": [],
    "tienda de cómics": [],
    "manicomio": ["zara", "tienda de cómics"],
}

def mostrar_grafo_dependencias():
    print("\n=== Grafo de dependencias (A -> requiere ...) ===")
    for nodo, reqs in dependencias.items():
        if reqs:
            print(f"- {nodo} -> {', '.join(reqs)}")
        else:
            print(f"- {nodo} -> (sin requisitos)")

def prerequisitos_pendientes(nombre):
    """Devuelve la lista de prerequisitos que aún faltan por construir para 'nombre'."""
    reqs = dependencias.get(nombre, [])
    faltan = [r for r in reqs if r not in edificios_creados]
    return faltan

def puede_construirse(nombre):
    """Comprueba si un edificio cumple sus dependencias en el grafo."""
    faltan = prerequisitos_pendientes(nombre)
    return len(faltan) == 0

def mostrar_recursos():
    print("\n=== Recursos disponibles ===")
    for nombre, cant in zip(MATERIALES, recursos):
        print(f"- {nombre}: {cant}")

def mostrar_edificios():
    print("\n=== Edificios disponibles (costes) ===")
    for (nombre, coste) in edificios.items():
        lista_materiales = ""
        for m, c in zip(MATERIALES, coste):
            lista_materiales += ", " + f"{m}:{c}"
        print(f"{nombre} -> {lista_materiales}")

def buscar_edificios(nombre):
    if nombre not in edificios:
        print("No existe el edificio.")
        return

    # === Comprobación de grafo de dependencias ===
    if not puede_construirse(nombre):
        faltan = prerequisitos_pendientes(nombre)
        print(f"No puedes construir '{nombre}' todavía. Te faltan: {', '.join(faltan)}")
        return

    cant_mat = edificios[nombre]
    crear_edificio(cant_mat, nombre)

def crear_edificio(cant_mat, nombre):
    suficiente = True
    for e, r in zip(cant_mat, recursos):
        if r < e:
            suficiente = False
            break

    if not suficiente:
        print("No tienes materiales suficientes.")
        return

    # Descontar materiales
    for i in range(len(recursos)):
        recursos[i] -= cant_mat[i]

    edificios_creados.append(nombre)

    # Mensajes de estado
    if len(edificios_creados) > 1:
        print(f"\n=== Edificios creados: {edificios_creados} ===\n")
    else:
        print(f"\n=== El edificio creado es {edificios_creados} ===\n")

    print("\n=== Materiales restantes ===")
    for n, cant in zip(MATERIALES, recursos):
        print(f"- {n}: {cant}")

def main():
    while True:
        mostrar_recursos()
        mostrar_edificios()
        mostrar_grafo_dependencias()

        eleccion = input("\nElige un edificio (nombre): ").lower().strip()
        buscar_edificios(eleccion)

        sino = input("¿Quieres seguir construyendo edificios? (S/N): ").lower().strip()
        if sino == "n":
            break

if __name__ == "__main__":
    main()

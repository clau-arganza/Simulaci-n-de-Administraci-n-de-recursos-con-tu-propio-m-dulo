MATERIALES = ["ladrillo", "ventanas", "rejas", "cemento", "madera"]

recursos = [800, 100, 120, 500, 500]
edificios = {
        "zara":             [200, 10, 1,   100, 50],
        "tienda de cómics": [100,  2, 5,    50, 25],
        "manicomio":        [300, 30, 100, 150, 100],
    }
edificios_creados=[]

# ========= NUEVO: tiempos de construcción (horas con 1 obrero) =========
tiempos = {
    "zara": 30,
    "tienda de cómics": 20,
    "manicomio": 60
}
num_obreros = 8  # puedes cambiarlo desde el menú

# ========= Código original (sin cambios de estructura) =========
def mostrar_recursos():
    print("\n=== Recursos disponibles ===")
    for nombre, cant in zip(MATERIALES, recursos):
        print(f"- {nombre}: {cant}")
    
def mostrar_edificios():
    print("\n=== Edificios disponibles (costes) ===")
    for (nombre, coste) in edificios.items():
        lista_materiales=""
        for m, c in zip(MATERIALES, coste):
            lista_materiales+=", "+f"{m}:{c}"
        print(f"{nombre} -> {lista_materiales}")

def buscar_edificios(nombre): 
    if nombre in edificios: 
        cant_mat=edificios[nombre]
        crear_edificio(cant_mat,nombre)    
    else:          
        print("no existe el Edificio")
    
def crear_edificio(cant_mat,nombre):
    suficiente=1
    for e,r in zip(cant_mat,recursos):
        if not r>=e:
            print ("No tienes Materiales suficientes")
            suficiente=0
    if suficiente>0:
        for x, valor in enumerate(recursos):
            valor-=cant_mat[x]
            if valor>-1 :
                recursos[x]=valor
        edificios_creados.append(nombre) 
        if  len(edificios_creados) > 1:
            print(f"\n=== Edificios creados es {edificios_creados}  ===\n")    
        else:    
            print(f"\n=== El edificio creado es {edificios_creados}  ===\n")        
        print("\n=== Materiales restantes ===")
        for nombre, cant in zip(MATERIALES, recursos):
            print(f"- {nombre}: {cant}")   

# ========= NUEVO: utilidades de simulación =========
def _validar_proyecto():
    if not edificios_creados:
        print("\nNo hay edificios en el proyecto. Crea alguno primero.")
        return False
    # también comprobamos que tengan tiempo definido
    no_def = [e for e in edificios_creados if e not in tiempos]
    if no_def:
        print("\nFaltan tiempos definidos para:", ", ".join(no_def))
        return False
    return True

def _imprimir_resumen_tiempos():
    print("\n=== Tiempos (1 obrero) de los edificios del proyecto ===")
    for e in edificios_creados:
        print(f"- {e}: {tiempos[e]} h")

def _simular(asignador, grupo=None):
    """
    Simulación discreta (hora a hora).
    - asignador(total_obreros, trabajos_restantes) -> dict {edificio: obreros_asignados}
    - trabajos_restantes: dict {edificio: horas-obrero restantes}
    """
    trabajos_restantes = {e: tiempos[e] for e in edificios_creados}  # horas con 1 obrero
    tiempo_total = 0
    # registro simple para una traza corta (opcional)
    # mientras quede trabajo en alguna obra
    while any(v > 0 for v in trabajos_restantes.values()):
        asignacion = asignador(num_obreros, trabajos_restantes, grupo)
        # consumir 1 hora de trabajo por obrero asignado a cada obra
        for ed, obr in asignacion.items():
            if trabajos_restantes[ed] > 0 and obr > 0:
                trabajos_restantes[ed] -= obr
                if trabajos_restantes[ed] < 0:
                    trabajos_restantes[ed] = 0
        tiempo_total += 1
    return tiempo_total

# Asignadores (tres modos pedidos)
def _asignador_equidad(total_obr, trabajos, _):
    """Reparte lo más equitativamente posible entre TODAS las obras con trabajo."""
    activas = [e for e, restante in trabajos.items() if restante > 0]
    asignacion = {e: 0 for e in trabajos}
    if not activas or total_obr <= 0:
        return asignacion
    base = total_obr // len(activas)
    extra = total_obr % len(activas)
    for i, e in enumerate(activas):
        asignacion[e] = base + (1 if i < extra else 0)
    return asignacion

def _asignador_uno_por_obra(total_obr, trabajos, _):
    """Como máximo 1 obrero por obra simultáneamente."""
    asignacion = {e: 0 for e in trabajos}
    if total_obr <= 0:
        return asignacion
    activas = [e for e, restante in trabajos.items() if restante > 0]
    # asignamos de izquierda a derecha 1 obrero
    for e in activas:
        if total_obr == 0:
            break
        asignacion[e] = 1
        total_obr -= 1
    return asignacion

def _asignador_en_grupos(total_obr, trabajos, grupo):
    """Obreros trabajan en grupos de tamaño 'grupo' (máx grupo por obra)."""
    if not grupo or grupo <= 0:
        grupo = 1
    asignacion = {e: 0 for e in trabajos}
    activas = [e for e, restante in trabajos.items() if restante > 0]
    # número de grupos que caben
    grupos_disponibles = total_obr // grupo
    i = 0
    while grupos_disponibles > 0 and i < len(activas):
        e = activas[i]
        asignacion[e] = grupo
        grupos_disponibles -= 1
        i += 1
    return asignacion

# Wrappers de usuario
def simular_equidad():
    if not _validar_proyecto(): 
        return
    _imprimir_resumen_tiempos()
    t = _simular(_asignador_equidad)
    print(f"\n[Equidad] Con {num_obreros} obreros, tiempo total = {t} horas.")

def simular_uno_por_obra():
    if not _validar_proyecto(): 
        return
    _imprimir_resumen_tiempos()
    t = _simular(_asignador_uno_por_obra)
    print(f"\n[Uno por obra] Con {num_obreros} obreros, tiempo total = {t} horas.")

def simular_en_grupos():
    if not _validar_proyecto(): 
        return
    try:
        g = int(input("Tamaño de grupo (p.ej. 2): ").strip() or "2")
    except ValueError:
        g = 2
    _imprimir_resumen_tiempos()
    t = _simular(_asignador_en_grupos, grupo=g)
    print(f"\n[Grupos de {g}] Con {num_obreros} obreros, tiempo total = {t} horas.")

def configurar_obreros():
    global num_obreros
    try:
        n = int(input("¿Cuántos obreros trabajarán en el proyecto?: ").strip())
        if n <= 0:
            print("Debe ser un entero positivo.")
        else:
            num_obreros = n
            print(f"Ahora hay {num_obreros} obreros asignados al proyecto.")
    except ValueError:
        print("Entrada no válida.")

def configurar_tiempo_edificio():
    print("\n=== Configurar tiempo de un edificio (horas con 1 obrero) ===")
    for nombre in edificios.keys():
        print("-", nombre)
    nombre = input("Elige edificio: ").strip().lower()
    # matcheo simple (nombre exacto en minúsculas)
    clave = None
    for k in edificios.keys():
        if k.lower() == nombre:
            clave = k
            break
    if clave is None:
        print("No existe el edificio.")
        return
    try:
        h = int(input("Horas con 1 obrero: ").strip())
        if h <= 0:
            print("Debe ser un entero positivo.")
            return
        tiempos[clave] = h
        print(f"Tiempo para '{clave}' actualizado a {h} h.")
    except ValueError:
        print("Entrada no válida.")

# ========= Menú principal ampliado =========
def main():
    while True:
        print("\n============== MENÚ ==============")
        mostrar_recursos()
        mostrar_edificios()
        print("\nAcciones:")
        print("1) Construir (gasta materiales y añade al proyecto)")
        print("2) Configurar número de obreros (actual:", num_obreros, ")")
        print("3) Configurar tiempo (horas con 1 obrero) de un edificio")
        print("4) Simular: reparto equitativo")
        print("5) Simular: uno por obra")
        print("6) Simular: en grupos")
        print("7) Ver lista de edificios en el proyecto")
        print("0) Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            eleccion = input("\nElige un edificio (nombre): ").strip()
            buscar_edificios(eleccion)
        elif opcion == "2":
            configurar_obreros()
        elif opcion == "3":
            configurar_tiempo_edificio()
        elif opcion == "4":
            simular_equidad()
        elif opcion == "5":
            simular_uno_por_obra()
        elif opcion == "6":
            simular_en_grupos()
        elif opcion == "7":
            print("\nEdificios en el proyecto:", edificios_creados if edificios_creados else "Ninguno")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

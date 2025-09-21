MATERIALES = ["ladrillo", "ventanas", "rejas", "cemento", "madera"]

recursos = [800, 100, 120, 500, 500]
edificios = {
        "Zara":             [200, 10, 0,   100, 50],
        "tienda de cómics": [100,  2, 1,    50, 25],
        "manicomio":        [300, 30, 100, 150, 100],
    }



def mostrar_recursos():
    print("\n=== Recursos disponibles ===")
    for nombre, cant in zip(MATERIALES, recursos):
        print(f"- {nombre}: {cant}")
    
 
def mostrar_edificios():
    print("\n=== Edificios disponibles (costes) ===")
    for i, (nombre, coste) in enumerate(edificios.items(), start=1):
        coste_str = ", ".join(f"{m}:{c}" for m, c in zip(MATERIALES, coste))
        print(f"{i}. {nombre} -> {coste_str}")

def buscar_edificios(nombre): 
    if nombre.isdigit():
        
        if int(nombre)>0 and int(nombre)<len(edificios)+1:
            
            print(f"  {edificios['tienda de cómics']}")
        else:
            print(" no correcto")    
    else: 
        for edificio in edificios:
            if nombre==edificio.lower():
                print(nombre)


    

        
def main():
    mostrar_recursos()
    mostrar_edificios()
    
    eleccion = input("\nElige un edificio (número o nombre): ").strip().lower()
    
    buscar_edificios(eleccion)
    
    
if __name__ == "__main__":
    main()
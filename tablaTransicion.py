import matplotlib
import graphviz
matplotlib.use('Agg')
class TablaTransiciones:
    def __init__(self):
        self.tabla = {}
        self.estado_inicial = None
        self.estados_finales = set()
        self.estados_no_finales = set()

    def agregar_transicion(self, estado, caracter, nuevo_estado):
        if estado not in self.tabla:
            self.tabla[estado] = {}
        self.tabla[estado][caracter] = nuevo_estado

    def probar_cadena(self, cadena):
        estado_actual = 'q0'
        for caracter in cadena:
            if caracter.isdigit():
                caracter = '[digito]'
            try:
                estado_actual = self.tabla[estado_actual][caracter]
            except KeyError:
                return False, estado_actual
        return estado_actual in self.estados_finales, estado_actual

    def borrar_transicion(self, fila):
        fila -= 1
        all_transitions = [(estado, caracter, nuevo_estado) for estado, transitions in self.tabla.items() for caracter, nuevo_estado in transitions.items()]
        if 0 <= fila < len(all_transitions):
            estado, caracter, _ = all_transitions[fila]
            del self.tabla[estado][caracter]
            if not self.tabla[estado]:
                del self.tabla[estado]


def generar_diagrama(tabla):
    G = graphviz.Digraph(format='png')

    for estado, transiciones in tabla.tabla.items():
        for caracter, nuevo_estado in transiciones.items():
            G.edge(estado, nuevo_estado, label=caracter)

    G.render(filename='diagrama', cleanup=True)
    print("Diagrama generado y guardado como 'diagrama.png'")

def ingresar_tabla(tabla):
    while True:
        try:
            estado = input("Ingrese el estado (ejemplo: q0): ")
            if tabla.estado_inicial is None:
                es_inicial = input(f"¿{estado} es el estado inicial? (si/no): ").lower()
                if es_inicial == 'si':
                    tabla.estado_inicial = estado

            caracter = input("Ingrese el caracter (ejemplo: +): ")
            nuevo_estado = input("Ingrese el nuevo estado (ejemplo: q1): ")

            if nuevo_estado not in tabla.estados_finales and nuevo_estado not in tabla.estados_no_finales:
                es_final = input(f"¿{nuevo_estado} es un estado final? (si/no): ").lower()
                if es_final == 'si':
                    tabla.estados_finales.add(nuevo_estado)
                else:
                    tabla.estados_no_finales.add(nuevo_estado)

            tabla.agregar_transicion(estado, caracter, nuevo_estado)
            break
        except ValueError:
            print("Entrada no válida, intente de nuevo.")

def probar_cadena(tabla):
    try:
        cadena = input("Ingrese la cadena a probar: ")
        es_valida, estado_final = tabla.probar_cadena(cadena)
        if es_valida:
            print(f"\nLa cadena es válida y terminó en el estado {estado_final}.")
        else:
            print(f"\nLa cadena no es válida. Se detuvo en el estado {estado_final}.")
    except Exception as e:
        print(f"\nOcurrió un error: {e}")

def ver_tabla(tabla):
    print("----------------------")
    print("| Nº | Estado | Caracter | Nuevo Estado |")
    print("----------------------")
    fila = 1
    for estado, transiciones in tabla.tabla.items():
        for caracter, nuevo_estado in transiciones.items():
            print(f"| {fila} | {estado} | {caracter.center(9)} | {nuevo_estado} |")
            fila += 1
    print("----------------------")

def borrar_transicion(tabla):
    ver_tabla(tabla)
    try:
        fila = int(input("Ingrese el número de fila a borrar (o 'no' para cancelar): "))
        tabla.borrar_transicion(fila)
    except ValueError:
        print("Operación cancelada.")

def instrucciones_de_uso():
    print("\nInstrucciones de Uso para 'Ingresar/Modificar Tabla de Transiciones'")
    print("---------------------------------------------------------------------")
    print("- Al ingresar un estado, sigue el formato 'qx' donde x es un número. Por ejemplo: q0, q1, q2, etc.")
    print("- El caracter `[digito]` es especial y representa cualquier número del 0 al 9. Si desea que un estado transite con un número, use este caracter.")
    print("- Si comete un error al ingresar una transición, puede usar la opción 4 del menú principal para borrar una fila específica.")
    print("- Al ingresar el caracter, asegúrese de que sea un solo carácter, excepto para `[digito]`.")
    print("- Si ingresa un estado como inicial, el programa no volverá a preguntar si es inicial en futuras inserciones. Lo mismo aplica para estados finales.")
    print("- Tenga en cuenta que el programa es sensible a mayúsculas y minúsculas, por lo que 'q0' y 'Q0' serían tratados como estados diferentes.")
    print("- Una vez haya ingresado todos los estados y transiciones que desee, puede utilizar la opción 6 del menú principal para generar el diagrama de transiciones.")
    print("\nRecuerde siempre seguir los ejemplos mostrados y revise sus entradas antes de confirmar.")
    input("\nPresione Enter para volver al menú principal.")

def mostrar_encabezado():
    print("                 ┌─────────────────────────────────────────────────────┐")
    print("                 │                                                     │")
    print("                 │       Universidad Mariano Gálvez de Guatemala       │")
    print("                 │    Proyecto Final - Autómatas y Lenguajes Formales  │")
    print("                 │                      Grupo 7                        │")
    print("                 │                                                     │")
    print("                 │                       Integrantes:                  │")
    print("                 │       Brandon Stewart Diaz Lopez - 0900-14-307      │")
    print("                 │      Favio Ezequiel Urrea Aguilar - 0900-17-712     │")
    print("                 │                                                     │")
    print("                 └─────────────────────────────────────────────────────┘")
def menu_principal():
    print("\nApp de Tabla de Transiciones")
    print("1. Ingresar/Modificar Tabla de Transiciones")
    print("2. Probar una cadena")
    print("3. Ver Tabla de Transiciones")
    print("4. Borrar una fila de la Tabla de Transiciones")
    print("5. Instrucciones de Uso para 'Ingresar/Modificar'")
    print("6. Generar Diagrama de Transiciones")  # Nueva opción
    print("7. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

def main():
    tabla_transiciones = TablaTransiciones()
    mostrar_encabezado()
    while True:
        opcion = menu_principal()
        if opcion == "1":
            ingresar_tabla(tabla_transiciones)
        elif opcion == "2":
            probar_cadena(tabla_transiciones)
        elif opcion == "3":
            ver_tabla(tabla_transiciones)
        elif opcion == "4":
            borrar_transicion(tabla_transiciones)
        elif opcion == "5":
            instrucciones_de_uso()
        elif opcion == "6":
            generar_diagrama(tabla_transiciones)
        elif opcion == "7":
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
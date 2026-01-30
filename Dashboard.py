import os
import subprocess
import json
from datetime import datetime


def mostrar_codigo(ruta_script):
    # Asegúrate de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding="utf-8") as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'py', ruta_script])
        else:  # Unix-based systems
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")
ARCHIVO_TAREAS = "tasks.json"

def cargar_tareas():
    if not os.path.exists(ARCHIVO_TAREAS):
        return []
    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_tareas(tareas):
    with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

def generar_id(tareas):
    if not tareas:
        return 1
    return max(t["id"] for t in tareas) + 1

def menu_tareas():
    tareas = cargar_tareas()

    while True:
        print("\n=== Mis tareas y proyectos ===")
        print("1 - Agregar tarea")
        print("2 - Ver tareas")
        print("3 - Marcar como completada")
        print("4 - Eliminar tarea")
        print("0 - Volver al menú principal")

        op = input("Elige una opción: ").strip()

        if op == "1":
            titulo = input("Título: ").strip()
            if not titulo:
                print("El título no puede estar vacío.")
                continue
            proyecto = input("Proyecto/Materia (ej: POO, Matemáticas): ").strip()
            prioridad = input("Prioridad (Alta/Media/Baja): ").strip() or "Media"

            nueva = {
                "id": generar_id(tareas),
                "titulo": titulo,
                "proyecto": proyecto,
                "prioridad": prioridad,
                "estado": "Pendiente",
                "creada": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            tareas.append(nueva)
            guardar_tareas(tareas)
            print("Tarea agregada.")

        elif op == "2":
            if not tareas:
                print("No hay tareas registradas.")
                continue

            print("\n--- Lista de tareas ---")
            for t in tareas:
                print(f"[{t['id']}] {t['titulo']} | {t['proyecto']} | {t['prioridad']} | {t['estado']} | {t['creada']}")

        elif op == "3":
            if not tareas:
                print("No hay tareas para marcar.")
                continue
            try:
                tid = int(input("ID de la tarea a completar: ").strip())
                encontrada = False
                for t in tareas:
                    if t["id"] == tid:
                        t["estado"] = "Completada"
                        encontrada = True
                        break
                if not encontrada:
                    print(" No existe una tarea con ese ID.")
                else:
                    guardar_tareas(tareas)
                    print("Tarea marcada como completada.")
            except ValueError:
                print("Ingresa un número válido.")

        elif op == "4":
            if not tareas:
                print("No hay tareas para eliminar.")
                continue
            try:
                tid = int(input("ID de la tarea a eliminar: ").strip())
                nuevas = [t for t in tareas if t["id"] != tid]
                if len(nuevas) == len(tareas):
                    print("No existe una tarea con ese ID.")
                else:
                    tareas = nuevas
                    guardar_tareas(tareas)
                    print("Tarea eliminada.")
            except ValueError:
                print("Ingresa un número válido.")

        elif op == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


def mostrar_menu():
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2',
        '3': 'Mis tareas y proyectos'
    }

    while True:
        print("\nMenu Principal - Dashboard")
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        print("0 - Salir")

        eleccion_unidad = input("Elige una unidad o '0' para salir: ").strip()

        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad == '3':
            menu_tareas()
        elif eleccion_unidad in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, unidades[eleccion_unidad]))
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")


def mostrar_sub_menu(ruta_unidad):
    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        print("\nSubmenú - Selecciona una subcarpeta")
        # Imprime las subcarpetas
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ")
        if eleccion_carpeta == '0':
            break
        else:
            try:
                eleccion_carpeta = int(eleccion_carpeta) - 1
                if 0 <= eleccion_carpeta < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[eleccion_carpeta]))
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

def mostrar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    while True:
        print("\nScripts - Selecciona un script para ver y ejecutar")
        # Imprime los scripts
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar al submenú anterior")
        print("9 - Regresar al menú principal")

        eleccion_script = input("Elige un script, '0' para regresar o '9' para ir al menú principal: ")
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return  # Regresar al menú principal
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()


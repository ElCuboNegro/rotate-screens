import keyboard
import win32api
import win32con
import threading
import time

# Definir constantes necesarias
ENUM_CURRENT_SETTINGS = -1
DISP_CHANGE_SUCCESSFUL = 0
DMDO_DEFAULT = 0
DMDO_90 = 1
DMDO_180 = 2
DMDO_270 = 3

# Crear un lock para manejar las rotaciones
rotation_lock = threading.Lock()
is_rotating = False

# Tiempo mínimo entre rotaciones (en segundos)
DEBOUNCE_TIME = 0.5
last_rotation_time = {}

# Función para obtener los nombres de dispositivos de monitores activos
def get_active_monitor_device_names():
    device_names = []
    i = 0
    while True:
        try:
            device = win32api.EnumDisplayDevices(None, i)
        except Exception:
            break
        if not device.DeviceName:
            break
        if device.StateFlags & win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP:
            device_names.append(device.DeviceName)
        i += 1
    return device_names

def rotate_monitor(device_name, rotation):
    try:
        dm = win32api.EnumDisplaySettings(device_name, ENUM_CURRENT_SETTINGS)

        # Ajustar la orientación y resolución si es necesario
        if rotation == 0 and dm.DisplayOrientation in [DMDO_90, DMDO_270]:
            dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
        elif rotation in [90, 270] and dm.DisplayOrientation in [DMDO_DEFAULT, DMDO_180]:
            dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth

        # Establecer la nueva orientación
        if rotation == 90:
            orientation = DMDO_90
        elif rotation == 180:
            orientation = DMDO_180
        elif rotation == 270:
            orientation = DMDO_270
        else:
            orientation = DMDO_DEFAULT

        dm.DisplayOrientation = orientation

        # Aplicar los cambios
        result = win32api.ChangeDisplaySettingsEx(device_name, dm)
        if result != DISP_CHANGE_SUCCESSFUL:
            print(f"Error al cambiar la orientación del monitor {device_name}")
        else:
            print(f"Monitor {device_name} rotado a {rotation} grados.")
    except Exception as e:
        print(f"No se pudo rotar el monitor {device_name}: {e}")

def toggle_rotation(monitor_index):
    global is_rotating
    current_time = time.time()
    last_time = last_rotation_time.get('toggle_rotation', 0)
    if current_time - last_time < DEBOUNCE_TIME:
        # Ignorar el evento si está dentro del tiempo de debounce
        return
    last_rotation_time['toggle_rotation'] = current_time

    with rotation_lock:
        if is_rotating:
            print("Rotación en progreso. Por favor, espera.")
            return
        if monitor_index >= len(device_names):
            print(f"Monitor {monitor_index} no está disponible.")
            return
        is_rotating = True

    def rotation_task():
        global is_rotating
        try:
            device_name = device_names[monitor_index]
            try:
                dm = win32api.EnumDisplaySettings(device_name, ENUM_CURRENT_SETTINGS)
                current_orientation = dm.DisplayOrientation

                # Determinar la nueva rotación
                if current_orientation == DMDO_DEFAULT:
                    new_rotation = 90
                elif current_orientation == DMDO_90:
                    new_rotation = 0
                elif current_orientation == DMDO_180:
                    new_rotation = 270
                elif current_orientation == DMDO_270:
                    new_rotation = 180
                else:
                    new_rotation = DMDO_DEFAULT

                rotate_monitor(device_name, new_rotation)
            except Exception as e:
                print(f"Error al obtener configuración de {device_name}: {e}")
        finally:
            with rotation_lock:
                is_rotating = False
            # Esperar un poco para evitar conflictos
            time.sleep(DEBOUNCE_TIME)

    threading.Thread(target=rotation_task).start()

def reset_all_monitors(event):
    global is_rotating
    current_time = time.time()
    last_time = last_rotation_time.get('reset_all_monitors', 0)
    if current_time - last_time < DEBOUNCE_TIME:
        # Ignorar el evento si está dentro del tiempo de debounce
        return
    last_rotation_time['reset_all_monitors'] = current_time

    with rotation_lock:
        if is_rotating:
            print("Rotación en progreso. Por favor, espera.")
            return
        if not device_names:
            print("No se encontraron monitores para reiniciar.")
            return
        is_rotating = True

    def reset_task():
        global is_rotating
        try:
            for device_name in device_names:
                rotate_monitor(device_name, 0)
        finally:
            with rotation_lock:
                is_rotating = False
            time.sleep(DEBOUNCE_TIME)

    threading.Thread(target=reset_task).start()

# Obtener los nombres de dispositivos de monitores activos
device_names = get_active_monitor_device_names()

# Mostrar los monitores detectados
print("Monitores detectados:")
for idx, name in enumerate(device_names):
    print(f"Monitor {idx}: {name}")

# Asignar funciones a las teclas usando on_release_key
keyboard.on_release_key('F13', reset_all_monitors, suppress=True)
keyboard.on_release_key('F14', lambda e: toggle_rotation(0), suppress=True)
keyboard.on_release_key('F15', lambda e: toggle_rotation(1), suppress=True)
keyboard.on_release_key('F16', lambda e: toggle_rotation(2), suppress=True)
keyboard.on_release_key('F17', lambda e: toggle_rotation(3), suppress=True)

print("\nScript en ejecución.")
print("F13: Reiniciar todos los monitores a 0 grados.")
print("F14: Rotar monitor 0 entre 0 y 90 grados.")
print("F15: Rotar monitor 1 entre 0 y 90 grados.")
print("F16: Rotar monitor 2 entre 0 y 90 grados.")
print("F17: Rotar monitor 3 entre 0 y 90 grados.")

keyboard.wait()

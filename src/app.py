import json
import tkinter as tk
from tkinter import scrolledtext
from difflib import SequenceMatcher

# ── Cargar base de datos ──────────────────────────────────────────────────────

def cargar_base_datos():
    try:
        with open("base_datos.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"preguntas": []}

# ── Lógica de búsqueda ────────────────────────────────────────────────────────

def similitud(texto_a, texto_b):
    """Devuelve un valor entre 0 y 1 indicando cuán parecidos son dos textos."""
    return SequenceMatcher(None, texto_a.lower(), texto_b.lower()).ratio()

def buscar_respuesta(pregunta, base_datos):
    """
    Búsqueda en dos pasos:
    Coincidencia exacta de palabras clave (igual que antes).
    Si no hay exacta, busca la entrada más similar (búsqueda difusa).
       Solo devuelve resultado si la similitud supera el umbral mínimo.
    """
    palabras_pregunta = set(pregunta.lower().split())

    # coincidencia exacta
    for item in base_datos["preguntas"]:
        palabras_clave = set(item["pregunta"].lower().split())
        if palabras_clave.intersection(palabras_pregunta):
            url = item.get("url", "No disponible")
            return item["respuesta"] + f"\nMás información: {url}", "exacta"

    # búsqueda difusa
    UMBRAL = 0.45  # similitud mínima para aceptar un resultado
    mejor_item = None
    mejor_puntuacion = 0.0

    for item in base_datos["preguntas"]:
        # comparar la pregunta del usuario con la clave del JSON
        puntuacion = similitud(pregunta, item["pregunta"])

        # también comparar palabra a palabra
        for palabra in palabras_pregunta:
            for clave in item["pregunta"].lower().split():
                punt_palabra = similitud(palabra, clave)
                if punt_palabra > puntuacion:
                    puntuacion = punt_palabra

        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_item = item

    if mejor_item and mejor_puntuacion >= UMBRAL:
        url = mejor_item.get("url", "No disponible")
        respuesta = (
            f"(Quizás quisiste preguntar por '{mejor_item['pregunta']}')\n\n"
            f"{mejor_item['respuesta']}\nMás información: {url}"
        )
        return respuesta, "difusa"

    return "Lo siento, no encontré ningún comando relacionado. Prueba con palabras como: ls, cd, grep, chmod...", "ninguna"

# ── Interfaz gráfica ──────────────────────────────────────────────────────────

def obtener_respuesta(event=None):
    pregunta = entrada_usuario.get().strip()
    if not pregunta:
        return

    respuesta, tipo = buscar_respuesta(pregunta, base_datos)

    # color del indicador según tipo de búsqueda
    colores = {"exacta": "#4CAF50", "difusa": "#FF9800", "ninguna": "#F44336"}
    etiquetas = {"exacta": "✓ coincidencia exacta", "difusa": "~ coincidencia aproximada", "ninguna": "✗ sin resultado"}

    historial_texto.config(state=tk.NORMAL)
    historial_texto.insert(tk.END, f"Tú: {pregunta}\n", "pregunta")
    historial_texto.insert(tk.END, f"Chatbot: {respuesta}\n", "respuesta")
    historial_texto.insert(tk.END, f"{etiquetas[tipo]}\n\n", f"tipo_{tipo}")
    historial_texto.config(state=tk.DISABLED)
    historial_texto.see(tk.END)

    # cctualizar contador
    contador["value"] += 1
    label_contador.config(text=f"Preguntas realizadas: {contador['value']}")

    entrada_usuario.delete(0, tk.END)

def limpiar_historial():
    historial_texto.config(state=tk.NORMAL)
    historial_texto.delete("1.0", tk.END)
    historial_texto.insert(tk.END, "Chatbot: ¡Hola! Pregúntame sobre comandos Linux.\n\n", "respuesta")
    historial_texto.config(state=tk.DISABLED)
    contador["value"] = 0
    label_contador.config(text="Preguntas realizadas: 0")

# ── Inicialización ────────────────────────────────────────────────────────────

base_datos = cargar_base_datos()
contador = {"value": 0}

root = tk.Tk()
root.title("Chatbot de Comandos Linux")
root.resizable(False, False)

# titulo
tk.Label(root, text="🐧 Chatbot de Comandos Linux", font=("Arial", 14, "bold")).pack(pady=(12, 4))

# area de historial
historial_texto = scrolledtext.ScrolledText(
    root, width=62, height=22, wrap=tk.WORD,
    font=("Arial", 11), state=tk.DISABLED
)
historial_texto.pack(padx=12, pady=4)

# estilos de texto
historial_texto.tag_config("pregunta",   foreground="#1565C0", font=("Arial", 11, "bold"))
historial_texto.tag_config("respuesta",  foreground="#212121", font=("Arial", 11))
historial_texto.tag_config("tipo_exacta",  foreground="#4CAF50", font=("Arial", 9, "italic"))
historial_texto.tag_config("tipo_difusa",  foreground="#FF9800", font=("Arial", 9, "italic"))
historial_texto.tag_config("tipo_ninguna", foreground="#F44336", font=("Arial", 9, "italic"))

# mensaje de bienvenida
historial_texto.config(state=tk.NORMAL)
historial_texto.insert(tk.END, "Chatbot: ¡Hola! Pregúntame sobre comandos Linux. Puedes escribir aunque tengas alguna errata.\n\n", "respuesta")
historial_texto.config(state=tk.DISABLED)

# entrada y botón enviar
frame_entrada = tk.Frame(root)
frame_entrada.pack(padx=12, pady=4, fill=tk.X)

entrada_usuario = tk.Entry(frame_entrada, width=50, font=("Arial", 11))
entrada_usuario.pack(side=tk.LEFT, padx=(0, 6))
entrada_usuario.bind("<Return>", obtener_respuesta)

tk.Button(
    frame_entrada, text="Enviar", command=obtener_respuesta,
    font=("Arial", 11), bg="#4CAF50", fg="white", width=8
).pack(side=tk.LEFT)

# Barra inferior
frame_inferior = tk.Frame(root)
frame_inferior.pack(padx=12, pady=(2, 12), fill=tk.X)

label_contador = tk.Label(frame_inferior, text="Preguntas realizadas: 0", font=("Arial", 9), fg="#757575")
label_contador.pack(side=tk.LEFT)

tk.Button(
    frame_inferior, text="Limpiar", command=limpiar_historial,
    font=("Arial", 9), bg="#E0E0E0", fg="#424242"
).pack(side=tk.RIGHT)

root.mainloop()
import json
import tkinter as tk
from tkinter import scrolledtext

# Aplicación en Python de un chatbot que resuelve dudas sobre los comandos más frecuentes en bash (Linux)

# Cargar base de datos desde el archivo JSON
def cargar_base_datos():
    try:
        with open("base_datos.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"preguntas": []}

# Buscar respuesta en la base de datos
def buscar_respuesta(pregunta, base_datos):
    palabras_pregunta = set(pregunta.lower().split())
    for item in base_datos["preguntas"]:
        palabras_clave = set(item["pregunta"].lower().split())
        if palabras_clave.intersection(palabras_pregunta):
            respuesta = item["respuesta"]
            url = item.get("url", "No disponible")
            return f"{respuesta}\nMás información: {url}"
    return "Lo siento, no tengo una respuesta para esa pregunta. Prueba con otro comando Linux."

# Función que se ejecuta al pulsar "Enviar"
def obtener_respuesta():
    pregunta = entrada_usuario.get()
    if pregunta.strip() == "":
        return
    respuesta = buscar_respuesta(pregunta, base_datos)
    historial_texto.insert(tk.END, f"Tú: {pregunta}\nChatbot: {respuesta}\n\n")
    historial_texto.see(tk.END)
    entrada_usuario.delete(0, tk.END)

# Cargar base de datos al iniciar
base_datos = cargar_base_datos()

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Chatbot de Comandos Linux")
root.resizable(False, False)

# Título
titulo = tk.Label(root, text="🐧 Chatbot de Comandos Linux", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

# Área de historial
historial_texto = scrolledtext.ScrolledText(root, width=60, height=22, wrap=tk.WORD, font=("Arial", 11))
historial_texto.pack(padx=10, pady=5)
historial_texto.insert(tk.END, "Chatbot: ¡Hola! Pregúntame sobre comandos Linux. Por ejemplo: 'ls', 'cd', 'grep', 'chmod'...\n\n")

# Campo de entrada
frame_entrada = tk.Frame(root)
frame_entrada.pack(padx=10, pady=5, fill=tk.X)

entrada_usuario = tk.Entry(frame_entrada, width=48, font=("Arial", 11))
entrada_usuario.pack(side=tk.LEFT, padx=(0, 5))
entrada_usuario.bind("<Return>", lambda event: obtener_respuesta())

boton_enviar = tk.Button(frame_entrada, text="Enviar", command=obtener_respuesta, font=("Arial", 11), bg="#4CAF50", fg="white")
boton_enviar.pack(side=tk.LEFT)

root.mainloop()
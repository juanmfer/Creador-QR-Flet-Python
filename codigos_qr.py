# Creador de QR con Flet y Python
# https://github.com/juanmfer
# Diciembre 2023
import flet as ft
import qrcode
import base64
from io import BytesIO
from PIL import Image
def main(page: ft.Page):
    page.title = "Generador de Codigo QR"
    #page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    # Horizontal
    page.window_width = 300
    # Vertical
    page.window_height = 600
    # resizable True o False
    page.window_resizable = False
    # Actualiza el page
    page.update()
    # Funcion para mostrar el QR
    def generarQr(e):
        page.update()
        texto_error.value = ""
        texto_ok.value = ""
        contControles = len(page.controls)
        # si txt esta vacio
        if txt.value == "":
            # Boton guardar inicia como desactivado
            btn_guardar.disabled = True
            # si no se escribe en txt, arroja advertencia
            texto_error.value = "No hay texto para convertir a QR"
            # se vacia texto_ok en casos previos de generacion.
            texto_ok.value == ""
            # si hay 6 controles, es de una generacion previa, como no se 
            # escribio nada, elimina el ultimo control agregado que es la img del QR
            if contControles >= 6:
                page.controls.pop()
            page.update()
        else:
            # si txt no esta vacio, vacia texto error, por generaciones anteriores
            texto_error.value = ""
            # activa el boton guardar
            btn_guardar.disabled = False
            # construye la imagen del QR con lo escrito en txt
            url = construyeQr(txt.value)
            img = ft.Image(src_base64=url)
            if contControles >= 6:
                page.controls.pop()
            # muestra en texto ok
            texto_ok.value = "QR generado con exito"
            # agrega el control img, para mostrar el QR generado
            page.add(img)
            page.update()
    # Funcion para contruir el QR
    def construyeQr(s):
        qr = qrcode.make(s)
        buffered = BytesIO()
        # Guarda el codigo QR  de la imagen en JPEG
        qr.save(buffered, format="JPEG")
        consBuff = base64.b64encode(buffered.getvalue())
        resultOfQrCode = consBuff.decode("utf-8")
        return resultOfQrCode
    # Funcion para guardar imagen, mismo directorio del archivo .py
    def guardarImagen(e):
        url = construyeQr(txt.value)
        nombre_archivo = "qr_guardado.png"
        #guardar_qr_image(url, nombre_archivo)
        decodificarImg = base64.b64decode(url)
        # Crea una imagen PIL desde los datos decodificados
        img = Image.open(BytesIO(decodificarImg))
        # Guarda la imagen en formato PNG
        img.save(nombre_archivo)
    # txt textfield para escribir lo que se va a convertir
    txt = ft.TextField(label="Convertir a QR",multiline=True)
    # btn Boton para generar el QR
    btn = ft.ElevatedButton("Generar QR",
                            on_click=generarQr,
                            bgcolor="blue",
                            color="white")
    # boton guardar, guarda el QR en imagen, se inicia deshabilitado
    btn_guardar = ft.ElevatedButton("Guardar Imagen QR", on_click=guardarImagen, disabled=True)
    # texto error donde se mostrara advertencia en rojo, en caso de que haya un problema
    texto_error = ft.Text(color="red")
    # texto ok donde se mostrara advertencia en verde, en caso de que se genere con exito
    texto_ok = ft.Text(color="green")
    page.add(txt, btn,texto_error, texto_ok, btn_guardar)
ft.app(target=main)
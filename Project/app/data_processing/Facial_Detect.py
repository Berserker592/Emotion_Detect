# Facial_detect.py
import cv2
import numpy as np
import base64

# Cargar el clasificador en cascada para la detección de rostros
#Servidor
try:
    haar_cascade = cv2.CascadeClassifier('/app/haar_face.xml')
except:
#Local
    haar_cascade = cv2.CascadeClassifier('app/haar_face.xml')

def mostrar_frame(frame,frame2):
    #cv2.imshow("Imagen",frame)
    cv2.imshow('Imagen Recortada',frame2)
    cv2.waitKey(1)


async def Deteccion(frame_data: str):
    i=0
    """
    Función que recibe los datos de una imagen en base64, procesa la imagen y devuelve la región del rostro detectado.
    
    :param frame_data: Cadena en base64 de la imagen recibida.
    :return: Imagen recortada con la cara detectada.
    """
    try:
        # Decodificar los datos base64
        frame_data = frame_data.split(",")[1]  # Eliminar encabezado base64
        frame_bytes = base64.b64decode(frame_data)

        # Convertir el frame a imagen
        np_frame = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

        # Convertir la imagen a escala de grises
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros
        faces_rect = haar_cascade.detectMultiScale(img_gray, scaleFactor=1.3, minNeighbors=4)
        #response = {"faces": [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in faces_rect]}
        #await websocket.send_json(response)

        #faces_roi = None  # Variable para la región de interés (cara detectada)

        for (x, y, w, h) in faces_rect:
            # Recortar la imagen para obtener solo la región de la cara
            faces_roi = frame[y:y+h, x:x+w]
            #mostrar_frame(None,faces_roi)
            #mostrar_frame(frame,faces_roi)
            Ubicacion = [x,y,w,h]
            Ubicacion = [int(i) for i in Ubicacion]
        return faces_rect, faces_roi, Ubicacion

    except Exception as e:
        i = i+1
        #print(f"Error en Deteccion {i}")
        #mostrar_frame(frame,faces_roi)
        return faces_rect, frame, [0,0,0,0]
     

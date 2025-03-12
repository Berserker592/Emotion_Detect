import os
import csv
import asyncio 
from datetime import datetime
from fastapi import FastAPI, WebSocket, UploadFile, File, Form, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from data_processing.Facial_Detect import Deteccion
from data_processing.Emotion_detect import emotion_analize

import subprocess


app = FastAPI()
#Montar la carpeta de archivos esenciales
# CORS y rutas estáticas

#Servidor
#app.mount("/static", StaticFiles(directory="/app/static"), name="static")
#os.makedirs("/home/admin/Reportes", exist_ok=True)
#os.makedirs("/home/admin/Videos", exist_ok=True)

#Local
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
app.mount("/Reportes", StaticFiles(directory="/app/Archivos/Reportes"), name="Reportes")
app.mount("/Videos", StaticFiles(directory="/app/Archivos/Videos"), name="Videos")

#print("Los archivos que se encuentran en la carpeta", os.listdir("/app/static"))
#app.mount("/Reportes", StaticFiles(directory="/app/Archivos/Reportes"), name="Reportes")
#app.mount("/Videos", StaticFiles(directory="/app/Archivos/Videos"), name="Videos")

# Ejecutar el comando 'pwd' en el sistema
#current_directory = subprocess.run(["pwd"], capture_output=True, text=True)
#list_directory = subprocess.run(["ls"], capture_output=True, text=True)


# Mostrar el resultado
#print(current_directory.stdout.strip())
#print(list_directory.stdout.strip())


#os.makedirs("/app/Archivos/Reportes", exist_ok=True)
#os.makedirs("/app/Archivos/Videos", exist_ok=True)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Permitir solicitudes de cualquier origen.
    allow_credentials=True,     # Permitir el uso de cookies y autenticación.
    allow_methods=["*"],        # Permitir cualquier método HTTP (GET, POST, PUT, etc.).
    allow_headers=["*"],        # Permitir cualquier cabecera HTTP personalizada.
)


@app.get("/")
def get_frontend():
    return FileResponse("/app/static/index.html")

# Crear carpeta para reportes y videos
#os.makedirs("/app/Archivos/Reportes", exist_ok=True)
#os.makedirs("/app/Archivos/Videos", exist_ok=True)


# Variables globales para gestionar el análisis
analyzing = True
emotion_log = [] 
features = []#Cantidad de personas en la imagen

templates = Jinja2Templates(directory="static") 


# Página principal
#@app.get("/", response_class=HTMLResponse)
#async def home(request: Request):
     # Renderiza el archivo index.html desde la carpeta templates
#    return templates.TemplateResponse("index.html", {"request": request})

#CODE 2
executor = ThreadPoolExecutor()
frame_queue = asyncio.Queue()  # Cola de frames para procesar en segundo plano

async def process_frames(websocket: WebSocket):
    """Proceso en segundo plano que toma frames de la cola y los analiza"""
    global analyzing, emotion_log, start_an
    start_an = datetime.now()

    while True:
        frame_data = await frame_queue.get()  # Obtener frame de la cola
        
        try:
            # Detectar rostros de forma asíncrona
            faces_rect, faces_roi, Ubicacion = await Deteccion(frame_data)

            # Contar personas detectadas
            N_personas = str(len(faces_rect))

            if analyzing:
                # Analizar emociones de forma asíncrona
                percentage, emotion, emociones = await emotion_analize(faces_roi)
                emotion_log.append({"time": datetime.now().isoformat(), "emotion": emotion})
            else:
                emotion = 'Desconocida'
                percentage = '0'
                emociones = [0, 0, 0, 0, 0, 0, 0]

            # Enviar respuesta al WebSocket
            """Envía los resultados al WebSocket"""
            end_an = datetime.now()
            tiempo = str(end_an - start_an)

            data_to_send = {
                'emotion': emotion,
                'percentage': percentage,
                "NumeroPersonas": N_personas,
                'Tiempo': tiempo,
                'emociones': emociones}
            print('Hasta aqui si funciona')
            print('datos a enviar', data_to_send)
            await websocket.send_json(data_to_send)
        
        except Exception as e:
            print(f"Error procesando frame: {e}")


# WebSocket para procesar frames en tiempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global analyzing, emotion_log,start_an
    start_an = datetime.now()
    await websocket.accept()
    
    # Iniciar el proceso en segundo plano solo una vez
    asyncio.create_task(process_frames(WebSocket))

    while True:
        try:
            global face_location
            
            # Recibir frame en base64
            frame_data = await websocket.receive_text()
            await frame_queue.put(frame_data)  # Agregar frame a la cola

            # CODE
            # Procesar la detección en un hilo separado
            # loop = asyncio.get_running_loop()
            # faces_rect, faces_roi, Ubicacion = await loop.run_in_executor(executor, Deteccion, frame_data)
    
            # Detectar el rostro en caso de encontrarse
            #faces_rect, faces_roi, Ubicacion = await Deteccion(frame_data)
            
            # Asegurarse si exite la deteccion de una persona                    
            
            #N_personas = str(len(faces_rect)) 
            
            #response = {"x": Ubicacion[0], "y": Ubicacion[1], "w": Ubicacion[2], "h": Ubicacion[3]}             
            #response = Ubicacion
            #face_location = response
            
            #await websocket.send_json({"person_detect": value})
            
            #Reconocimiento de las emociones
            #Si se desea mas personas unir al bucle anterior

            #if analyzing and N_personas == '1':
            
            #if analyzing:
 
                # CODE
                # Crear una tarea en segundo plano para el análisis de emociones
                # task = asyncio.create_task(analizar_emocion(faces_roi, websocket, N_personas))

                # Espera de los datos de el analisis
            #    percentage, emotion, emociones = await emotion_analize(faces_roi)
            #    emotion_log.append({"time": datetime.now().isoformat(), "emotion": emotion})
                    
            #else:
            #    emotion = 'Desconocida'
            #    percentage = '0'
            #    emociones = [0,0,0,0,0,0,0]

                # CODE
                # Enviar respuesta sin análisis
                # await enviar_respuesta(websocket, emotion, percentage, N_personas, emociones)

            #end_an = datetime.now()
            #tiempo = str(end_an-start_an)
            #data_to_send = {'emotion':emotion,
            #               'percentage':percentage,
            #               "NumeroPersonas":N_personas,
            #               'Tiempo':tiempo,
            #               'emociones':emociones}   
            #await websocket.send_json(data_to_send)
            
            #return {"message": f"Rostro no encontrado {e}"}
                           
        except WebSocketDisconnect:
            print('Cliente Desconectado. Guardando Reporte.....')
            save_analysis("Archivo_Recuperado")
            break

        except Exception as e:
            print(f"Error en WebSocket: {e}")
            break
    
    #await websocket.close()

# Función para analizar la emoción en segundo plano
#async def analizar_emocion(faces_roi, websocket, N_personas):
#    loop = asyncio.get_running_loop()
#    percentage, emotion, emociones = await loop.run_in_executor(executor, emotion_analize, faces_roi)
#    
#    emotion_log.append({"time": datetime.now().isoformat(), "emotion": emotion})
#
#    await enviar_respuesta(websocket, emotion, percentage, N_personas, emociones)

# Función para enviar la respuesta al cliente
#async def enviar_respuesta(websocket, emotion, percentage, N_personas, emociones):
#    end_an = datetime.now()
#    tiempo = str(end_an - start_an)
#
#    data_to_send = {
#        'emotion': emotion,
#        'percentage': percentage,
#        "NumeroPersonas": N_personas,
#        'Tiempo': tiempo,
#        'emociones': emociones
#    }
#    await websocket.send_json(data_to_send)

@app.get("/face-location")
async def get_face_location():
    if face_location:
        print('La ubicacion registrada',face_location)
        return {"Ubicacion": face_location}
    return {"Ubicacion": []} 

#New Code
def analyze_emotions(emotion_log):
    analyzed_log = []
    last_emotion = None
    last_time = None
    abrupt_changes = 0

    for entry in emotion_log:
        time = datetime.strptime(entry["time"], "%Y-%m-%dT%H:%M:%S.%f")
        #time = datetime.strptime(entry["time"], "%H:%M:%S")
        emotion = entry["emotion"]
        
        # Detectar cambios abruptos de emoción
        abrupt_change = False
        if last_emotion and emotion != last_emotion:
            abrupt_change = True
            abrupt_changes += 1
        
        # Calcular duración entre registros
        duration = (time - last_time).total_seconds() if last_time else 0
        
        analyzed_log.append({
            "time": entry["time"],
            "emotion": emotion,
            "duration_since_last": duration,
            "abrupt_change": abrupt_change,
        })
        
        last_emotion = emotion
        last_time = time
    
    return analyzed_log, abrupt_changes

def generate_emotion_graph(report_path, analyzed_log):
    times = [entry["time"] for entry in analyzed_log]
    emotions = [entry["emotion"] for entry in analyzed_log]

    plt.figure(figsize=(10, 6))
    plt.plot(times, emotions, marker="o", linestyle="-", label="Emotions Over Time")
    plt.xlabel("Tiempo")
    plt.ylabel("Emociones")
    plt.title("Emociones Detectadas en el Tiempo")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    graph_path = report_path.replace(".csv", ".png")
    plt.savefig(graph_path)
    plt.close()

# Ruta para guardar análisis y reporte
@app.post("/save-analysis/")
async def save_analysis(
    video: UploadFile = File(...),
    patient_name: str = Form(...)
    ):
    
    global emotion_log,end_an
    
    Input_Name = patient_name.replace(" ", "_").replace("/", "_")  # Asegúrate de que el nombre sea válido para un archivo
    
    if not patient_name.strip():
        return {"message": "El nombre del paciente no puede estar vacío"}

    #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp = datetime.now().strftime("%d_%m_%Y")   
    
    report_path = f"/app/Archivos/Reportes/RP_{Input_Name}_{timestamp}.csv"
    video_path = f"/app/Archivos/Videos/VD_{Input_Name}_{timestamp}.webm"
    
    #video_path = f"Videos/{video.filename}"#captured_video.webm
    
    if not emotion_log:
        return {"message": "No hay datos para guardar"}
    
    
    # Guardar reporte en CSV
    #with open(report_path, mode="w", newline="") as file:
    #    writer = csv.DictWriter(file, fieldnames=["time", "emotion"])
    #    writer.writeheader()
    #    writer.writerows(emotion_log)
    analyzed_log, abrupt_changes = analyze_emotions(emotion_log)

    # Guardar reporte en CSV
    with open(report_path, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=["time", "emotion", "duration_since_last", "abrupt_change"]
        )
        writer.writeheader()
        writer.writerows(analyzed_log)
        #generate_emotion_graph(report_path, analyzed_log)   
    
    
    #Guardar video en webm
    try:
        file_content = await video.read()
        #print(f"Tipo de contenido: {video.content_type}")
        #print(f"El archivo recibido tiene {len(file_content)} bytes")
        
        if os.path.exists(video_path):
            #print(f'la ruta existente sera: {video_path}')
            with open(video_path, "wb") as f:
                f.write(file_content)
                
            #return {"message": f"Video guardado en {video_path}"}
            emotion_log = []  # Limpiar el log después de guardar
        else:
            with open(video_path, "wb") as f:
                f.write(file_content)
            #print(f'la ruta no existente sera: {video_path}')
                
            #return {"message": f"Video guardado en {video_path}"}
        emotion_log = []  # Limpiar el log después de guardar
                 
        return {"message": f"Reporte guardado en {report_path}, Video guardado en {video_path}"}
        
    except Exception as e:
        return {"message": f"Error al guardar el video: {str(e)}"}   

# Endpoint para guardar análisis y reporte
@app.post("/save-analysis-report/")
async def save_analysis(
    patient_name: str = Form(...)
    ):
    global emotion_log
    
    Input_Name = patient_name.replace(" ", "_").replace("/", "_")  # Asegúrate de que el nombre sea válido para un archivo
    
    if not patient_name.strip():
        return {"message": "El nombre del paciente no puede estar vacío"}

    #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp = datetime.now().strftime("%d_%m_%Y")   
    
    report_path = f"Archivos/Reportes/RP_{Input_Name}_{timestamp}.csv"
    
    #video_path = f"Videos/{video.filename}"#captured_video.webm
    
    if not emotion_log:
        return {"message": "No hay datos para guardar"}
    
    analyzed_log, abrupt_changes = analyze_emotions(emotion_log)

    # Guardar reporte en CSV
    try:
        with open(report_path, mode="w", newline="") as file:
            writer = csv.DictWriter(
                file, 
                fieldnames=["time", "emotion", "duration_since_last", "abrupt_change"]
            )
            writer.writeheader()
            writer.writerows(analyzed_log)
            emotion_log = []  # Limpiar el log después de guardar
                     
            return {"message": f"Reporte guardado en {report_path}"}
        
    except Exception as e:
        return {"message": f"Error al guardar el reporte: {str(e)}"}   

#    emotion_log = []  # Limpiar el log después de guardar
#    return {"message": f"Reporte guardado en {report_path}, Video guardado en {video_path}"}


#@app.post("/upload-video/")
#async def upload_video(video: UploadFile = File(...)):
#    video_path = f"videos/{video.filename}"
#    try:
#        with open(video_path, "wb") as f:
#            f.write(await video.read())
#        return {"message": f"Video guardado en {video_path}"}
#    except Exception as e:
#        return {"message": f"Error al guardar el video: {str(e)}"}


@app.get("/list-reports/")
async def list_reports():
    reports = os.listdir("/app/Archivos/Reportes/")
    videos = os.listdir("/app/Archivos/Videos/")
    return {"reports": reports, "videos": videos}


# Ruta donde se almacenan los reportes
REPORTS_DIR = Path("/app/Archivos/Reportes")

@app.get("/get-report/{report_name}")
async def get_report(report_name: str):
    report_path = REPORTS_DIR / report_name
    if not report_path.exists():
        return JSONResponse(status_code=404, content={"message": "Reporte no encontrado"})

    # Leer el archivo CSV y convertirlo a JSON
    df = pd.read_csv(report_path)
    return df.to_dict(orient="records")

from flask import Flask, request, jsonify, render_template
import face_recognition
import numpy as np
import base64
import cv2

app = Flask(__name__)

# Cargar imagen base
leonidas_img = face_recognition.load_image_file("leonidas.jpg")
leonidas_encoding = face_recognition.face_encodings(leonidas_img)[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    try:
        data = request.json
        img_data = base64.b64decode(data['imagen'])
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_img)
        if not encodings:
            return jsonify({"match": False, "mensaje": "No se detectó rostro"})

        current_encoding = encodings[0]
        distancia = face_recognition.face_distance([leonidas_encoding], current_encoding)[0]
        match = distancia < 0.5

        return jsonify({
            "match": bool(match),
            "distancia": float(distancia),
            "mensaje": "✅ Leonidas" if match else "❌ Otro rostro"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import propios
from YOLO.hackathonnasa import EnhanceBaldio
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

@app.route('/getImage', methods=['GET'])
def getImage():
    return send_file('static/imagen_concatenada.png', mimetype='image/png')

@app.route('/postGeminiPrompt', methods=['POST'])
def getPrompt():
    data = request.json
    prompt = data.get('prompt')
    genai.configure(api_key=propios.getGenLanModAPIkey())
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

@app.route('/process_coordinates', methods=['POST'])
def process_coordinates():
    data = request.json
    print(data)
    lat = data.get('lat')
    lng = data.get('lng')
    EnhanceBaldio(lat, lng)

    return jsonify({
        "lat" : lat,
        "lng" : lng})

@app.route('/getBaldio', methods=['POST'])
def getBaldios():
    if request.is_json:
        return send_file('static/imagen_concatenada.png', mimetype='image/png')
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
@app.route('/getHospitales', methods=['GET'])
def getHospitales():
    return jsonify({"url": "http://localhost:5000/static/kriggingHospitales.html"})
    
@app.route('/getIndustrial', methods=['GET'])
def getIndustrial():
    return jsonify({"url": "http://localhost:5000/static/kriggingIndustrial.html"})

@app.route('/getParques', methods=['GET'])
def getParques():
    return jsonify({"url": "http://localhost:5000/static/kriggingParques.html"})

if __name__ == '__main__':
    propios.kriggingParques()
    propios.kriggingIndustrial()
    propios.kriggingHospitales()
    
    app.run(debug=True)

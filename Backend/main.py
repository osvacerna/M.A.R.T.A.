from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import propios
from YOLO.hackathonnasa import EnhanceBaldio

app = Flask(__name__)
CORS(app)

@app.route('/getImage', methods=['GET'])
def getImage():
    return send_file('static/imagen_concatenada.png', mimetype='image/png')

@app.route('/process_coordinates', methods=['POST'])
def process_coordinates():
    data = request.json
    print(data)
    lat = data.get('lat')
    lng = data.get('lng')
    EnhanceBaldio(lat, lng)

    response_message = "hola" + str(lat+lng)
    print(response_message)
    return jsonify({
        "lat" : lat,
        "lng" : lng,
        "message": response_message})

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

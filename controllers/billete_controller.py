from flask import Blueprint, request, jsonify
from services.billete_service import BilleteService
from services.billete_service_pesos import BilleteServicePesos

billete_controller = Blueprint('billete_controller', __name__)

billete_service = BilleteService()
billete_servicePesos = BilleteServicePesos()


@billete_controller.route('/predictBillete', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    # Mapeo de las clases para billetes en pesos argentinos
    pesos_class_mapping = {
        0: 31,  1: 15,  2: 28,  3: 29,  4: 12,  5: 13,
        6: 24,  7: 23,  8: 25,  9: 8,  10: 7, 11: 9,
        12: 17, 13: 16, 14: 1,  15: 0, 16: 30, 17: 14,
        18: 26, 19: 10, 20: 19, 21: 18, 22: 3,  23: 2,
        24: 27, 25: 11, 26: 22, 27: 21, 28: 20, 29: 6,
        30: 5,  31: 4
    }
    
    # Mapeo de las clases para billetes en dólares
    usd_class_mapping = {
        32: 41,  # fifty-back
        33: 40,  # fifty-front
        34: 37,  # five-back
        35: 36,  # five-front
        36: 33,  # one-back
        37: 32,  # one-front
        38: 39,  # ten-back
        39: 38,  # ten-front
        40: 35,  # twenty-back
        41: 34   # twenty-front
    }
    
    try:
        # Obtener la predicción usando el servicio
        prediction = billete_service.predict(file)
        print("Prediction:", prediction)

        # Determinar el tipo de billete basado en la predicción
        if prediction in pesos_class_mapping:
            mapped_prediction = pesos_class_mapping[prediction]
        elif prediction in usd_class_mapping:
            mapped_prediction = usd_class_mapping[prediction]
        else:
            return jsonify({"error": "Invalid prediction returned"}), 500

        return jsonify({"prediction": mapped_prediction}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@billete_controller.route('/predictPesos', methods=['POST'])
def predictPesos():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
        # Mapeo de las clases de la predicción a los índices deseados
    class_mapping = {
        0: 31,  
        1: 15,   
        2: 28,   
        3: 29,  
        4: 12,  
        5: 13,
        6: 24,
        7: 23,
        8: 25,
        9: 8,
        10: 7,
        11: 9,
        12: 17,
        13: 16,
        14: 1,
        15: 0,
        16: 30,
        17: 14,
        18: 26,
        19: 10,
        20: 19,
        21: 18,
        22: 3,
        23: 2,
        24: 27,
        25: 11,
        26: 22,
        27: 21,
        28: 20,
        29: 6,
        30: 5,
        31: 4,

    }

    try:
        prediction = billete_servicePesos.predict(file)
        print(prediction)
        mapped_prediction = class_mapping.get(prediction, None)

        if mapped_prediction is not None:
            return jsonify({"prediction": mapped_prediction}), 200
        else:
            return jsonify({"error": "Invalid prediction returned"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


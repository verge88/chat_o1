from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)
client = Client("yuntian-deng/o1")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        # Обработка текстового ввода
        input_text = request.form.get('input_text', '') if request.method == 'POST' else request.args.get('input_text', '')

        if not input_text:
            return jsonify({'error': 'Missing required input_text'}), 400

        # Обработка файла, если предоставлен
        file = request.files.get('file')
        file_data = None
        if file:
            file_data = {'file': file, 'alt_text': file.filename}

        # Вызов модели через Gradio
        result = client.predict(
            inputs=input_text,
            top_p=1,
            temperature=1,
            chat_counter=0,
            chatbot=[file_data] if file_data else [],
            api_name="/predict"
        )

        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

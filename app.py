from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/report')
def get_report():
    try:
        with open('output/correlation_report.txt', 'r') as file:
            content = file.read()
        return jsonify({"report": content})
    except FileNotFoundError:
        return jsonify({"report": "Report not found. Run main.py first."}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
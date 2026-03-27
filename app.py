from flask import Flask, jsonify
import os, socket
app = Flask(__name__)
@app.route('/')
def hello():
    student_name = os.environ.get('STUDENT_NAME', 'Student')
    return f"<html><body><h1 style='color: green;'>Hello from Jenkins CI/CD Pipeline!</h1><p>Student: {student_name}</p><p>Hostname: {socket.gethostname()}</p></body></html>"
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "python-app"})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

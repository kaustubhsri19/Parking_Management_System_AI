"""
Simple test to check Flask app
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello! The Flask app is working!"

@app.route('/test')
def test():
    return "Test route is working!"

if __name__ == '__main__':
    print("🚀 Starting simple test app on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)


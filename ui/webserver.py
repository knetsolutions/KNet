from flask import Flask, request, render_template
from flask import jsonify
import sys

fname = "index.html"

# Rest Server
app = Flask(__name__)
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()

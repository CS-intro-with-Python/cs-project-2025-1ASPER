from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def home():
    return "Hi!"


@app.route('/user/<username>')
def get_user(username):
    return jsonify({"message": f"Hello, {username}!"})


@app.route('/search')
def search():
    q = request.args.get('q', '')
    return jsonify({"query": q, "length": len(q)})


if __name__ == '__main__':
    app.run(debug=True)

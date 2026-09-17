from flask import Flask, jsonify, request, send_from_directory

from kabum import buscar_kabum

app = Flask(__name__, static_folder="static")


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/buscar")
def api_buscar():
    produto = request.args.get("q", "").strip()
    if not produto:
        return jsonify({"erro": "informe o parametro q"}), 400

    try:
        resultados = buscar_kabum(produto)
    except Exception as exc:
        return jsonify({"erro": str(exc)}), 502

    return jsonify(resultados)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

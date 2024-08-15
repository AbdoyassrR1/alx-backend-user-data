#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_payload():
    """get JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def add_user():
    """ create new user """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """ login the user """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    is_valid = AUTH.valid_login(email, password)
    if not is_valid:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})

    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status."""
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)

    if user_cookie is None or user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("profile", methods=["GET"])
def profile() -> str:
    """  If the user exist,'
    respond with a 200 HTTP status and the following JSON payload:"""
    session_id_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id_cookie)
    if session_id_cookie is None or user is None:
        abort(403)

    jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, jsonify, request, abort, redirect, url_for
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
def login():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout the user"""
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)

    if user_cookie is None or user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")

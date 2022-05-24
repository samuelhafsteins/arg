"""
PEWPEW
"""

import os
import re
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request

from store import Store
from dns import DNS

store = Store()

app = Flask(__name__)

load_dotenv()


@app.route("/api/v1/")
def show_size():
    """
    Shows the size of the key value store on the root path for the v1 of the API.
    """
    return f"There are {store.size()} domains in the DNS store!", 200


@app.route("/api/v1/lookup/<domain>", methods=["POST"])
def create_domain(domain):
    """
    Takes in an domain name, validates it and then checks if the DNS
    has been resolved recently.
    """
    cached = store.read(domain)
    if cached:
        return cached.lookup(), 200

    dns = DNS(domain)
    res = dns.lookup()
    store.create(domain, dns)
    return f"Results: {res}", 200


@app.route("/api/v1/lookup/<domain>", methods=["GET"])
def read_domain(domain):
    """
    Checks if the domain in is in the cache and that the cache is valid,
    if so, it returns the IP address for that domain.
    """
    cached = store.read(domain)
    if cached:
        if request.args.get("debug") == "true":
            return cached.debug(), 200

        if cached.valid_cache():
            return cached.lookup(), 200

    return "ERR - Cache not found or is invalid", 400


@app.route("/api/v1/lookup/<domain>", methods=["DEL"])
def delete_domain(domain):
    """
    Removes the cached results from the cache.
    """
    deleted = store.delete(domain)
    if deleted:
        return f"{domain} deleted from cache", 200

    return "ERR - domain not found in cache", 400


@app.route("/api/v1/lookup/<domain>", methods=["PUT"])
def update_domain(domain):
    """
    Updates the cache for the domain.
    """
    cached = store.read(domain)
    if cached:
        cached.update(request.args)
        return f"{domain} updated", 200

    return "ERR - domain not found in cache", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

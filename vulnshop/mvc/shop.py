"""Storefront pages."""
from flask import Blueprint, render_template, request
from ..db import query_all, query_one

bp = Blueprint("shop", __name__)


@bp.get("/")
@bp.get("/shop")
def index():
    return render_template("shop/index.html",
                           products=query_all("SELECT * FROM products"))


@bp.get("/shop/product/<int:pid>")
def product(pid):
    return render_template("shop/product.html",
                           product=query_one("SELECT * FROM products WHERE id = ?", (pid,)))

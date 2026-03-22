#!/usr/bin/env python3
"""Langlaw — Flask web server."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv, set_key, dotenv_values
from flask import Flask, jsonify, render_template, request

ENV_PATH = ROOT / ".env"
load_dotenv(ENV_PATH)

app = Flask(__name__)

_KEY_FIELDS = ["OPENAI_API_KEY", "OC_ID"]


@app.route("/api/settings", methods=["GET"])
def settings_get():
    current = dotenv_values(ENV_PATH) if ENV_PATH.exists() else {}
    return jsonify({
        k: bool(current.get(k, "").strip()) for k in _KEY_FIELDS
    })


@app.route("/api/settings", methods=["POST"])
def settings_post():
    body = request.get_json(silent=True) or {}
    if not ENV_PATH.exists():
        ENV_PATH.touch()
    changed = False
    for k in _KEY_FIELDS:
        val = (body.get(k) or "").strip()
        if val:
            set_key(str(ENV_PATH), k, val)
            os.environ[k] = val
            changed = True
    load_dotenv(ENV_PATH, override=True)
    return jsonify({"ok": True, "changed": changed})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    body = request.get_json(silent=True) or {}
    case_description = (body.get("case_description") or "").strip()

    if not case_description:
        return jsonify({"error": "사건 설명을 입력해 주세요."}), 400

    try:
        from src.legal_reasoner import analyze_case
        result = analyze_case(case_description)
        return jsonify({
            "keywords": result["keywords"],
            "cases": result["cases"],
            "laws": [
                {
                    "조문번호": l.get("조문번호", ""),
                    "제목": l.get("제목", ""),
                    "내용": l.get("내용", "")[:300],
                }
                for l in result["laws"]
            ],
            "judgment": result["judgment"],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

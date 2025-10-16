# llm_client.py — v4 (robuste) : Responses → Tools → Chat(json)
from __future__ import annotations
import json, os, re
from typing import Any, Dict, Optional
from openai import OpenAI

# .env (facultatif)
try:
    from dotenv import load_dotenv; load_dotenv()
except Exception:
    pass

# ---------- Config ----------
_API_KEY = os.getenv("OPENAI_API_KEY")      # <— clé standard
if not _API_KEY:
    raise RuntimeError("OPENAI_API_KEY manquante (mets-la dans .env).")
_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_BASE_URL = os.getenv("OPENAI_BASE_URL") or None
DEBUG = os.getenv("DEBUG_LLM", "0") == "1"
RETURN_STUB_IF_FAIL = os.getenv("LLM_RETURN_STUB_IF_FAIL", "0") == "1"

client = OpenAI(api_key=_API_KEY, base_url=_BASE_URL) if _BASE_URL else OpenAI(api_key=_API_KEY)

FAMILY_JSON_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "sexe": {"type": "string", "enum": ["H", "F", "Inconnu"]},
            "parent": {"type": "array", "items": {"type": "string"}, "default": []},
            "enfants": {"type": "array", "items": {"type": "string"}, "default": []},
            "conjoint": {"type": "string", "default": ""}
        },
        "required": ["sexe", "parent", "enfants", "conjoint"],
        "additionalProperties": False
    }
}

def _log(s: str): 
    if DEBUG: print(f"[LLM] {s}")

def _first_text_from_responses(resp) -> str:
    try:
        parsed = getattr(resp, "output_parsed", None)
        if parsed is not None:
            return json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
        parts = []
        for item in (resp.output or []):
            for c in getattr(item, "content", []) or []:
                if getattr(c, "type", "") == "output_text":
                    parts.append(c.text)
        return "".join(parts).strip()
    except Exception as e:
        _log(f"responses parse err: {e}")
        return ""

def _safe_load_json(text: str) -> Optional[Dict[str, Any]]:
    if not text: return None
    try:
        return json.loads(text)
    except Exception:
        pass
    try:
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if m: return json.loads(m.group(0))
    except Exception:
        pass
    return None

def _normalize(data: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for person, info in (data or {}).items():
        if not isinstance(info, dict): continue
        out[person] = {
            "sexe": (info.get("sexe") or "Inconnu"),
            "parent": (info.get("parent") or []),
            "enfants": (info.get("enfants") or []),
            "conjoint": (info.get("conjoint") or ""),
        }
    return out

_SYSTEM = (
    "Tu es un extracteur d'informations généalogiques. "
    "À partir d'un avis généalogique selon la langue de l'utilisateur, retourne UNIQUEMENT un objet JSON"
    " conforme èa l'avis. "
    "Chaque clé = nom complet d'une personne apparaissant dans le texte."
    "Si pour une personne donnée, il apparait uniquement son prénom, et que le nom de son père est connu, attribue-lui le nom de son père."
    "N'invente pas; si inconnu, mets sexe='Inconnu', parent=[], enfants=[], conjoint=''. "
    "Le résultat ne doit contenir que le JSON, sans texte autour."
)

def extract_family_json(obituary_text: str, temperature: float = 0.1, max_output_tokens: int = 2048) -> str:
    if not obituary_text or not obituary_text.strip():
        _log("input vide -> {}"); return "{}"
    _log(f"Model: {_MODEL}")

    # --- Tentative 1: Responses API + json_schema
    try:
        _log("Responses + json_schema…")
        resp = client.responses.create(
            model=_MODEL,
            input=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": obituary_text},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "family_schema", "schema": FAMILY_JSON_SCHEMA, "strict": True},
            },
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        text = _first_text_from_responses(resp)
        data = _safe_load_json(text) or getattr(resp, "output_parsed", None)
        if isinstance(data, dict):
            out = json.dumps(_normalize(data), ensure_ascii=False, separators=(",", ":"))
            _log("Responses OK"); return out
        _log("Responses non-dict → tools…")
    except Exception as e:
        _log(f"Responses ERROR: {e} → tools…")

    # --- Tentative 2: Chat Completions + TOOLS (function calling)
    try:
        _log("Chat tools(function calling)…")
        comp = client.chat.completions.create(
            model=_MODEL,
            temperature=temperature,
            tools=[{
                "type": "function",
                "function": {
                    "name": "set_family",
                    "description": "Renvoyer l'objet JSON du graphe familial.",
                    "parameters": FAMILY_JSON_SCHEMA,
                },
            }],
            tool_choice={"type": "function", "function": {"name": "set_family"}},
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": obituary_text},
            ],
        )
        calls = comp.choices[0].message.tool_calls if comp.choices else None
        if calls:
            args = calls[0].function.arguments
            data = _safe_load_json(args)
            if isinstance(data, dict):
                out = json.dumps(_normalize(data), ensure_ascii=False, separators=(",", ":"))
                _log("Tools OK"); return out
        _log("Tools sans args → json_object…")
    except Exception as e:
        _log(f"Tools ERROR: {e} → json_object…")

    # --- Tentative 3: Chat Completions + json_object
    try:
        _log("Chat json_object…")
        comp = client.chat.completions.create(
            model=_MODEL,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": obituary_text},
            ],
        )
        content = comp.choices[0].message.content if comp.choices else ""
        data = _safe_load_json(content)
        if isinstance(data, dict):
            out = json.dumps(_normalize(data), ensure_ascii=False, separators=(",", ":"))
            _log("Chat OK"); return out
        _log("Chat non-dict")
    except Exception as e:
        _log(f"Chat ERROR: {e}")

    if RETURN_STUB_IF_FAIL:
        _log("Stub renvoyé (LLM_RETURN_STUB_IF_FAIL=1)")
        stub = {"Défunt": {"sexe": "Inconnu", "parent": [], "enfants": [], "conjoint": ""}}
        return json.dumps(stub, ensure_ascii=False, separators=(",", ":"))

    _log("Échec → {}")
    return "{}"

def quick_healthcheck() -> str:
    try:
        r = client.responses.create(model=_MODEL, input="OK", temperature=0)
        t = _first_text_from_responses(r)
        return "OK" if "OK" in (t or "OK").upper() else (t or "OK")
    except Exception:
        pass
    try:
        c = client.chat.completions.create(model=_MODEL, messages=[{"role":"user","content":"OK"}], temperature=0)
        msg = c.choices[0].message.content if c.choices else ""
        return "OK" if "OK" in (msg or "OK").upper() else (msg or "OK")
    except Exception as e:
        return f"ERREUR: {e}"

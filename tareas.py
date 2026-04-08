import json
import os
from pathlib import Path

_JSON_FILE = Path(__file__).resolve().parent / "tareas.json"

_tareas: list[dict] = []
_siguiente_id: int = 1


def _cargar() -> None:
    global _tareas, _siguiente_id
    _tareas = []
    _siguiente_id = 1
    if not _JSON_FILE.is_file():
        return
    try:
        with open(_JSON_FILE, encoding="utf-8") as f:
            data = json.load(f)
        _tareas = data["tareas"]
        _siguiente_id = int(data["siguiente_id"])
        for t in _tareas:
            t.setdefault("completada", False)
        if _tareas:
            max_id = max(int(x["id"]) for x in _tareas)
            if _siguiente_id <= max_id:
                _siguiente_id = max_id + 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        _tareas = []
        _siguiente_id = 1


def _guardar() -> None:
    payload = {"siguiente_id": _siguiente_id, "tareas": _tareas}
    tmp = _JSON_FILE.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, _JSON_FILE)


_cargar()


def agregar_tarea(texto: str) -> int | None:
    global _siguiente_id
    limpio = (texto or "").strip()
    if not limpio:
        return None
    tid = _siguiente_id
    _siguiente_id += 1
    _tareas.append({"id": tid, "texto": limpio, "completada": False})
    _guardar()
    return tid


def completar_tarea(id: int) -> bool:
    for t in _tareas:
        if t["id"] == id:
            t["completada"] = True
            _guardar()
            return True
    return False


def listar_tareas() -> list[dict]:
    return list(_tareas)

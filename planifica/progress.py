from __future__ import annotations

from typing import Any


def _filled(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, dict):
        return any(_filled(v) for v in value.values())
    return bool(value)


def module_completion(payload: dict) -> dict[str, float]:
    org = payload.get("org") or {}
    pei = payload.get("pei") or {}
    pg = payload.get("proyecto_guia") or {}
    pq = payload.get("proyecto_preguntas") or {}
    dafo = payload.get("dafo") or {}
    cim = payload.get("cimientos") or {}
    rend = payload.get("rendimiento") or {}
    rrhh = payload.get("rrhh") or {}
    vol = payload.get("voluntarios") or {}

    def ratio(keys: list[str], src: dict) -> float:
        if not keys:
            return 0.0
        ok = sum(1 for k in keys if _filled(src.get(k)))
        return ok / len(keys)

    checks = list(pq.values())
    check_ratio = sum(1 for c in checks if c) / len(checks) if checks else 0.0

    return {
        "organizacion": ratio(
            ["nombre", "tipo", "pais", "contacto_nombre", "contacto_email"],
            org,
        ),
        "pei": ratio(["nombre", "periodo", "version", "aprobado_por"], pei),
        "proyectos": (
            ratio(["nombre", "objetivo", "vinculo_estrategico", "criterios_exito"], pg)
            + check_ratio
        )
        / 2,
        "dafo": ratio(["fortalezas", "debilidades", "oportunidades", "amenazas"], dafo),
        "cimientos": ratio(["vision", "mision", "valores"], cim),
        "prioridades": 1.0
        if _filled(payload.get("prioridades")) and _filled(payload.get("objetivos_smart"))
        else (0.5 if _filled(payload.get("prioridades")) or _filled(payload.get("objetivos_smart")) else 0.0),
        "acciones": 1.0 if _filled(payload.get("acciones")) else 0.0,
        "rendimiento": (
            (0.4 if any(str((a or {}).get("kpi") or "").strip() for a in (payload.get("acciones") or [])) else 0.0)
            + (0.3 if _filled(rend.get("frecuencia_evaluacion")) else 0.0)
            + (0.3 if _filled(rend.get("informes_comite")) else 0.0)
        ),
        "personas": (ratio(["roles_clave", "brechas_formacion"], rrhh) + ratio(["necesidades", "formacion"], vol)) / 2,
        "actividades": 1.0 if _filled(payload.get("actividades")) else 0.0,
        "tablero": 1.0
        if any(
            str(a.get("estado") or "") in {"Planificada", "En curso", "Cumplida"}
            and str(a.get("titulo") or "").strip()
            for a in (payload.get("actividades") or [])
        )
        else 0.0,
    }


def total_completion(payload: dict) -> float:
    parts = module_completion(payload)
    if not parts:
        return 0.0
    return sum(parts.values()) / len(parts)

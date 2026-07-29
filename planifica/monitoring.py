"""Monitoreo de actividades vinculadas al PEI (tablero integrado)."""

from __future__ import annotations

from typing import Any

import pandas as pd

ESTADOS = ["Borrador", "Planificada", "En curso", "Cumplida", "Suspendida"]
ESTADOS_TABLERO = {"Planificada", "En curso", "Cumplida"}


def empty_actividad() -> dict[str, Any]:
    return {
        "id": "",
        "titulo": "",
        "prioridad": "",
        "objetivo": "",
        "accion_pei": "",
        "responsable": "",
        "periodo": "",
        "fecha_inicio": "",
        "fecha_fin": "",
        "estado": "Planificada",
        "kpi_nombre": "",
        "meta": 0.0,
        "avance": 0.0,
        "unidad": "",
        "notas": "",
    }


def parse_lines(text: str) -> list[str]:
    lines = []
    for raw in (text or "").splitlines():
        line = raw.strip().lstrip("0123456789.-) ").strip()
        if line:
            lines.append(line)
    return lines


def priority_options(payload: dict[str, Any]) -> list[str]:
    opts = parse_lines(payload.get("prioridades") or "")
    for a in payload.get("acciones") or []:
        p = str(a.get("prioridad") or "").strip()
        if p and p not in opts:
            opts.append(p)
    return opts or ["General"]


def objective_options(payload: dict[str, Any]) -> list[str]:
    return parse_lines(payload.get("objetivos_smart") or "") or ["Sin objetivo definido"]


def action_options(payload: dict[str, Any]) -> list[str]:
    """Acciones del módulo 6 (y ya usadas en actividades), sin vacíos ni duplicados."""
    opts: list[str] = []
    seen: set[str] = set()

    def add(value: Any) -> None:
        text = str(value or "").strip()
        if text and text not in seen:
            seen.add(text)
            opts.append(text)

    for a in payload.get("acciones") or []:
        add(a.get("accion"))
    for a in payload.get("actividades") or []:
        add(a.get("accion_pei"))
    return opts


def kpis_from_acciones(payload: dict[str, Any]) -> list[str]:
    """KPI únicos del plan de acción (fuente única de indicadores)."""
    opts: list[str] = []
    seen: set[str] = set()
    for a in payload.get("acciones") or []:
        text = str(a.get("kpi") or "").strip()
        if text and text not in seen:
            seen.add(text)
            opts.append(text)
    return opts


def sync_kpis_from_acciones(payload: dict[str, Any]) -> list[str]:
    """Copia los KPI del plan de acción al bloque rendimiento (sin duplicar definición)."""
    kpis = kpis_from_acciones(payload)
    rend = payload.setdefault("rendimiento", {})
    rend["kpis"] = "\n".join(kpis)
    return kpis


def kpi_options(payload: dict[str, Any]) -> list[str]:
    """KPI del plan de acción y de actividades ya cargadas."""
    opts: list[str] = []
    seen: set[str] = set()

    def add(value: Any) -> None:
        text = str(value or "").strip()
        if not text:
            return
        parts = [p.strip() for p in text.replace(";", "\n").split("·")]
        for part in parts:
            for line in parse_lines(part):
                if line and line not in seen:
                    seen.add(line)
                    opts.append(line)

    for kpi in kpis_from_acciones(payload):
        add(kpi)
    for a in payload.get("actividades") or []:
        add(a.get("kpi_nombre"))
    return opts


def actividades_visibles(payload: dict[str, Any], *, solo_tablero: bool = False) -> list[dict[str, Any]]:
    rows = payload.get("actividades") or []
    out = []
    for a in rows:
        if not str(a.get("titulo") or "").strip():
            continue
        estado = str(a.get("estado") or "Borrador")
        if solo_tablero and estado not in ESTADOS_TABLERO:
            continue
        out.append(a)
    return out


def _num(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def dashboard_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    all_acts = actividades_visibles(payload, solo_tablero=False)
    board = actividades_visibles(payload, solo_tablero=True)
    by_estado: dict[str, int] = {e: 0 for e in ESTADOS}
    for a in all_acts:
        est = str(a.get("estado") or "Borrador")
        by_estado[est] = by_estado.get(est, 0) + 1

    progreso_items = []
    for a in board:
        meta = _num(a.get("meta"))
        avance = _num(a.get("avance"))
        pct = (avance / meta * 100.0) if meta > 0 else (100.0 if str(a.get("estado")) == "Cumplida" else 0.0)
        progreso_items.append(min(pct, 150.0))

    avance_global = sum(progreso_items) / len(progreso_items) if progreso_items else 0.0
    cumplidas = by_estado.get("Cumplida", 0)
    en_curso = by_estado.get("En curso", 0)
    planificadas = by_estado.get("Planificada", 0)

    return {
        "total": len(all_acts),
        "en_tablero": len(board),
        "avance_global": round(avance_global, 1),
        "cumplidas": cumplidas,
        "en_curso": en_curso,
        "planificadas": planificadas,
        "borrador": by_estado.get("Borrador", 0),
        "by_estado": by_estado,
    }


def df_por_estado(payload: dict[str, Any]) -> pd.DataFrame:
    m = dashboard_metrics(payload)
    rows = [{"Estado": k, "Cantidad": v} for k, v in m["by_estado"].items() if v > 0]
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["Estado", "Cantidad"])


def df_por_prioridad(payload: dict[str, Any]) -> pd.DataFrame:
    board = actividades_visibles(payload, solo_tablero=True)
    agg: dict[str, dict[str, float]] = {}
    for a in board:
        key = str(a.get("prioridad") or "Sin prioridad").strip() or "Sin prioridad"
        bucket = agg.setdefault(key, {"Actividades": 0, "Meta": 0.0, "Avance": 0.0})
        bucket["Actividades"] += 1
        bucket["Meta"] += _num(a.get("meta"))
        bucket["Avance"] += _num(a.get("avance"))
    rows = []
    for prioridad, vals in agg.items():
        meta = vals["Meta"]
        avance = vals["Avance"]
        pct = (avance / meta * 100.0) if meta > 0 else 0.0
        rows.append(
            {
                "Prioridad": prioridad,
                "Actividades": int(vals["Actividades"]),
                "Meta": meta,
                "Avance": avance,
                "% cumplimiento": round(min(pct, 150.0), 1),
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=["Prioridad", "Actividades", "Meta", "Avance", "% cumplimiento"]
    )


def df_actividades_tabla(payload: dict[str, Any], *, solo_tablero: bool = True) -> pd.DataFrame:
    rows = []
    for a in actividades_visibles(payload, solo_tablero=solo_tablero):
        meta = _num(a.get("meta"))
        avance = _num(a.get("avance"))
        pct = (avance / meta * 100.0) if meta > 0 else (100.0 if a.get("estado") == "Cumplida" else 0.0)
        rows.append(
            {
                "Actividad": a.get("titulo") or "",
                "Prioridad": a.get("prioridad") or "",
                "Objetivo": a.get("objetivo") or "",
                "Responsable": a.get("responsable") or "",
                "Período": a.get("periodo") or "",
                "Estado": a.get("estado") or "",
                "KPI": a.get("kpi_nombre") or "",
                "Meta": meta,
                "Avance": avance,
                "%": round(min(pct, 150.0), 1),
                "Unidad": a.get("unidad") or "",
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=[
            "Actividad",
            "Prioridad",
            "Objetivo",
            "Responsable",
            "Período",
            "Estado",
            "KPI",
            "Meta",
            "Avance",
            "%",
            "Unidad",
        ]
    )


def df_kpi_meta_avance(payload: dict[str, Any]) -> pd.DataFrame:
    board = actividades_visibles(payload, solo_tablero=True)
    rows = []
    for a in board:
        kpi = str(a.get("kpi_nombre") or a.get("titulo") or "").strip()
        if not kpi:
            continue
        rows.append(
            {
                "KPI / actividad": kpi[:48],
                "Meta": _num(a.get("meta")),
                "Avance": _num(a.get("avance")),
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["KPI / actividad", "Meta", "Avance"])

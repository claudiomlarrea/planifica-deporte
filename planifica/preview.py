"""Vista previa del PEI con componentes nativos de Streamlit (sin HTML)."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from planifica.surveys import list_configured_surveys


def _txt(value: Any) -> str:
    text = str(value or "").strip()
    return text if text else "—"


def _block(label: str, value: Any) -> None:
    st.markdown(f"**{label}**")
    st.text(_txt(value))


def render_plan_preview(title: str, payload: dict[str, Any]) -> None:
    org = payload.get("org") or {}
    pei = payload.get("pei") or {}
    pg = payload.get("proyecto_guia") or {}
    dafo = payload.get("dafo") or {}
    cim = payload.get("cimientos") or {}
    rend = payload.get("rendimiento") or {}
    rrhh = payload.get("rrhh") or {}
    vol = payload.get("voluntarios") or {}
    pei_titulo = pei.get("nombre") or title
    pais = org.get("pais") or org.get("region") or "—"
    provincia = org.get("provincia") or ""
    ubicacion = f"{pais}" + (f" · {provincia}" if provincia else "")

    st.markdown(f"## {pei_titulo}")
    st.caption("Primer Plan Estratégico Institucional")

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"**Organización**\n\n{_txt(org.get('nombre'))}")
    m2.markdown(f"**Tipo**\n\n{_txt(org.get('tipo'))}")
    m3.markdown(f"**Ubicación**\n\n{_txt(ubicacion)}")
    m4.markdown(f"**Horizonte**\n\n{_txt(org.get('horizonte_anios'))} años")

    st.markdown("### Identidad del PEI")
    _block("Nombre", pei_titulo)
    _block("Período", pei.get("periodo"))
    _block("Versión", pei.get("version"))
    _block("Quién lo aprobará", pei.get("aprobado_por"))
    _block("Fecha de aprobación", pei.get("fecha_aprobacion"))

    st.markdown("### 1 · Análisis DAFO")
    c1, c2 = st.columns(2)
    with c1:
        _block("Fortalezas", dafo.get("fortalezas"))
        _block("Oportunidades", dafo.get("oportunidades"))
    with c2:
        _block("Debilidades", dafo.get("debilidades"))
        _block("Amenazas", dafo.get("amenazas"))

    st.markdown("### 2 · Visión, misión y valores")
    _block("Visión", cim.get("vision"))
    _block("Misión", cim.get("mision"))
    _block("Valores", cim.get("valores"))

    st.markdown("### 3 · Prioridades y objetivos")
    _block("Prioridades estratégicas", payload.get("prioridades"))
    _block("Objetivos SMART", payload.get("objetivos_smart"))

    st.markdown("### 4 · Plan de acción")
    acciones = payload.get("acciones") or []
    rows = []
    for a in acciones:
        if not any(str(a.get(k) or "").strip() for k in ("accion", "responsable", "plazo", "kpi")):
            continue
        rows.append(
            {
                "Prioridad": a.get("prioridad") or "",
                "Acción": a.get("accion") or "",
                "Responsable": a.get("responsable") or "",
                "Plazo": a.get("plazo") or "",
                "KPI": a.get("kpi") or "",
                "Recursos": a.get("recursos") or "",
                "Estado": a.get("estado") or "",
            }
        )
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.caption("Sin acciones registradas.")

    st.markdown("### 5 · Evaluación e informes")
    _block("Indicadores del plan de acción (KPI)", rend.get("kpis"))
    _block("Frecuencia de evaluación", rend.get("frecuencia_evaluacion"))
    _block("Informes al comité", rend.get("informes_comite"))

    st.markdown("### 6 · Recursos humanos y voluntarios")
    _block("Roles clave", rrhh.get("roles_clave"))
    _block("Brechas de formación", rrhh.get("brechas_formacion"))
    _block("Reclutamiento", rrhh.get("reclutamiento"))
    _block("Necesidades de voluntariado", vol.get("necesidades"))
    _block("Motivaciones", vol.get("motivaciones"))
    _block("Formación", vol.get("formacion"))
    _block("Reconocimiento", vol.get("reconocimiento"))

    st.markdown("### 7 · Primer proyecto (opcional)")
    _block("Proyecto", pg.get("nombre"))
    _block("Objetivo", pg.get("objetivo"))
    _block("Contribuye al PEI en", pg.get("vinculo_estrategico"))
    _block("Criterios de éxito", pg.get("criterios_exito"))

    acts = payload.get("actividades") or []
    visibles = [a for a in acts if str(a.get("titulo") or "").strip()]
    if visibles:
        st.markdown("### 8 · Actividades de ejecución")
        rows = []
        for a in visibles:
            rows.append(
                {
                    "Actividad": a.get("titulo") or "",
                    "Prioridad": a.get("prioridad") or "",
                    "Estado": a.get("estado") or "",
                    "Meta": a.get("meta") or 0,
                    "Avance": a.get("avance") or 0,
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    surveys = list_configured_surveys(payload)
    if surveys:
        st.markdown("### 10 · Encuestas de consulta")
        for s in surveys:
            dest = f" · {s['destinatarios']}" if s.get("destinatarios") else ""
            st.markdown(f"- **{s['etiqueta']}**: {s['url']}{dest}")

    st.caption("Generado con Rumbo Deporte · Manual COI (2020), Unidades 53–57")

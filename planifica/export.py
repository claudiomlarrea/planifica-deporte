from __future__ import annotations

import html
import json
from typing import Any


def _line(label: str, value: str) -> str:
    v = (value or "").strip()
    return f"### {label}\n{v if v else '—'}\n\n"


def _esc(value: Any) -> str:
    return html.escape(str(value or "").strip() or "—")


def _block(label: str, value: Any) -> str:
    text = str(value or "").strip() or "—"
    if text == "—":
        paragraphs = "<p class='pd-empty'>—</p>"
    else:
        paragraphs = "".join(
            f"<p>{html.escape(line)}</p>" if line.strip() else "<br/>"
            for line in text.splitlines()
        )
    return f"""
    <div class="pd-field">
      <div class="pd-field-label">{html.escape(label)}</div>
      <div class="pd-field-body">{paragraphs}</div>
    </div>
    """


def plan_to_html(title: str, payload: dict[str, Any]) -> str:
    """Vista previa tipográfica del plan (HTML), no Markdown crudo."""
    org = payload.get("org") or {}
    pei = payload.get("pei") or {}
    pg = payload.get("proyecto_guia") or {}
    dafo = payload.get("dafo") or {}
    cim = payload.get("cimientos") or {}
    rend = payload.get("rendimiento") or {}
    rrhh = payload.get("rrhh") or {}
    vol = payload.get("voluntarios") or {}
    tech = payload.get("tecnologia") or {}
    acciones = payload.get("acciones") or []

    pais = org.get("pais") or org.get("region") or "—"
    provincia = org.get("provincia") or ""
    ubicacion = f"{pais}" + (f" · {provincia}" if provincia else "")
    pei_titulo = pei.get("nombre") or title

    meta = f"""
    <div class="pd-meta">
      <div><span>Organización</span><strong>{_esc(org.get('nombre'))}</strong></div>
      <div><span>Tipo</span><strong>{_esc(org.get('tipo'))}</strong></div>
      <div><span>Ubicación</span><strong>{_esc(ubicacion)}</strong></div>
      <div><span>Horizonte</span><strong>{_esc(org.get('horizonte_anios'))} años</strong></div>
    </div>
    """

    pei_block = f"""
      <h3>Plan Estratégico Institucional</h3>
      {_block("Nombre del PEI", pei_titulo)}
      {_block("Período", pei.get("periodo"))}
      {_block("Versión", pei.get("version"))}
      {_block("Aprobado por", pei.get("aprobado_por"))}
      {_block("Fecha de aprobación", pei.get("fecha_aprobacion"))}
    """

    if acciones:
        rows = []
        for a in acciones:
            if not any(str(a.get(k) or "").strip() for k in ("accion", "responsable", "plazo", "kpi")):
                continue
            rows.append(
                "<tr>"
                f"<td>{_esc(a.get('prioridad'))}</td>"
                f"<td>{_esc(a.get('accion'))}</td>"
                f"<td>{_esc(a.get('responsable'))}</td>"
                f"<td>{_esc(a.get('plazo'))}</td>"
                f"<td>{_esc(a.get('kpi'))}</td>"
                f"<td>{_esc(a.get('estado'))}</td>"
                "</tr>"
            )
        acciones_html = (
            """
            <table class="pd-table">
              <thead>
                <tr>
                  <th>Prioridad</th><th>Acción</th><th>Responsable</th>
                  <th>Plazo</th><th>KPI</th><th>Estado</th>
                </tr>
              </thead>
              <tbody>
            """
            + ("".join(rows) if rows else "<tr><td colspan='6'>Sin acciones registradas.</td></tr>")
            + "</tbody></table>"
        )
    else:
        acciones_html = "<p class='pd-empty'>Sin acciones registradas.</p>"

    return f"""
    <div class="pd-doc">
      <div class="pd-doc-header">
        <div class="pd-doc-badge">Plan Estratégico Institucional</div>
        <h2>{_esc(pei_titulo)}</h2>
      </div>
      {meta}
      {pei_block}
      <h3>1 · Gestión de proyectos</h3>
      {_block("Proyecto emblemático", pg.get("nombre"))}
      {_block("Objetivo", pg.get("objetivo"))}
      {_block("Vínculo con el PEI", pg.get("vinculo_estrategico"))}
      {_block("Criterios de éxito", pg.get("criterios_exito"))}
      <h3>2 · Análisis DAFO</h3>
      <div class="pd-grid-2">
        {_block("Fortalezas", dafo.get("fortalezas"))}
        {_block("Debilidades", dafo.get("debilidades"))}
        {_block("Oportunidades", dafo.get("oportunidades"))}
        {_block("Amenazas", dafo.get("amenazas"))}
      </div>
      <h3>3 · Cimientos estratégicos</h3>
      {_block("Visión", cim.get("vision"))}
      {_block("Misión", cim.get("mision"))}
      {_block("Valores", cim.get("valores"))}
      <h3>4 · Prioridades y objetivos</h3>
      {_block("Prioridades estratégicas", payload.get("prioridades"))}
      {_block("Objetivos SMART", payload.get("objetivos_smart"))}
      <h3>5 · Plan de acción</h3>
      {acciones_html}
      <h3>6 · Gestión del rendimiento</h3>
      {_block("Indicadores (KPI)", rend.get("kpis"))}
      {_block("Frecuencia de evaluación", rend.get("frecuencia_evaluacion"))}
      {_block("Informes al comité", rend.get("informes_comite"))}
      <h3>7 · Recursos humanos</h3>
      {_block("Roles clave", rrhh.get("roles_clave"))}
      {_block("Brechas de formación", rrhh.get("brechas_formacion"))}
      {_block("Reclutamiento", rrhh.get("reclutamiento"))}
      <h3>8 · Voluntarios y formación</h3>
      {_block("Necesidades", vol.get("necesidades"))}
      {_block("Motivaciones", vol.get("motivaciones"))}
      {_block("Formación", vol.get("formacion"))}
      {_block("Reconocimiento", vol.get("reconocimiento"))}
      <h3>9 · Tecnología e IA</h3>
      {_block("Notas", tech.get("notas_ia"))}
      <div class="pd-doc-footer">
        Manual de Administración Deportiva, COI (2020) · Unidades 53–57 · Generado con PlanificaDeporte
      </div>
    </div>
    """


def plan_to_markdown(title: str, payload: dict[str, Any]) -> str:
    org = payload.get("org") or {}
    pei = payload.get("pei") or {}
    pg = payload.get("proyecto_guia") or {}
    dafo = payload.get("dafo") or {}
    cim = payload.get("cimientos") or {}
    rend = payload.get("rendimiento") or {}
    rrhh = payload.get("rrhh") or {}
    vol = payload.get("voluntarios") or {}
    tech = payload.get("tecnologia") or {}
    pei_titulo = pei.get("nombre") or title

    lines = [
        f"# Plan Estratégico Institucional — {pei_titulo}",
        "",
        f"**Organización:** {org.get('nombre', '')}",
        f"**Tipo:** {org.get('tipo', '')}",
        f"**País:** {org.get('pais') or org.get('region', '')}"
        + (f" · **Provincia:** {org.get('provincia')}" if org.get("provincia") else ""),
        f"**Horizonte:** {org.get('horizonte_anios', '')} años",
        "",
        "## Plan Estratégico Institucional",
        _line("Nombre del PEI", pei_titulo),
        _line("Período", pei.get("periodo", "")),
        _line("Versión", pei.get("version", "")),
        _line("Aprobado por", pei.get("aprobado_por", "")),
        _line("Fecha de aprobación", pei.get("fecha_aprobacion", "")),
        "",
        "---",
        "",
        "## 1. Gestión de proyectos (referencia)",
        _line("Proyecto emblemático", pg.get("nombre", "")),
        _line("Objetivo", pg.get("objetivo", "")),
        _line("Vínculo con el PEI", pg.get("vinculo_estrategico", "")),
        _line("Criterios de éxito", pg.get("criterios_exito", "")),
        "",
        "## 2. Análisis DAFO",
        _line("Fortalezas", dafo.get("fortalezas", "")),
        _line("Debilidades", dafo.get("debilidades", "")),
        _line("Oportunidades", dafo.get("oportunidades", "")),
        _line("Amenazas", dafo.get("amenazas", "")),
        "",
        "## 3. Cimientos estratégicos",
        _line("Visión", cim.get("vision", "")),
        _line("Misión", cim.get("mision", "")),
        _line("Valores", cim.get("valores", "")),
        "",
        "## 4. Prioridades y objetivos",
        _line("Prioridades estratégicas", payload.get("prioridades", "")),
        _line("Objetivos SMART", payload.get("objetivos_smart", "")),
        "",
        "## 5. Plan de acción",
    ]

    acciones = payload.get("acciones") or []
    if acciones:
        for i, a in enumerate(acciones, 1):
            lines.append(
                f"{i}. **{a.get('accion', '')}** — Responsable: {a.get('responsable', '')} · "
                f"Plazo: {a.get('plazo', '')} · KPI: {a.get('kpi', '')} · "
                f"Recursos: {a.get('recursos', '')} · Estado: {a.get('estado', '')}"
            )
        lines.append("")
    else:
        lines.append("_Sin acciones registradas._\n")

    lines.extend(
        [
            "## 6. Gestión del rendimiento",
            _line("Indicadores (KPI)", rend.get("kpis", "")),
            _line("Frecuencia de evaluación", rend.get("frecuencia_evaluacion", "")),
            _line("Informes al comité", rend.get("informes_comite", "")),
            "",
            "## 7. Recursos humanos",
            _line("Roles clave", rrhh.get("roles_clave", "")),
            _line("Brechas de formación", rrhh.get("brechas_formacion", "")),
            _line("Reclutamiento", rrhh.get("reclutamiento", "")),
            "",
            "## 8. Voluntarios y formación",
            _line("Necesidades", vol.get("necesidades", "")),
            _line("Motivaciones", vol.get("motivaciones", "")),
            _line("Formación", vol.get("formacion", "")),
            _line("Reconocimiento", vol.get("reconocimiento", "")),
            "",
            "## 9. Tecnología e IA (opcional)",
            _line("Notas", tech.get("notas_ia", "")),
            "",
            "---",
            "",
            "_Referencia: Manual de Administración Deportiva, COI (2020), Unidades 53–57._",
            "_Generado con PlanificaDeporte._",
        ]
    )
    return "\n".join(lines)


def plan_backup_bytes(title: str, payload: dict[str, Any]) -> bytes:
    doc = {"format": "planifica-deporte-backup", "version": 1, "title": title, "payload": payload}
    return json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")


def parse_plan_backup(raw: bytes) -> tuple[str, dict[str, Any]]:
    data = json.loads(raw.decode("utf-8"))
    if data.get("format") != "planifica-deporte-backup":
        raise ValueError("Archivo no reconocido como respaldo PlanificaDeporte.")
    return str(data.get("title") or "Plan importado"), data.get("payload") or {}

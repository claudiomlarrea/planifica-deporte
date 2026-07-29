"""Encuestas (Google Forms) para reunir aportes al PEI."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import streamlit as st

# Apartados donde la comisión suele consultar a socios, clubes o voluntarios.
SURVEY_MODULES: dict[str, dict[str, str]] = {
    "foda": {
        "titulo": "Encuesta FODA",
        "para_que": (
            "Reunir fortalezas, oportunidades, debilidades y amenazas vistas por "
            "dirigentes, entrenadores, clubes afiliados y socios."
        ),
        "destinatarios_ej": "Comisión directiva, secretarios de clubes, cuerpo técnico, socios activos",
        "preguntas": (
            "1. ¿Cuál es tu rol o vínculo con la organización? "
            "(dirigente, entrenador, socio, voluntario, familiar, referente de club, otro)\n"
            "2. FORTALEZAS — ¿Cuáles son las principales fortalezas internas? (2 a 5 ideas)\n"
            "3. OPORTUNIDADES — ¿Qué oportunidades del entorno conviene aprovechar?\n"
            "4. DEBILIDADES — ¿Qué debilidades internas deberían priorizarse?\n"
            "5. AMENAZAS — ¿Qué amenazas externas preocupan más?\n"
            "6. (Opcional) Si tuvieras que elegir UNA prioridad para los próximos 2 años, ¿cuál sería?"
        ),
    },
    "cimientos": {
        "titulo": "Encuesta visión, misión y valores",
        "para_que": (
            "Consultar cómo la comunidad entiende el propósito y los valores antes de "
            "cerrar la redacción del PEI."
        ),
        "destinatarios_ej": "Asamblea, comisión, referentes de clubes, familias",
        "preguntas": (
            "1. ¿Cuál es tu rol o vínculo con la organización?\n"
            "2. VISIÓN — En 2030, ¿cómo te gustaría que se reconozca a la organización?\n"
            "3. MISIÓN — ¿Para qué existe la organización, en tus palabras?\n"
            "4. VALORES — ¿Qué 3 valores no deberían negociarse?\n"
            "5. (Opcional) ¿Hay alguna frase o idea que debería aparecer sí o sí en la misión o la visión?"
        ),
    },
    "prioridades": {
        "titulo": "Encuesta prioridades y objetivos",
        "para_que": (
            "Priorizar focos estratégicos y validar si los objetivos SMART resuenan "
            "con clubes y partes interesadas."
        ),
        "destinatarios_ej": "Comisión, clubes afiliados, área técnica, representantes regionales",
        "preguntas": (
            "1. Ordená de 1 a 5 las prioridades que más importan (base, formación, "
            "competencias, finanzas, gobernanza…).\n"
            "2. ¿Qué resultado concreto debería lograrse en 2 años?\n"
            "3. ¿Hay alguna prioridad faltante?\n"
            "4. Rol / vínculo con la organización"
        ),
    },
    "acciones": {
        "titulo": "Encuesta plan de acción",
        "para_que": (
            "Proponer o validar acciones concretas: qué hacer, quién, cuándo, "
            "recursos e indicador, vinculadas a las prioridades del PEI."
        ),
        "destinatarios_ej": "Comisión, áreas técnicas, referentes de clubes, responsables de proyectos",
        "preguntas": (
            "1. Rol / vínculo con la organización\n"
            "2. ¿A qué prioridad del PEI aporta la acción?\n"
            "3. ¿Qué acción concreta proponés?\n"
            "4. ¿Quién debería ser responsable?\n"
            "5. ¿En qué plazo?\n"
            "6. ¿Qué recursos hacen falta?\n"
            "7. ¿Con qué KPI se mide el avance?"
        ),
    },
    "rendimiento": {
        "titulo": "Encuesta evaluación e informes",
        "para_que": (
            "Acordar con qué frecuencia se revisa el PEI y qué informes necesita "
            "el comité (los KPI se toman del plan de acción)."
        ),
        "destinatarios_ej": "Comisión ejecutiva, tesorería, área técnica, responsables de sedes",
        "preguntas": (
            "1. ¿Con qué frecuencia deberían informar avance (mensual / trimestral / anual)?\n"
            "2. ¿Qué información necesitás recibir del plan?\n"
            "3. ¿Quién debería sintetizar el informe al comité?\n"
            "4. Rol / vínculo con la organización"
        ),
    },
    "personas": {
        "titulo": "Encuesta recursos humanos y voluntarios",
        "para_que": (
            "Detectar roles críticos, brechas de formación y motivaciones del "
            "voluntariado para sostener el PEI."
        ),
        "destinatarios_ej": "Staff, voluntarios de eventos, referentes de clubes, nuevos ingresantes",
        "preguntas": (
            "1. ¿En qué roles hace falta más gente o más formación?\n"
            "2. ¿Qué te motiva a colaborar (servicio, familia, prestigio, experiencia…)?\n"
            "3. ¿Qué formación o reconocimiento te ayudaría a seguir?\n"
            "4. Rol / vínculo con la organización"
        ),
    },
}


def empty_survey_entry() -> dict[str, str]:
    return {
        "url": "",
        "etiqueta": "",
        "destinatarios": "",
        "notas": "",
    }


def normalize_form_url(url: str) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    return raw


def is_plausible_form_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    # Google Forms y enlaces cortos frecuentes; también se admiten otros formularios web.
    if "forms.gle" in host or "docs.google.com" in host:
        return True
    if "form" in path or "forms" in host:
        return True
    return bool(parsed.netloc)


def get_survey(payload: dict[str, Any], module_key: str) -> dict[str, str]:
    encuestas = payload.setdefault("encuestas", {})
    if module_key == "foda" and "dafo" in encuestas and "foda" not in encuestas:
        encuestas["foda"] = encuestas.pop("dafo")
    elif module_key == "foda" and "dafo" in encuestas:
        encuestas.pop("dafo", None)
    entry = encuestas.setdefault(module_key, empty_survey_entry())
    for k, v in empty_survey_entry().items():
        entry.setdefault(k, v)
    return entry


def list_configured_surveys(payload: dict[str, Any]) -> list[dict[str, str]]:
    encuestas = payload.get("encuestas") or {}
    out: list[dict[str, str]] = []
    for key, meta in SURVEY_MODULES.items():
        entry = encuestas.get(key) or {}
        url = normalize_form_url(str(entry.get("url") or ""))
        if not url:
            continue
        out.append(
            {
                "modulo": key,
                "titulo": meta["titulo"],
                "url": url,
                "etiqueta": str(entry.get("etiqueta") or meta["titulo"]),
                "destinatarios": str(entry.get("destinatarios") or ""),
            }
        )
    return out


def render_survey_panel(module_key: str, payload: dict[str, Any]) -> None:
    """Panel para pegar el Google Form, abrirlo y copiar el enlace a grupos."""
    meta = SURVEY_MODULES.get(module_key)
    if not meta:
        return

    entry = get_survey(payload, module_key)
    st.markdown(
        f'<div class="rumbo-survey-cta"><span>Encuesta para reunir aportes — {meta["titulo"]}</span></div>',
        unsafe_allow_html=True,
    )
    open_panel = st.toggle(
        "Configurar encuesta y compartir con participantes",
        value=bool((entry.get("url") or "").strip()),
        key=f"survey_toggle_{module_key}",
    )
    if not open_panel:
        return

    st.caption(meta["para_que"])
    st.info(
        "La comisión directiva crea el formulario en Google Forms (u otra herramienta), "
        "pega el enlace acá y lo comparte con los grupos que elija "
        "(WhatsApp, mail, redes del club/federación/asociación). "
        "Después sintetizan las respuestas en los campos de este módulo."
    )

    entry["etiqueta"] = st.text_input(
        "Nombre del formulario (para los participantes)",
        entry.get("etiqueta") or meta["titulo"],
        key=f"survey_label_{module_key}",
        placeholder=meta["titulo"],
    )
    entry["url"] = st.text_input(
        "Enlace del formulario (Google Forms u otro)",
        entry.get("url", ""),
        key=f"survey_url_{module_key}",
        placeholder="https://forms.gle/… o https://docs.google.com/forms/…",
    )
    entry["destinatarios"] = st.text_input(
        "A quiénes lo enviará la comisión (registro interno)",
        entry.get("destinatarios", ""),
        key=f"survey_to_{module_key}",
        placeholder=meta["destinatarios_ej"],
    )
    entry["notas"] = st.text_area(
        "Notas (plazo de respuesta, responsable de síntesis…)",
        entry.get("notas", ""),
        key=f"survey_notes_{module_key}",
        height=70,
    )

    url = normalize_form_url(entry.get("url", ""))
    b1, b2, b3 = st.columns(3)
    with b1:
        if url and is_plausible_form_url(url):
            st.markdown(
                f'<a class="rumbo-survey-btn" href="{url}" target="_blank" rel="noopener noreferrer">'
                "Acceder al formulario</a>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span class="rumbo-survey-btn-disabled">Acceder al formulario</span>',
                unsafe_allow_html=True,
            )
            st.caption("Pegá un enlace válido para habilitar el acceso.")
    with b2:
        if url and st.button(
            "Preparar enlace para copiar",
            key=f"survey_copy_{module_key}",
            use_container_width=True,
        ):
            st.session_state[f"survey_show_copy_{module_key}"] = True
    with b3:
        if st.button(
            "Ver preguntas sugeridas",
            key=f"survey_qs_{module_key}",
            use_container_width=True,
        ):
            st.session_state[f"survey_show_qs_{module_key}"] = not st.session_state.get(
                f"survey_show_qs_{module_key}", False
            )

    if url and st.session_state.get(f"survey_show_copy_{module_key}"):
        st.success(
            "Copiá el enlace y envialo a los grupos que defina la comisión "
            "(clubes, WhatsApp, mail, redes)."
        )
        st.code(url, language=None)
        etiqueta = (entry.get("etiqueta") or meta["titulo"]).strip()
        st.text_area(
            "Texto sugerido para el mensaje",
            (
                f"Hola: desde la comisión de {payload.get('org', {}).get('nombre') or 'la organización'} "
                f"te invitamos a completar «{etiqueta}» para aportar al Plan Estratégico (PEI).\n\n"
                f"{url}\n\n"
                "Tu respuesta nos ayuda a construir el plan con la comunidad. ¡Gracias!"
            ),
            height=120,
            key=f"survey_msg_{module_key}",
        )

    if st.session_state.get(f"survey_show_qs_{module_key}"):
        st.markdown("**Preguntas sugeridas para armar el Google Form**")
        st.code(meta["preguntas"], language=None)

    if url and not is_plausible_form_url(url):
        st.warning("Revisá el enlace: debería empezar con https:// y ser un formulario web.")

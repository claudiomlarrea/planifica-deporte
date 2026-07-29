"""Rumbo Deporte — interfaz principal Streamlit."""

from __future__ import annotations

import copy
from datetime import date

import pandas as pd
import streamlit as st

from planifica.database import (
    create_plan,
    delete_plan,
    duplicate_plan,
    get_plan,
    get_usage_count,
    increment_usage,
    init_schema,
    list_plans,
    login_account,
    register_account,
    update_plan,
)
from planifica.export import parse_plan_backup, plan_backup_bytes, plan_to_docx, plan_to_markdown
from planifica.geo import PAISES, PROVINCIAS_ARGENTINA, region_label
from planifica.modules import HOW_IT_WORKS, MODULE_HELP, MODULE_ORDER
from planifica.monitoring import (
    ESTADOS,
    action_options,
    dashboard_metrics,
    df_actividades_tabla,
    df_kpi_meta_avance,
    df_por_estado,
    df_por_prioridad,
    empty_actividad,
    kpi_options,
    objective_options,
    priority_options,
    sync_kpis_from_acciones,
)
from planifica.preview import render_plan_preview
from planifica.progress import module_completion, total_completion
from planifica.surveys import list_configured_surveys, render_survey_panel
from planifica.theme import inject_theme, metric_card, render_header
from planifica.utils import demo_plan_payload, empty_plan_payload, generate_id

st.set_page_config(
    page_title="Rumbo Deporte",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

ACTION_COLUMNS = [
    "prioridad",
    "accion",
    "responsable",
    "plazo",
    "kpi",
    "recursos",
    "estado",
]


def ensure_state() -> None:
    defaults = {
        "page": "home",
        "account": None,
        "plan_id": None,
        "edit_module": "organizacion",
        "draft_payload": None,
        "draft_title": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


@st.cache_resource
def bootstrap_db(backend: str = "sqlite") -> bool:
    """backend se usa como clave de caché (sqlite vs postgres) para recrear tablas al cambiar Secrets."""
    init_schema()
    return True


def save_current_plan() -> None:
    acc = st.session_state.account
    pid = st.session_state.plan_id
    if not acc or not pid or st.session_state.draft_payload is None:
        return
    update_plan(
        pid,
        acc["id"],
        title=st.session_state.draft_title,
        payload=st.session_state.draft_payload,
        status=None,
    )


def load_plan_into_session(plan_id: str) -> None:
    acc = st.session_state.account
    if not acc:
        return
    plan = get_plan(plan_id, acc["id"])
    if not plan:
        st.error("Plan no encontrado.")
        return
    st.session_state.plan_id = plan_id
    st.session_state.draft_payload = copy.deepcopy(plan["payload"])
    st.session_state.draft_title = plan["title"]
    st.session_state.page = "edit"
    st.session_state.edit_module = "organizacion"


def sidebar_nav() -> None:
    st.sidebar.title("Navegación")
    if st.session_state.account:
        st.sidebar.success(f"Organización / cuenta: **{st.session_state.account['name']}**")
        if st.sidebar.button("Mis PEI", use_container_width=True):
            save_current_plan()
            st.session_state.page = "panel"
            st.session_state.plan_id = None
            st.rerun()
        if st.sidebar.button("Crear primer PEI / nuevo", use_container_width=True):
            save_current_plan()
            st.session_state.page = "new_plan"
            st.rerun()
        if st.sidebar.button("Cerrar sesión", use_container_width=True):
            save_current_plan()
            st.session_state.account = None
            st.session_state.page = "home"
            st.session_state.plan_id = None
            st.rerun()
    else:
        if st.sidebar.button("Acceso organizaciones", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()

    st.sidebar.divider()
    if st.session_state.page == "edit" and st.session_state.draft_payload:
        st.sidebar.divider()
        st.sidebar.markdown("**Módulos del plan**")
        labels = [label for _, label in MODULE_ORDER]
        keys = [key for key, _ in MODULE_ORDER]
        idx = keys.index(st.session_state.edit_module) if st.session_state.edit_module in keys else 0
        choice = st.sidebar.radio(
            "Ir a",
            labels,
            index=idx,
            label_visibility="collapsed",
        )
        new_key = keys[labels.index(choice)]
        if new_key != st.session_state.edit_module:
            save_current_plan()
            st.session_state.edit_module = new_key
            st.rerun()

        comp = module_completion(st.session_state.draft_payload)
        st.sidebar.caption("Avance por módulo")
        for key, label in MODULE_ORDER:
            if key in ("resumen", "tablero"):
                continue
            pct = int(comp.get(key, 0) * 100)
            st.sidebar.progress(comp.get(key, 0), text=f"{label.split('·', 1)[-1].strip()} ({pct}%)")

    st.sidebar.divider()
    st.sidebar.caption(f"**{get_usage_count()}** sesiones registradas en Rumbo Deporte")


def page_home() -> None:
    st.subheader("Tu primer Plan Estratégico Institucional")
    st.markdown(
        "Pensado para clubes, federaciones y asociaciones que **aún no tienen PEI**. "
        "Armá el plan desde cero, cargá **actividades de ejecución** y seguí el avance "
        "en el **tablero de monitoreo** integrado (Manual COI, Unidades 53–57)."
    )
    if st.button("Entrar / crear cuenta", type="primary"):
        st.session_state.page = "auth"
        st.rerun()
    with st.expander("Cómo funciona el sistema", expanded=True):
        st.markdown(HOW_IT_WORKS)


def page_auth() -> None:
    st.subheader("Acceso organizaciones")
    tab_login, tab_register = st.tabs(["Iniciar sesión", "Crear cuenta"])

    with tab_login:
        name = st.text_input(
            "Nombre de la federación, club o consultora",
            key="login_name",
            placeholder="Ej.: Deporte SA",
        )
        pin = st.text_input("PIN", type="password", key="login_pin")
        if st.button("Ingresar", type="primary"):
            user = login_account(name, pin)
            if not user:
                st.error(
                    "Credenciales incorrectas. Usá el **nombre completo** de la cuenta "
                    "(ej. «Deporte SA», no solo «Deporte») y el PIN correcto."
                )
            else:
                increment_usage()
                st.session_state.account = user
                st.session_state.page = "panel"
                st.rerun()

    with tab_register:
        st.caption(
            "Una cuenta por organización o consultor. Ej.: «Federación-Judo-Mendoza» o "
            "«Consultora-Gestion-Deportiva»."
        )
        name = st.text_input("Nombre", key="reg_name")
        pin = st.text_input("PIN (mín. 4 caracteres)", type="password", key="reg_pin")
        if st.button("Crear cuenta", type="primary"):
            if len(pin.strip()) < 4:
                st.error("PIN demasiado corto.")
            else:
                try:
                    user = register_account(name, pin)
                    increment_usage()
                    st.session_state.account = user
                    st.session_state.page = "panel"
                    st.success("Cuenta creada.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"No se pudo crear la cuenta: {exc}")


def page_panel() -> None:
    acc = st.session_state.account
    if not acc:
        st.session_state.page = "auth"
        st.rerun()
        return

    st.subheader("Planes Estratégicos Institucionales")
    c1, c2, c3 = st.columns(3)
    plans = list_plans(acc["id"])
    with c1:
        metric_card("PEI", str(len(plans)))
    with c2:
        avg = (
            sum(total_completion(p["payload"]) for p in plans) / len(plans) * 100
            if plans
            else 0
        )
        metric_card("Avance promedio", f"{avg:.0f}%")
    with c3:
        if st.button("Crear PEI", use_container_width=True):
            st.session_state.page = "new_plan"
            st.rerun()

    st.markdown("#### Respaldo del PEI")
    st.caption(
        "Guardá una copia en **.json** en tu computadora o en Drive. "
        "Si la app se redeploya sin base persistente, podés **volver a importar** ese archivo."
    )
    imp_col, _ = st.columns([2, 1])
    with imp_col:
        up = st.file_uploader("Archivo .json de Rumbo Deporte", type=["json"])
        if up and st.button("Importar PEI desde archivo"):
            try:
                title, payload = parse_plan_backup(up.getvalue())
                create_plan(acc["id"], title, payload)
                st.success("PEI importado.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    if not plans:
        st.warning(
            "Todavía no hay un PEI. Creá el **primer Plan Estratégico Institucional** "
            "o cargá la demo para practicar."
        )
        return

    st.markdown("**Descargar respaldo**")
    for plan in plans:
        pct = int(total_completion(plan["payload"]) * 100)
        org = (plan["payload"].get("org") or {}).get("nombre") or "Sin nombre de org."
        safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in plan["title"][:50]).strip()
        d1, d2, d3 = st.columns([4, 2, 2])
        with d1:
            st.markdown(f"**{plan['title']}** · {pct}% · {org}")
            st.caption(f"Actualizado: {plan['updated_at'][:10]}")
        with d2:
            st.download_button(
                "Descargar .json",
                plan_backup_bytes(plan["title"], plan["payload"]),
                file_name=f"{safe or 'pei'}.json",
                mime="application/json",
                type="primary",
                use_container_width=True,
                key=f"panel_json_{plan['id']}",
            )
        with d3:
            if st.button("Editar plan", key=f"panel_ed_{plan['id']}", use_container_width=True):
                load_plan_into_session(plan["id"])
                st.rerun()
        st.divider()

    st.markdown("#### Más opciones por plan")
    for plan in plans:
        pct = int(total_completion(plan["payload"]) * 100)
        org = (plan["payload"].get("org") or {}).get("nombre") or "Sin nombre de org."
        with st.expander(f"**{plan['title']}** · {pct}% · {org}", expanded=False):
            st.caption(f"Actualizado: {plan['updated_at'][:10]} · Estado: {plan['status']}")
            b1, b2, b3, b4, b5, b6 = st.columns(6)
            with b1:
                if st.button("Editar", key=f"ed_{plan['id']}"):
                    load_plan_into_session(plan["id"])
                    st.rerun()
            with b2:
                st.download_button(
                    "Word",
                    plan_to_docx(plan["title"], plan["payload"]),
                    file_name=f"{plan['title'][:40]}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"docx_{plan['id']}",
                )
            with b3:
                md = plan_to_markdown(plan["title"], plan["payload"])
                st.download_button(
                    "Markdown",
                    md.encode("utf-8"),
                    file_name=f"{plan['title'][:40]}.md",
                    key=f"md_{plan['id']}",
                )
            with b4:
                st.download_button(
                    "JSON (respaldo)",
                    plan_backup_bytes(plan["title"], plan["payload"]),
                    file_name=f"{plan['title'][:40]}.json",
                    mime="application/json",
                    key=f"json_{plan['id']}",
                )
            with b5:
                if st.button("Duplicar", key=f"dup_{plan['id']}"):
                    duplicate_plan(plan["id"], acc["id"])
                    st.rerun()
            with b6:
                if st.button("Eliminar", key=f"del_{plan['id']}"):
                    delete_plan(plan["id"], acc["id"])
                    st.rerun()


def page_new_plan() -> None:
    acc = st.session_state.account
    if not acc:
        st.session_state.page = "auth"
        st.rerun()
        return

    st.subheader("Crear el primer PEI")
    st.caption(
        "Partimos de cero: la institución todavía no tiene plan estratégico. "
        "Vas a armar el documento marco (PEI) y recién después, si querés, un proyecto concreto."
    )
    title = st.text_input(
        "Nombre tentativo del PEI",
        placeholder="Plan Estratégico Institucional 2026–2030",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Empezar PEI en blanco", type="primary", use_container_width=True):
            if not title.strip():
                st.error("Indicá un nombre para el PEI.")
            else:
                plan = create_plan(acc["id"], title, empty_plan_payload())
                load_plan_into_session(plan["id"])
                st.rerun()
    with c2:
        if st.button("Cargar demo (Federación de Judo)", use_container_width=True):
            demo_title = title.strip() or "PEI demo — Federación de Judo 2026–2030"
            plan = create_plan(acc["id"], demo_title, demo_plan_payload())
            load_plan_into_session(plan["id"])
            st.rerun()


def _module_help(module_key: str) -> None:
    text = MODULE_HELP.get(module_key, "")
    if text:
        st.caption(text)


def _payload() -> dict:
    if st.session_state.draft_payload is None:
        st.session_state.draft_payload = empty_plan_payload()
    payload = st.session_state.draft_payload
    payload.setdefault("pei", {
        "nombre": "",
        "periodo": "",
        "version": "1.0",
        "aprobado_por": "",
        "fecha_aprobacion": "",
    })
    payload.setdefault("actividades", [])
    return payload


def page_edit() -> None:
    acc = st.session_state.account
    if not acc or not st.session_state.plan_id:
        st.session_state.page = "panel"
        st.rerun()
        return

    payload = _payload()
    mod = st.session_state.edit_module
    pct = int(total_completion(payload) * 100)

    st.session_state.draft_title = st.text_input(
        "Nombre del PEI en construcción",
        value=st.session_state.draft_title,
        key="plan_title_input",
        placeholder="Ej.: Primer Plan Estratégico Institucional 2026–2030",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Avance total", f"{pct}%")
    with c2:
        org_name = (payload.get("org") or {}).get("nombre") or "—"
        metric_card("Organización", org_name[:24])
    with c3:
        if st.button("Guardar ahora", use_container_width=True):
            save_current_plan()
            st.success("Guardado.")

    st.divider()

    if mod == "organizacion":
        st.markdown("### Organización")
        _module_help("organizacion")
        org = payload.setdefault("org", {})
        org["nombre"] = st.text_input("Nombre legal o comercial", org.get("nombre", ""))
        tipos = ["Federación", "Club", "Liga", "Comité olímpico", "Asociación", "Otra"]
        tipo_actual = org.get("tipo") or "Federación"
        org["tipo"] = st.selectbox(
            "Tipo",
            tipos,
            index=tipos.index(tipo_actual) if tipo_actual in tipos else 0,
        )
        # Compatibilidad: planes viejos guardaban solo "region"
        if not org.get("pais") and org.get("region"):
            region_raw = str(org.get("region") or "")
            if region_raw.startswith("Argentina"):
                org["pais"] = "Argentina"
                if "·" in region_raw:
                    org["provincia"] = region_raw.split("·", 1)[1].strip()
            elif region_raw in PAISES:
                org["pais"] = region_raw
            else:
                org["pais"] = "Otro"

        pais_actual = org.get("pais") or "Argentina"
        if pais_actual not in PAISES:
            pais_actual = "Otro"
        org["pais"] = st.selectbox(
            "País",
            PAISES,
            index=PAISES.index(pais_actual),
        )
        if org["pais"] == "Argentina":
            prov_actual = org.get("provincia") or ""
            prov_opts = ["— Seleccionar provincia —"] + PROVINCIAS_ARGENTINA
            idx_prov = (
                PROVINCIAS_ARGENTINA.index(prov_actual) + 1
                if prov_actual in PROVINCIAS_ARGENTINA
                else 0
            )
            eleccion = st.selectbox("Provincia / CABA", prov_opts, index=idx_prov)
            org["provincia"] = "" if eleccion.startswith("—") else eleccion
        else:
            org["provincia"] = ""
        org["region"] = region_label(org["pais"], org.get("provincia", ""))
        org["contacto_nombre"] = st.text_input("Referente del plan", org.get("contacto_nombre", ""))
        org["contacto_email"] = st.text_input("Correo de contacto", org.get("contacto_email", ""))

    elif mod == "pei":
        st.markdown("### Tu primer Plan Estratégico Institucional")
        st.info(
            "Partimos de que la institución **todavía no tiene PEI**. "
            "Este módulo inicia el documento que van a construir juntos."
        )
        _module_help("pei")
        pei = payload.setdefault("pei", {})
        if not pei.get("nombre") and st.session_state.draft_title:
            pei["nombre"] = st.session_state.draft_title
        pei["nombre"] = st.text_input(
            "Nombre del primer PEI",
            pei.get("nombre", ""),
            placeholder="Plan Estratégico Institucional 2026–2030",
        )
        if pei["nombre"].strip():
            st.session_state.draft_title = pei["nombre"].strip()
        c1, c2 = st.columns(2)
        with c1:
            pei["periodo"] = st.text_input(
                "Período de vigencia",
                pei.get("periodo", ""),
                placeholder="2026–2030",
            )
        with c2:
            pei["version"] = st.text_input("Versión", pei.get("version") or "1.0")
        org = payload.setdefault("org", {})
        org["horizonte_anios"] = st.slider(
            "Horizonte (años)",
            3,
            7,
            int(org.get("horizonte_anios") or 5),
        )
        pei["aprobado_por"] = st.text_input(
            "Quién lo aprobará cuando esté listo",
            pei.get("aprobado_por", ""),
            placeholder="Comité ejecutivo / Asamblea (aún pendiente de aprobación)",
        )
        pei["fecha_aprobacion"] = st.text_input(
            "Fecha de aprobación (completar cuando lo adopten)",
            pei.get("fecha_aprobacion", ""),
            placeholder="AAAA-MM-DD — dejar vacío si todavía no está aprobado",
        )

    elif mod == "proyectos":
        st.markdown("### Primer proyecto a partir del PEI (opcional)")
        st.warning(
            "Este paso es **después** del PEI. "
            "No se trata de inventar proyectos sueltos: primero el plan, luego un proyecto concreto que lo ejecute."
        )
        _module_help("proyectos")
        pei = payload.get("pei") or {}
        pei_nombre = pei.get("nombre") or st.session_state.draft_title or "—"
        st.caption(f"PEI en construcción: **{pei_nombre}**")
        pg = payload.setdefault("proyecto_guia", {})
        pg["nombre"] = st.text_input(
            "Nombre del primer proyecto (ej. torneo, campus, campaña)",
            pg.get("nombre", ""),
        )
        pg["objetivo"] = st.text_area("Objetivo del proyecto", pg.get("objetivo", ""), height=80)
        c1, c2 = st.columns(2)
        with c1:
            pg["inicio"] = st.text_input("Inicio", pg.get("inicio", ""), placeholder=str(date.today().year))
        with c2:
            pg["fin"] = st.text_input("Finalización", pg.get("fin", ""))
        pg["gestor"] = st.text_input("Gestor del proyecto", pg.get("gestor", ""))
        pg["vinculo_estrategico"] = st.text_area(
            "¿A qué prioridad u objetivo del PEI contribuye?",
            pg.get("vinculo_estrategico", ""),
            height=80,
            placeholder="Ej.: Prioridad «crecimiento de la base» — objetivo +5% afiliados",
        )
        pg["criterios_exito"] = st.text_area("Criterios de éxito (medibles)", pg.get("criterios_exito", ""), height=80)
        pg["presupuesto"] = st.text_input("Presupuesto estimado", pg.get("presupuesto", ""))

        st.markdown("#### Checklist antes de lanzar el proyecto (manual COI)")
        pq = payload.setdefault("proyecto_preguntas", {})
        pq["alineacion_mision"] = st.checkbox(
            "¿Está alineado con la visión, misión y objetivos del PEI que acaban de definir?",
            pq.get("alineacion_mision", False),
        )
        pq["normativa"] = st.checkbox("¿Conforme a estatuto y normativas?", pq.get("normativa", False))
        pq["recursos"] = st.checkbox("¿Recursos humanos y materiales suficientes?", pq.get("recursos", False))
        pq["medicion"] = st.checkbox("¿Se podrán medir los resultados?", pq.get("medicion", False))
        pq["partes_interesadas"] = st.checkbox("¿Participación de partes interesadas?", pq.get("partes_interesadas", False))
        pq["riesgos"] = st.checkbox("¿Identificados riesgos y respuesta?", pq.get("riesgos", False))

    elif mod == "dafo":
        st.markdown("### Análisis DAFO")
        _module_help("dafo")
        render_survey_panel("dafo", payload)
        dafo = payload.setdefault("dafo", {})
        c1, c2 = st.columns(2)
        with c1:
            dafo["fortalezas"] = st.text_area("Fortalezas", dafo.get("fortalezas", ""), height=160)
            dafo["oportunidades"] = st.text_area("Oportunidades", dafo.get("oportunidades", ""), height=160)
        with c2:
            dafo["debilidades"] = st.text_area("Debilidades", dafo.get("debilidades", ""), height=160)
            dafo["amenazas"] = st.text_area("Amenazas", dafo.get("amenazas", ""), height=160)

    elif mod == "cimientos":
        st.markdown("### Cimientos estratégicos")
        _module_help("cimientos")
        render_survey_panel("cimientos", payload)
        cim = payload.setdefault("cimientos", {})
        cim["vision"] = st.text_area("Visión", cim.get("vision", ""), height=100)
        cim["mision"] = st.text_area("Misión", cim.get("mision", ""), height=120)
        cim["valores"] = st.text_area("Valores básicos", cim.get("valores", ""), height=100)

    elif mod == "prioridades":
        st.markdown("### Prioridades y objetivos SMART")
        _module_help("prioridades")
        render_survey_panel("prioridades", payload)
        payload["prioridades"] = st.text_area(
            "Prioridades estratégicas (4 a 6, una por línea)",
            payload.get("prioridades", ""),
            height=120,
        )
        payload["objetivos_smart"] = st.text_area(
            "Objetivos SMART",
            payload.get("objetivos_smart", ""),
            height=120,
            placeholder="Ej.: Aumentar afiliados activos un 5% en 2 años.",
        )

    elif mod == "acciones":
        st.markdown("### Plan de acción operativo")
        _module_help("acciones")
        st.caption(
            "Definí acá el **KPI de cada acción** (una sola vez). "
            "El módulo 7 solo define frecuencia de evaluación e informes al comité."
        )
        render_survey_panel("acciones", payload)
        rows = payload.get("acciones") or []
        if not rows:
            rows = [{c: "" for c in ACTION_COLUMNS}]
        df = pd.DataFrame(rows)
        for col in ACTION_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        df = df[ACTION_COLUMNS]
        edited = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "estado": st.column_config.SelectboxColumn(
                    "Estado",
                    options=["Planificado", "En curso", "Completado", "Suspendido"],
                ),
            },
        )
        payload["acciones"] = edited.fillna("").to_dict(orient="records")
        sync_kpis_from_acciones(payload)

    elif mod == "rendimiento":
        st.markdown("### Evaluación e informes (Unidad 55)")
        _module_help("rendimiento")
        kpis = sync_kpis_from_acciones(payload)
        render_survey_panel("rendimiento", payload)
        st.markdown("#### Indicadores del plan (desde el plan de acción)")
        if kpis:
            for kpi in kpis:
                st.markdown(f"- {kpi}")
            st.caption(
                "Estos KPI se toman automáticamente del **módulo 6 · Plan de acción**. "
                "Para modificarlos, editá la columna KPI de esa tabla."
            )
        else:
            st.warning(
                "Todavía no hay KPI en el plan de acción. "
                "Completá la columna **kpi** en el módulo 6."
            )
        rend = payload.setdefault("rendimiento", {})
        rend["frecuencia_evaluacion"] = st.text_area(
            "Frecuencia de evaluación",
            rend.get("frecuencia_evaluacion", ""),
            height=80,
        )
        rend["informes_comite"] = st.text_area(
            "Informes al comité ejecutivo",
            rend.get("informes_comite", ""),
            height=80,
            placeholder="Informe mensual de avance; evaluación anual esperado vs. real.",
        )

    elif mod == "personas":
        st.markdown("### Recursos humanos y voluntarios (Unidades 56–57)")
        _module_help("personas")
        render_survey_panel("personas", payload)
        rrhh = payload.setdefault("rrhh", {})
        vol = payload.setdefault("voluntarios", {})
        st.markdown("#### Personal / recursos humanos")
        rrhh["roles_clave"] = st.text_area("Roles críticos", rrhh.get("roles_clave", ""), height=100)
        rrhh["brechas_formacion"] = st.text_area("Brechas de formación", rrhh.get("brechas_formacion", ""), height=100)
        rrhh["reclutamiento"] = st.text_area("Reclutamiento y ubicación por competencias", rrhh.get("reclutamiento", ""), height=100)
        st.markdown("#### Voluntarios")
        vol["necesidades"] = st.text_area("Necesidades periódicas de voluntariado", vol.get("necesidades", ""), height=80)
        vol["motivaciones"] = st.text_area("Motivaciones (servicio, familia, prestigio…)", vol.get("motivaciones", ""), height=80)
        vol["formacion"] = st.text_area("Plan de formación", vol.get("formacion", ""), height=80)
        vol["reconocimiento"] = st.text_area("Reconocimiento y retención", vol.get("reconocimiento", ""), height=80)

    elif mod == "resumen":
        st.markdown("### Resumen del plan")
        _module_help("resumen")
        surveys = list_configured_surveys(payload)
        if surveys:
            st.markdown("#### Encuestas vinculadas")
            for s in surveys:
                dest = f" · Destinatarios: {s['destinatarios']}" if s.get("destinatarios") else ""
                st.markdown(f"- **{s['etiqueta']}**{dest}")
                st.markdown(
                    f'<a class="rumbo-survey-btn" href="{s["url"]}" target="_blank" rel="noopener noreferrer">'
                    f"Acceder al formulario · {s['titulo']}</a>",
                    unsafe_allow_html=True,
                )
        md = plan_to_markdown(st.session_state.draft_title, payload)
        safe_name = (st.session_state.draft_title or "PEI")[:50]
        st.markdown("#### Descargar")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "Descargar Word (.docx)",
                plan_to_docx(st.session_state.draft_title, payload),
                file_name=f"{safe_name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                "Descargar Markdown",
                md.encode("utf-8"),
                file_name=f"{safe_name}.md",
                use_container_width=True,
            )
        with c3:
            st.download_button(
                "Descargar respaldo (.json)",
                plan_backup_bytes(st.session_state.draft_title, payload),
                file_name=f"{safe_name}.json",
                mime="application/json",
                use_container_width=True,
            )
        if st.button("Marcar plan como finalizado"):
            update_plan(
                st.session_state.plan_id,
                acc["id"],
                title=st.session_state.draft_title,
                payload=payload,
                status="finalizado",
            )
            st.success("Estado: finalizado.")
        st.divider()
        st.markdown("#### Vista previa")
        render_plan_preview(st.session_state.draft_title, payload)

    elif mod == "actividades":
        st.markdown("### Actividades de ejecución del PEI")
        _module_help("actividades")
        st.info(
            "Cargá actividades concretas vinculadas a prioridades y objetivos. "
            "Los **Borradores** no aparecen en el tablero hasta cambiar de estado."
        )
        acts = payload.setdefault("actividades", [])
        prios = priority_options(payload)
        objs = objective_options(payload)
        acciones_pei = action_options(payload)
        kpis = kpi_options(payload)

        with st.form("nueva_actividad", clear_on_submit=True):
            st.markdown("#### Nueva actividad")
            titulo = st.text_input("Título de la actividad")
            c1, c2 = st.columns(2)
            with c1:
                prioridad = st.selectbox("Prioridad del PEI", prios)
                objetivo = st.selectbox("Objetivo SMART", objs)
                responsable = st.text_input("Responsable")
                periodo = st.text_input("Período", placeholder="2026-Q1 / 2026-S1")
            with c2:
                estado = st.selectbox("Estado", ESTADOS, index=1)
                if acciones_pei:
                    accion_pei = st.selectbox(
                        "Acción del plan (opcional)",
                        ["—"] + acciones_pei,
                    )
                else:
                    st.caption(
                        "Todavía no hay acciones en el módulo 6. "
                        "Cargalas ahí para elegirlas en este desplegable."
                    )
                    accion_pei = "—"
                if kpis:
                    kpi_sel = st.selectbox(
                        "KPI / indicador",
                        ["—"] + kpis + ["Otro (escribir abajo)"],
                    )
                else:
                    kpi_sel = "Otro (escribir abajo)"
                    st.caption(
                        "Todavía no hay KPI en el módulo 7 ni en el plan de acción. "
                        "Podés escribir uno abajo o cargarlos primero."
                    )
                unidad = st.text_input("Unidad", placeholder="afiliados, escuelas, torneos…")
            kpi_otro = st.text_input(
                "KPI personalizado (si elegiste «Otro» o no hay lista)",
                placeholder="Ej.: Escuelas activas",
            )
            if kpi_sel == "Otro (escribir abajo)" or kpi_sel == "—":
                kpi_nombre = kpi_otro.strip()
            else:
                kpi_nombre = kpi_sel
            c3, c4, c5 = st.columns(3)
            with c3:
                meta = st.number_input("Meta", min_value=0.0, value=0.0, step=1.0)
            with c4:
                avance = st.number_input("Avance actual", min_value=0.0, value=0.0, step=1.0)
            with c5:
                fecha_inicio = st.text_input("Inicio", placeholder="AAAA-MM-DD")
            fecha_fin = st.text_input("Fin", placeholder="AAAA-MM-DD")
            notas = st.text_area("Notas", height=70)
            if st.form_submit_button("Agregar actividad", type="primary"):
                if not titulo.strip():
                    st.error("Indicá un título.")
                else:
                    nueva = empty_actividad()
                    nueva.update(
                        {
                            "id": generate_id("act"),
                            "titulo": titulo.strip(),
                            "prioridad": prioridad,
                            "objetivo": objetivo,
                            "accion_pei": "" if accion_pei == "—" else accion_pei,
                            "responsable": responsable.strip(),
                            "periodo": periodo.strip(),
                            "fecha_inicio": fecha_inicio.strip(),
                            "fecha_fin": fecha_fin.strip(),
                            "estado": estado,
                            "kpi_nombre": kpi_nombre,
                            "meta": float(meta),
                            "avance": float(avance),
                            "unidad": unidad.strip(),
                            "notas": notas.strip(),
                        }
                    )
                    acts.append(nueva)
                    save_current_plan()
                    st.success("Actividad agregada.")
                    st.rerun()

        st.markdown("#### Actividades cargadas")
        if not acts:
            st.caption("Todavía no hay actividades. Usá el formulario de arriba o cargá la demo del PEI.")
        else:
            df = pd.DataFrame(acts)
            cols_show = [
                c
                for c in [
                    "titulo",
                    "prioridad",
                    "objetivo",
                    "responsable",
                    "periodo",
                    "estado",
                    "kpi_nombre",
                    "meta",
                    "avance",
                    "unidad",
                ]
                if c in df.columns
            ]
            edited = st.data_editor(
                df[cols_show] if cols_show else df,
                num_rows="fixed",
                use_container_width=True,
                column_config={
                    "estado": st.column_config.SelectboxColumn("estado", options=ESTADOS),
                    "meta": st.column_config.NumberColumn("meta", min_value=0.0),
                    "avance": st.column_config.NumberColumn("avance", min_value=0.0),
                },
                key="acts_editor",
            )
            if st.button("Guardar cambios de la tabla"):
                for i in range(len(edited)):
                    if i < len(acts):
                        for col in cols_show:
                            acts[i][col] = edited.iloc[i][col]
                save_current_plan()
                st.success("Cambios guardados.")
            del_opts = [
                f"{i + 1}. {a.get('titulo') or '(sin título)'}"
                for i, a in enumerate(acts)
            ]
            if del_opts:
                elegir = st.selectbox("Eliminar actividad", ["—"] + del_opts)
                if elegir != "—" and st.button("Eliminar seleccionada"):
                    idx_del = del_opts.index(elegir)
                    acts.pop(idx_del)
                    save_current_plan()
                    st.rerun()

    elif mod == "tablero":
        st.markdown("### Tablero de monitoreo del PEI")
        _module_help("tablero")
        metrics = dashboard_metrics(payload)
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            metric_card("Actividades", str(metrics["total"]))
        with m2:
            metric_card("En tablero", str(metrics["en_tablero"]))
        with m3:
            metric_card("Avance global", f"{metrics['avance_global']}%")
        with m4:
            metric_card("En curso", str(metrics["en_curso"]))
        with m5:
            metric_card("Cumplidas", str(metrics["cumplidas"]))

        if metrics["en_tablero"] == 0:
            st.warning(
                "No hay actividades publicadas en el tablero. "
                "Cargá actividades en el módulo 11 y cambiá el estado a Planificada, En curso o Cumplida."
            )
        else:
            g1, g2 = st.columns(2)
            with g1:
                st.markdown("#### Actividades por estado")
                df_est = df_por_estado(payload)
                if not df_est.empty:
                    st.bar_chart(df_est.set_index("Estado"))
            with g2:
                st.markdown("#### Cumplimiento por prioridad")
                df_prio = df_por_prioridad(payload)
                if not df_prio.empty and "% cumplimiento" in df_prio.columns:
                    st.bar_chart(df_prio.set_index("Prioridad")[["% cumplimiento"]])

            st.markdown("#### Meta vs. avance (KPI)")
            df_kpi = df_kpi_meta_avance(payload)
            if not df_kpi.empty:
                st.bar_chart(df_kpi.set_index("KPI / actividad")[["Meta", "Avance"]])

            st.markdown("#### Detalle de actividades en tablero")
            st.dataframe(
                df_actividades_tabla(payload, solo_tablero=True),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("#### Avance por prioridad (tabla)")
            st.dataframe(df_por_prioridad(payload), use_container_width=True, hide_index=True)

        with st.expander("Incluir borradores en la tabla (solo consulta)"):
            st.dataframe(
                df_actividades_tabla(payload, solo_tablero=False),
                use_container_width=True,
                hide_index=True,
            )

    nav_c1, nav_c2, nav_c3 = st.columns([1, 1, 2])
    keys = [k for k, _ in MODULE_ORDER]
    idx = keys.index(mod) if mod in keys else 0
    with nav_c1:
        if idx > 0 and st.button("← Módulo anterior"):
            save_current_plan()
            st.session_state.edit_module = keys[idx - 1]
            st.rerun()
    with nav_c2:
        if idx < len(keys) - 1 and st.button("Siguiente módulo →"):
            save_current_plan()
            st.session_state.edit_module = keys[idx + 1]
            st.rerun()


def main() -> None:
    from planifica.db_backend import using_postgres

    bootstrap_db("postgres" if using_postgres() else "sqlite")
    ensure_state()
    inject_theme()
    render_header()
    sidebar_nav()

    page = st.session_state.page
    if page == "home":
        page_home()
    elif page == "auth":
        page_auth()
    elif page == "panel":
        page_panel()
    elif page == "new_plan":
        page_new_plan()
    elif page == "edit":
        page_edit()
    else:
        page_home()


if __name__ == "__main__":
    main()

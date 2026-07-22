"""PlanificaDeporte — interfaz principal Streamlit."""

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
from planifica.export import parse_plan_backup, plan_backup_bytes, plan_to_html, plan_to_markdown
from planifica.geo import PAISES, PROVINCIAS_ARGENTINA, region_label
from planifica.modules import HOW_IT_WORKS, MODULE_HELP, MODULE_ORDER
from planifica.progress import module_completion, total_completion
from planifica.theme import inject_theme, metric_card, render_header
from planifica.utils import demo_plan_payload, empty_plan_payload

st.set_page_config(
    page_title="PlanificaDeporte",
    page_icon="P",
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
def bootstrap_db() -> bool:
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
        if st.sidebar.button("Mis planes estratégicos", use_container_width=True):
            save_current_plan()
            st.session_state.page = "panel"
            st.session_state.plan_id = None
            st.rerun()
        if st.sidebar.button("Nuevo plan", use_container_width=True):
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
            if key == "resumen":
                continue
            pct = int(comp.get(key, 0) * 100)
            st.sidebar.progress(comp.get(key, 0), text=f"{label.split('·', 1)[-1].strip()} ({pct}%)")

    st.sidebar.divider()
    st.sidebar.caption(f"**{get_usage_count()}** sesiones registradas en PlanificaDeporte")


def page_home() -> None:
    st.subheader("Construí el plan que impulsa a tu organización")
    st.markdown(
        "Sistema paso a paso para federaciones, clubes y asociaciones "
        "(Manual COI, Unidades 53–57): datos, DAFO, objetivos, acciones, indicadores y personas."
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
        name = st.text_input("Nombre de la federación, club o consultora", key="login_name")
        pin = st.text_input("PIN", type="password", key="login_pin")
        if st.button("Ingresar", type="primary"):
            user = login_account(name, pin)
            if not user:
                st.error("Credenciales incorrectas.")
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

    st.subheader("Planes estratégicos")
    c1, c2, c3 = st.columns(3)
    plans = list_plans(acc["id"])
    with c1:
        metric_card("Planes", str(len(plans)))
    with c2:
        avg = (
            sum(total_completion(p["payload"]) for p in plans) / len(plans) * 100
            if plans
            else 0
        )
        metric_card("Avance promedio", f"{avg:.0f}%")
    with c3:
        if st.button("Nuevo plan", use_container_width=True):
            st.session_state.page = "new_plan"
            st.rerun()

    st.markdown("#### Importar respaldo")
    up = st.file_uploader("Archivo .json de PlanificaDeporte", type=["json"])
    if up and st.button("Importar plan"):
        try:
            title, payload = parse_plan_backup(up.getvalue())
            create_plan(acc["id"], title, payload)
            st.success("Plan importado.")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

    if not plans:
        st.warning("Todavía no hay planes. Creá uno nuevo o cargá la demo desde «Nuevo plan».")
        return

    for plan in plans:
        pct = int(total_completion(plan["payload"]) * 100)
        org = (plan["payload"].get("org") or {}).get("nombre") or "Sin nombre de org."
        with st.expander(f"**{plan['title']}** · {pct}% · {org}", expanded=False):
            st.caption(f"Actualizado: {plan['updated_at'][:10]} · Estado: {plan['status']}")
            b1, b2, b3, b4, b5 = st.columns(5)
            with b1:
                if st.button("Editar", key=f"ed_{plan['id']}"):
                    load_plan_into_session(plan["id"])
                    st.rerun()
            with b2:
                md = plan_to_markdown(plan["title"], plan["payload"])
                st.download_button(
                    "Exportar MD",
                    md.encode("utf-8"),
                    file_name=f"{plan['title'][:40]}.md",
                    key=f"md_{plan['id']}",
                )
            with b3:
                st.download_button(
                    "Backup JSON",
                    plan_backup_bytes(plan["title"], plan["payload"]),
                    file_name=f"{plan['title'][:40]}.json",
                    key=f"json_{plan['id']}",
                )
            with b4:
                if st.button("Duplicar", key=f"dup_{plan['id']}"):
                    duplicate_plan(plan["id"], acc["id"])
                    st.rerun()
            with b5:
                if st.button("Eliminar", key=f"del_{plan['id']}"):
                    delete_plan(plan["id"], acc["id"])
                    st.rerun()


def page_new_plan() -> None:
    acc = st.session_state.account
    if not acc:
        st.session_state.page = "auth"
        st.rerun()
        return

    st.subheader("Nuevo plan estratégico")
    title = st.text_input("Título del plan", placeholder="Plan estratégico 2026–2030")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Plan en blanco", type="primary", use_container_width=True):
            if not title.strip():
                st.error("Indicá un título.")
            else:
                plan = create_plan(acc["id"], title, empty_plan_payload())
                load_plan_into_session(plan["id"])
                st.rerun()
    with c2:
        if st.button("Cargar demo (Federación de Judo)", use_container_width=True):
            demo_title = title.strip() or "Demo — Federación de Judo"
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
        "Plan Estratégico Institucional",
        value=st.session_state.draft_title,
        key="plan_title_input",
        placeholder="Ej.: Plan Estratégico Institucional 2026–2030",
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
        st.markdown("### Plan Estratégico Institucional")
        _module_help("pei")
        pei = payload.setdefault("pei", {})
        if not pei.get("nombre") and st.session_state.draft_title:
            pei["nombre"] = st.session_state.draft_title
        pei["nombre"] = st.text_input(
            "Nombre del PEI",
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
            "Aprobado por",
            pei.get("aprobado_por", ""),
            placeholder="Comité ejecutivo / Asamblea",
        )
        pei["fecha_aprobacion"] = st.text_input(
            "Fecha de aprobación",
            pei.get("fecha_aprobacion", ""),
            placeholder="AAAA-MM-DD",
        )

    elif mod == "proyectos":
        st.markdown("### Gestión de proyectos (Unidad 53 COI)")
        _module_help("proyectos")
        pei = payload.get("pei") or {}
        pei_nombre = pei.get("nombre") or st.session_state.draft_title or "—"
        st.info(f"**PEI de referencia:** {pei_nombre}")
        pg = payload.setdefault("proyecto_guia", {})
        pg["nombre"] = st.text_input("Proyecto emblemático (ej. torneo, campus)", pg.get("nombre", ""))
        pg["objetivo"] = st.text_area("Objetivo del proyecto", pg.get("objetivo", ""), height=80)
        c1, c2 = st.columns(2)
        with c1:
            pg["inicio"] = st.text_input("Inicio", pg.get("inicio", ""), placeholder=str(date.today().year))
        with c2:
            pg["fin"] = st.text_input("Finalización", pg.get("fin", ""))
        pg["gestor"] = st.text_input("Gestor del proyecto", pg.get("gestor", ""))
        pg["vinculo_estrategico"] = st.text_area(
            "Vínculo con el Plan Estratégico Institucional",
            pg.get("vinculo_estrategico", ""),
            height=80,
            placeholder="Prioridad u objetivo del PEI al que contribuye este proyecto",
        )
        pg["criterios_exito"] = st.text_area("Criterios de éxito (medibles)", pg.get("criterios_exito", ""), height=80)
        pg["presupuesto"] = st.text_input("Presupuesto estimado", pg.get("presupuesto", ""))

        st.markdown("#### Checklist previo al proyecto (manual COI)")
        pq = payload.setdefault("proyecto_preguntas", {})
        pq["alineacion_mision"] = st.checkbox("¿Alineado con misión y objetivos del PEI?", pq.get("alineacion_mision", False))
        pq["normativa"] = st.checkbox("¿Conforme a estatuto y normativas?", pq.get("normativa", False))
        pq["recursos"] = st.checkbox("¿Recursos humanos y materiales suficientes?", pq.get("recursos", False))
        pq["medicion"] = st.checkbox("¿Se podrán medir los resultados?", pq.get("medicion", False))
        pq["partes_interesadas"] = st.checkbox("¿Participación de partes interesadas?", pq.get("partes_interesadas", False))
        pq["riesgos"] = st.checkbox("¿Identificados riesgos y respuesta?", pq.get("riesgos", False))

    elif mod == "dafo":
        st.markdown("### Análisis DAFO")
        _module_help("dafo")
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
        cim = payload.setdefault("cimientos", {})
        cim["vision"] = st.text_area("Visión", cim.get("vision", ""), height=100)
        cim["mision"] = st.text_area("Misión", cim.get("mision", ""), height=120)
        cim["valores"] = st.text_area("Valores básicos", cim.get("valores", ""), height=100)

    elif mod == "prioridades":
        st.markdown("### Prioridades y objetivos SMART")
        _module_help("prioridades")
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

    elif mod == "rendimiento":
        st.markdown("### Gestión y evaluación del rendimiento (Unidad 55)")
        _module_help("rendimiento")
        rend = payload.setdefault("rendimiento", {})
        rend["kpis"] = st.text_area(
            "Indicadores clave (KPI) vinculados a objetivos",
            rend.get("kpis", ""),
            height=120,
        )
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
        rrhh = payload.setdefault("rrhh", {})
        vol = payload.setdefault("voluntarios", {})
        st.markdown("#### Personal")
        rrhh["roles_clave"] = st.text_area("Roles críticos", rrhh.get("roles_clave", ""), height=100)
        rrhh["brechas_formacion"] = st.text_area("Brechas de formación", rrhh.get("brechas_formacion", ""), height=100)
        rrhh["reclutamiento"] = st.text_area("Reclutamiento y ubicación por competencias", rrhh.get("reclutamiento", ""), height=100)
        st.markdown("#### Voluntarios")
        vol["necesidades"] = st.text_area("Necesidades periódicas de voluntariado", vol.get("necesidades", ""), height=80)
        vol["motivaciones"] = st.text_area("Motivaciones (servicio, familia, prestigio…)", vol.get("motivaciones", ""), height=80)
        vol["formacion"] = st.text_area("Plan de formación", vol.get("formacion", ""), height=80)
        vol["reconocimiento"] = st.text_area("Reconocimiento y retención", vol.get("reconocimiento", ""), height=80)
        tech = payload.setdefault("tecnologia", {})
        st.markdown("#### Tecnología e IA (diferencial)")
        tech["notas_ia"] = st.text_area(
            "Usos concretos de IA en la gestión",
            tech.get("notas_ia", ""),
            height=80,
            placeholder="Torneos, consultas, reportes KPI, borradores de proyectos…",
        )

    elif mod == "resumen":
        st.markdown("### Resumen del plan")
        _module_help("resumen")
        md = plan_to_markdown(st.session_state.draft_title, payload)
        st.markdown(plan_to_html(st.session_state.draft_title, payload), unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "Descargar Markdown",
                md.encode("utf-8"),
                file_name=f"{st.session_state.draft_title[:50]}.md",
                type="primary",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                "Descargar backup JSON",
                plan_backup_bytes(st.session_state.draft_title, payload),
                file_name=f"{st.session_state.draft_title[:50]}.json",
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
    bootstrap_db()
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

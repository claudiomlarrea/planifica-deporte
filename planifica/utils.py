from __future__ import annotations

import secrets
import string
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def generate_id(prefix: str = "pln") -> str:
    suffix = secrets.token_hex(8)
    return f"{prefix}_{suffix}"


def empty_plan_payload() -> dict:
    return {
        "org": {
            "nombre": "",
            "tipo": "Federación",
            "pais": "Argentina",
            "provincia": "",
            "region": "",
            "contacto_nombre": "",
            "contacto_email": "",
            "horizonte_anios": 5,
        },
        "pei": {
            "nombre": "",
            "periodo": "",
            "version": "1.0",
            "aprobado_por": "",
            "fecha_aprobacion": "",
        },
        "proyecto_guia": {
            "nombre": "",
            "objetivo": "",
            "inicio": "",
            "fin": "",
            "gestor": "",
            "vinculo_estrategico": "",
            "criterios_exito": "",
            "presupuesto": "",
        },
        "proyecto_preguntas": {
            "alineacion_mision": False,
            "normativa": False,
            "recursos": False,
            "medicion": False,
            "partes_interesadas": False,
            "riesgos": False,
        },
        "dafo": {"fortalezas": "", "debilidades": "", "oportunidades": "", "amenazas": ""},
        "cimientos": {"vision": "", "mision": "", "valores": ""},
        "prioridades": "",
        "objetivos_smart": "",
        "acciones": [],
        "rendimiento": {
            "kpis": "",
            "frecuencia_evaluacion": "",
            "informes_comite": "",
        },
        "rrhh": {
            "roles_clave": "",
            "brechas_formacion": "",
            "reclutamiento": "",
        },
        "voluntarios": {
            "necesidades": "",
            "motivaciones": "",
            "formacion": "",
            "reconocimiento": "",
        },
        "proyectos_cartera": [],
        "tecnologia": {"notas_ia": "", "herramientas": ""},
    }


def demo_plan_payload() -> dict:
    data = empty_plan_payload()
    data["org"].update(
        {
            "nombre": "Federación de Judo (ejemplo demo)",
            "tipo": "Federación",
            "pais": "Argentina",
            "provincia": "Buenos Aires",
            "region": "Argentina · Buenos Aires",
            "contacto_nombre": "Comisión directiva",
            "horizonte_anios": 5,
        }
    )
    data["pei"].update(
        {
            "nombre": "Primer Plan Estratégico Institucional 2026–2030",
            "periodo": "2026–2030",
            "version": "1.0",
            "aprobado_por": "Pendiente — Asamblea (demo)",
            "fecha_aprobacion": "",
        }
    )
    data["proyecto_guia"].update(
        {
            "nombre": "Circuito nacional de torneos infantiles",
            "objetivo": "Duplicar participantes sub-13 en tres años.",
            "vinculo_estrategico": "Prioridad del PEI: crecimiento de la base.",
            "criterios_exito": "Nº de judocas, clubes participantes, satisfacción.",
        }
    )
    data["proyecto_guia"].update(
        {
            "nombre": "Circuito nacional de torneos infantiles",
            "objetivo": "Duplicar participantes sub-13 en tres años.",
            "vinculo_estrategico": "Prioridad: crecimiento de la base.",
            "criterios_exito": "Nº de judocas, clubes participantes, satisfacción.",
        }
    )
    data["dafo"]["fortalezas"] = "Buena imagen pública\nVoluntarios comprometidos\nRelación con clubes"
    data["dafo"]["debilidades"] = "Poca formación formal de entrenadores\nBase financiera limitada"
    data["dafo"]["oportunidades"] = "Programas escolares\nPatrocinio local"
    data["dafo"]["amenazas"] = "Competencia de otros deportes\nRotación de dirigentes"
    data["cimientos"]["vision"] = "Ser referencia nacional en desarrollo del judo base."
    data["cimientos"]["mision"] = (
        "Promover el judo con valores olímpicos, formar entrenadores y "
        "articular clubes en todo el país."
    )
    data["cimientos"]["valores"] = "Respeto · Excelencia · Responsabilidad · Inclusión"
    data["prioridades"] = (
        "1. Crecimiento de la base\n2. Formación de entrenadores\n"
        "3. Competencias y visibilidad\n4. Sostenibilidad financiera"
    )
    data["objetivos_smart"] = "Aumentar afiliados activos un 5% en 2 años."
    data["acciones"] = [
        {
            "prioridad": "Base",
            "accion": "Escuelas en 10 clubes nuevos",
            "responsable": "Área desarrollo",
            "plazo": "2026–2027",
            "kpi": "Judocas sub-13",
            "recursos": "Tatamis, becas",
            "estado": "Planificado",
        }
    ]
    data["rendimiento"]["kpis"] = "Afiliados · Clubes · Entrenadores certificados · % mujeres"
    data["rendimiento"]["frecuencia_evaluacion"] = "Informe mensual al comité; evaluación anual."
    return data

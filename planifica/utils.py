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
        "actividades": [],
        "encuestas": {},
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
    data["objetivos_smart"] = (
        "Aumentar afiliados activos un 5% en 2 años.\n"
        "Capacitar a 40 entrenadores certificados en 18 meses.\n"
        "Organizar 6 torneos formativos sub-15 por año."
    )
    data["acciones"] = [
        {
            "prioridad": "Crecimiento de la base",
            "accion": "Escuelas en 10 clubes nuevos",
            "responsable": "Área desarrollo",
            "plazo": "2026–2027",
            "kpi": "Escuelas de iniciación activas",
            "recursos": "Tatamis, becas",
            "estado": "Planificado",
        },
        {
            "prioridad": "Formación de entrenadores",
            "accion": "Cursos de certificación anuales",
            "responsable": "Secretaría técnica",
            "plazo": "2026–2028",
            "kpi": "Entrenadores certificados en el período",
            "recursos": "Docentes, aula",
            "estado": "Planificado",
        },
    ]
    data["rendimiento"]["kpis"] = (
        "Escuelas de iniciación activas\n"
        "Entrenadores certificados en el período"
    )
    data["rendimiento"]["frecuencia_evaluacion"] = "Informe mensual al comité; evaluación anual."
    data["actividades"] = [
        {
            "id": "act_demo_1",
            "titulo": "Abrir 4 escuelas infantiles en clubes afiliados",
            "prioridad": "Crecimiento de la base",
            "objetivo": "Aumentar afiliados activos un 5% en 2 años.",
            "accion_pei": "Escuelas en 10 clubes nuevos",
            "responsable": "Área desarrollo",
            "periodo": "2026-S1",
            "fecha_inicio": "2026-01-01",
            "fecha_fin": "2026-06-30",
            "estado": "En curso",
            "kpi_nombre": "Escuelas activas",
            "meta": 4,
            "avance": 2,
            "unidad": "escuelas",
            "notas": "Demo de monitoreo",
        },
        {
            "id": "act_demo_2",
            "titulo": "Curso de certificación de entrenadores — cohorte 1",
            "prioridad": "Formación de entrenadores",
            "objetivo": "Capacitar a 40 entrenadores certificados en 18 meses.",
            "accion_pei": "Cursos de certificación anuales",
            "responsable": "Secretaría técnica",
            "periodo": "2026-S1",
            "fecha_inicio": "2026-03-01",
            "fecha_fin": "2026-05-31",
            "estado": "Cumplida",
            "kpi_nombre": "Entrenadores certificados",
            "meta": 20,
            "avance": 22,
            "unidad": "personas",
            "notas": "",
        },
        {
            "id": "act_demo_3",
            "titulo": "Torneo formativo sub-15 — sede Centro",
            "prioridad": "Competencias y visibilidad",
            "objetivo": "Organizar 6 torneos formativos sub-15 por año.",
            "accion_pei": "",
            "responsable": "Comisión de competencias",
            "periodo": "2026-Q2",
            "fecha_inicio": "2026-04-01",
            "fecha_fin": "2026-04-30",
            "estado": "Planificada",
            "kpi_nombre": "Participantes sub-15",
            "meta": 120,
            "avance": 0,
            "unidad": "judocas",
            "notas": "",
        },
        {
            "id": "act_demo_4",
            "titulo": "Borrador campaña de patrocinio local",
            "prioridad": "Sostenibilidad financiera",
            "objetivo": "Aumentar afiliados activos un 5% en 2 años.",
            "accion_pei": "",
            "responsable": "Marketing",
            "periodo": "2026",
            "fecha_inicio": "",
            "fecha_fin": "",
            "estado": "Borrador",
            "kpi_nombre": "Sponsors firmados",
            "meta": 3,
            "avance": 0,
            "unidad": "convenios",
            "notas": "No impacta tablero hasta salir de borrador",
        },
    ]
    return data

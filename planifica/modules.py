"""Navegación y ayuda: primer PEI + ejecución + tablero de monitoreo."""

from __future__ import annotations

MODULE_ORDER: list[tuple[str, str]] = [
    ("organizacion", "1 · Organización"),
    ("pei", "2 · Tu primer PEI"),
    ("dafo", "3 · Análisis DAFO"),
    ("cimientos", "4 · Visión, misión y valores"),
    ("prioridades", "5 · Prioridades y objetivos"),
    ("acciones", "6 · Plan de acción"),
    ("rendimiento", "7 · Indicadores (KPI)"),
    ("personas", "8 · Personas y voluntarios"),
    ("proyectos", "9 · Primer proyecto (opcional)"),
    ("resumen", "10 · Resumen y exportación"),
    ("actividades", "11 · Actividades de ejecución"),
    ("tablero", "12 · Tablero de monitoreo"),
]

MODULE_HELP: dict[str, str] = {
    "organizacion": (
        "Empezá por identificar la institución: club, federación, liga o asociación. "
        "Todavía no hace falta tener un plan escrito: este sistema lo construye con ustedes."
    ),
    "pei": (
        "Acá nace el primer Plan Estratégico Institucional. "
        "Definí nombre, período y quién lo aprobará cuando esté listo (comité o asamblea)."
    ),
    "dafo": (
        "Antes de decidir a dónde van: miren dónde están. "
        "Fortalezas y debilidades internas; oportunidades y amenazas del entorno."
    ),
    "cimientos": (
        "Redactá por primera vez visión (a dónde quieren llegar), misión (para qué existen) "
        "y valores (cómo trabajan). Sin esto no hay PEI."
    ),
    "prioridades": (
        "Elegí entre 4 y 6 focos para los próximos años y formular objetivos SMART "
        "(medibles y con plazo)."
    ),
    "acciones": (
        "Convertí los objetivos en acciones concretas: qué, quién, cuándo, con qué recursos y KPI."
    ),
    "rendimiento": (
        "Definí cómo van a saber si el PEI avanza: indicadores e informes al comité."
    ),
    "personas": (
        "El PEI se ejecuta con personas: roles, formación y voluntariado."
    ),
    "proyectos": (
        "Opcional. Cuando el PEI ya tiene rumbo, podés registrar un primer proyecto "
        "(torneo, campus, campaña) que nazca de ese plan — no al revés."
    ),
    "resumen": (
        "Revisá el primer PEI completo. Descargá Word (.docx) para comité/asamblea, "
        "Markdown o JSON de respaldo."
    ),
    "actividades": (
        "Con el PEI armado, cargá actividades de ejecución vinculadas a prioridades y objetivos. "
        "Solo las que no están en Borrador alimentan el tablero."
    ),
    "tablero": (
        "Tablero de monitoreo del PEI: avance global, actividades por estado y prioridad, "
        "meta vs. avance (estilo Looker Studio, integrado en el sistema)."
    ),
}

HOW_IT_WORKS = """
**Ciclo completo**

1. **Armar el PEI** (módulos 1–10): organización, DAFO, visión, objetivos, acciones, KPI, personas.
2. **Ejecutar** (módulo 11): cargar actividades vinculadas a prioridades y objetivos del PEI.
3. **Monitorear** (módulo 12): tablero con gráficos y tablas de avance (meta vs. real).

**Regla del tablero**

- Una actividad en **Borrador** no cuenta.
- **Planificada / En curso / Cumplida** sí impactan el monitoreo.
- Cada actividad debe estar vinculada a una prioridad u objetivo del PEI.
"""

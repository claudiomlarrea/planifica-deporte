"""Navegación y ayuda: primer PEI desde cero (club / federación / asociación)."""

from __future__ import annotations

# Orden pedagógico: partimos de cero → armamos el PEI → al final un proyecto opcional.
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
}
HOW_IT_WORKS = """
**Para instituciones que todavía no tienen plan**

Muchos clubes y asociaciones **no tienen PEI**: solo actividades, torneos e improvisación.
PlanificaDeporte guía el **primer Plan Estratégico Institucional** paso a paso.

1. Crear cuenta de la organización.
2. **Nuevo PEI** (en blanco o con demo de ejemplo).
3. Completar módulos **1 → 8** (quiénes somos, DAFO, visión, objetivos, acciones, KPI, personas).
4. El módulo **9** (proyecto) es opcional y va **después** del PEI.
5. En **Resumen**, exportar y llevar el documento a aprobación.

**Después de aprobarlo**

- Asignar responsables en el plan de acción.
- Revisar indicadores con la frecuencia acordada.
- Actualizar el PEI cada año (plan operativo) y al cerrar el horizonte.
"""

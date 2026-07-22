"""Navegación y ayuda operativa por módulo (qué completar, no guion de charla)."""

from __future__ import annotations

MODULE_ORDER: list[tuple[str, str]] = [
    ("organizacion", "1 · Organización"),
    ("pei", "2 · Plan Estratégico Institucional"),
    ("proyectos", "3 · Gestión de proyectos"),
    ("dafo", "4 · Análisis DAFO"),
    ("cimientos", "5 · Visión, misión y valores"),
    ("prioridades", "6 · Prioridades y objetivos SMART"),
    ("acciones", "7 · Plan de acción"),
    ("rendimiento", "8 · Rendimiento y KPI"),
    ("personas", "9 · Personas y voluntarios"),
    ("resumen", "10 · Resumen y exportación"),
]

MODULE_HELP: dict[str, str] = {
    "organizacion": (
        "Completá los datos identificatorios de la federación, club o asociación. "
        "Se usan en todas las exportaciones."
    ),
    "pei": (
        "Definí el Plan Estratégico Institucional (PEI): nombre, período, versión y aprobación. "
        "Es el documento marco al que se alinean proyectos, acciones e indicadores."
    ),
    "proyectos": (
        "Registrá un proyecto concreto (torneo, campus, campaña) y marcá el checklist antes de iniciarlo. "
        "Cada proyecto debe alinearse al Plan Estratégico Institucional."
    ),
    "dafo": (
        "Listá fortalezas y debilidades internas, oportunidades y amenazas externas. "
        "Este análisis orienta prioridades y objetivos del PEI."
    ),
    "cimientos": (
        "Redactá visión (a dónde apuntamos), misión (para qué existimos) y valores (cómo actuamos). "
        "Son la base del Plan Estratégico Institucional."
    ),
    "prioridades": (
        "Elegí entre 4 y 6 áreas de foco del PEI y formulá objetivos SMART (medibles y con plazo)."
    ),
    "acciones": (
        "Agregá filas con acciones, responsable, plazo, KPI y recursos. "
        "Podés sumar o quitar filas en la tabla."
    ),
    "rendimiento": (
        "Definí indicadores ligados a los objetivos del PEI y cuándo informar al comité ejecutivo."
    ),
    "personas": (
        "Describí roles, formación, voluntariado y reconocimiento. "
        "Opcional: usos de tecnología e IA en la gestión."
    ),
    "resumen": (
        "Revisá el Plan Estratégico Institucional, descargá Markdown o JSON y compartilo con comité o asamblea. "
        "El JSON sirve de respaldo para importar en otra sesión."
    ),
}

HOW_IT_WORKS = """
**Flujo recomendado**

1. **Crear cuenta** (una por federación, club o consultora).
2. **Nuevo plan** — en blanco o con la **demo** precargada para practicar.
3. Recorrer los **módulos 1 a 8** en la barra lateral; el avance se guarda al cambiar de módulo o con **Guardar ahora**.
4. En **Resumen**, exportar el plan y usarlo en reuniones de planificación y presupuesto anual.

**Para que el plan funcione en la organización**

- Aprobá visión, misión y objetivos en comité directivo.
- Asigná responsables en cada fila del plan de acción.
- Revisá KPI con la frecuencia que definiste (informe mensual + evaluación anual, según COI).
- Actualizá el plan en el sistema cuando cambien prioridades o finalice el horizonte.
"""

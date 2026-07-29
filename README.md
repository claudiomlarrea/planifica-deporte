# Rumbo Deporte

Sistema de planificación estratégica para **clubes, federaciones, asociaciones y organizaciones deportivas**, alineado al Manual COI (2020) Unidades 53–57.

Ciclo: **armar PEI → cargar actividades → monitorear en tablero** (gráficos y tablas integrados).

Misma línea visual que EvaluAR (verde institucional).

## Ejecutar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

- Repo: https://github.com/claudiomlarrea/planifica-deporte
- Main file: `app.py`
- Deploy: https://share.streamlit.io/deploy?repository=claudiomlarrea/planifica-deporte&branch=main&mainModule=app.py

## Uso rápido

1. Crear cuenta (PIN de al menos 4 caracteres).
2. **Nuevo PEI → Cargar demo (Federación de Judo)** (incluye actividades de ejemplo).
3. Completar módulos 1–10 del PEI.
4. **Módulo 11**: actividades de ejecución vinculadas a prioridades/objetivos.
5. **Módulo 12**: tablero de monitoreo (avance, estados, meta vs. real).
6. En DAFO, visión/misión, prioridades, KPI y recursos humanos: vincular Google Forms y compartir el enlace con los grupos que defina la comisión.
7. Exportar Word / Markdown / JSON desde Resumen.

## Persistencia en Streamlit Cloud

Sin `DATABASE_URL`, los PEI se guardan en SQLite y **se borran en cada redeploy**.

1. Creá una base en [Neon](https://neon.tech).
2. Streamlit Cloud → **Settings → Secrets**:

```
DATABASE_URL = "postgresql://..."
```

3. **Reboot** la app.

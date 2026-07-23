# PlanificaDeporte

Sistema de planificación estratégica para **federaciones, clubes y organizaciones deportivas**, alineado al Manual COI (2020) Unidades 53–57.

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
- App (tras el deploy): https://planifica-deporte.streamlit.app

## Persistencia en Streamlit Cloud

Sin `DATABASE_URL`, los PEI se guardan en SQLite local del contenedor y **se borran en cada redeploy**.

1. Creá una base en [Neon](https://neon.tech) (o reutilizá el proyecto de EvaluAR con otra database).
2. Copiá la connection string (pooled) con `sslmode=require`.
3. En Streamlit Cloud → **Settings → Secrets**:

```
DATABASE_URL = "postgresql://..."
```

4. **Reboot** la app. A partir de ahí los PEI persisten.

Mientras tanto: descargá siempre **Word** o **JSON** desde Resumen / Mis PEI.

1. Crear cuenta (PIN de al menos 4 caracteres).
2. **Nuevo plan → Cargar demo (Federación de Judo)**.
3. Completar módulos: Organización → PEI → Proyectos → DAFO → Visión/misión → Objetivos → Acciones → KPI → Personas → Resumen.
4. Exportar Markdown o JSON.

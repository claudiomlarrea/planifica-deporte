/**
 * Rumbo Deporte — completar formulario Indicadores (KPI) YA CREADO
 * https://docs.google.com/forms/d/10Wk_VE_-fuxp_Qcv0wznIl8w3WbXl5-YCL2kHLu_L-M/edit
 *
 * Ejecutar: fillRumboKpiForm
 * Pegar viewform en Rumbo Deporte → módulo 7 · Indicadores (KPI)
 */
function fillRumboKpiForm() {
  var FORM_ID = "10Wk_VE_-fuxp_Qcv0wznIl8w3WbXl5-YCL2kHLu_L-M";
  var form = FormApp.openById(FORM_ID);

  form.setTitle("Rumbo Deporte — Indicadores (KPI)");
  form.setDescription(
    "Encuesta para acordar qué resultados medir en el PEI y con qué frecuencia informar.\n" +
      "La comisión sintetizará las respuestas en Rumbo Deporte (Gestión y evaluación del rendimiento)."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    "¡Gracias! Tu aporte ayuda a definir los indicadores del PEI."
  );

  var items = form.getItems();
  for (var i = items.length - 1; i >= 0; i--) {
    form.deleteItem(items[i]);
  }

  form
    .addMultipleChoiceItem()
    .setTitle("1. ¿Cuál es tu rol o vínculo con la organización?")
    .setChoiceValues([
      "Dirigente / comisión directiva",
      "Entrenador / cuerpo técnico",
      "Socio / afiliado",
      "Voluntario",
      "Tesorería / administración",
      "Referente de club o sede",
      "Otro",
    ])
    .setRequired(true);

  form
    .addCheckboxItem()
    .setTitle(
      "2. ¿Con qué indicadores debería medirse el éxito del PEI? (marcá los que consideres clave)"
    )
    .setChoiceValues([
      "Afiliados / deportistas activos",
      "Clubes o sedes con programas activos",
      "Entrenadores certificados",
      "Participantes en torneos / eventos",
      "% de mujeres (base y/o cuerpo técnico)",
      "Ingresos por patrocinio vs. cuotas",
      "Retención de voluntarios",
      "Satisfacción de clubes / familias (encuesta)",
      "Otro (indicá en la pregunta 4)",
    ])
    .setRequired(true);

  form
    .addMultipleChoiceItem()
    .setTitle("3. ¿Con qué frecuencia deberían informar el avance del plan?")
    .setChoiceValues([
      "Mensual",
      "Trimestral",
      "Semestral",
      "Anual",
      "No estoy seguro/a",
    ])
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "4. ¿Qué información del plan necesitás recibir vos (o tu área/club)?"
    )
    .setHelpText("Ej.: avance de escuelas, presupuesto, calendario de torneos…")
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "5. (Opcional) ¿Hay algún indicador que hoy no se mide y debería medirse?"
    )
    .setRequired(false);

  Logger.log("Pegá en Rumbo Deporte (módulo 7) este enlace:");
  Logger.log(
    "https://docs.google.com/forms/d/10Wk_VE_-fuxp_Qcv0wznIl8w3WbXl5-YCL2kHLu_L-M/viewform"
  );
}

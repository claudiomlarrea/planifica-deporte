/**
 * Rumbo Deporte — completar formulario Plan de acción YA CREADO
 * https://docs.google.com/forms/d/1cAP85LQY6MA9JneiTj-x8Tg0Mudit1rra1CNca_wqLg/edit
 *
 * Ejecutar: fillRumboPlanAccionForm
 * Pegar viewform en Rumbo Deporte → módulo 6 · Plan de acción
 */
function fillRumboPlanAccionForm() {
  var FORM_ID = "1cAP85LQY6MA9JneiTj-x8Tg0Mudit1rra1CNca_wqLg";
  var form = FormApp.openById(FORM_ID);

  form.setTitle("Rumbo Deporte — Plan de acción");
  form.setDescription(
    "Encuesta para proponer o validar acciones concretas del PEI: qué hacer, quién, cuándo y con qué recursos.\n" +
      "La comisión sintetizará las respuestas en Rumbo Deporte."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    "¡Gracias! Tu aporte ayuda a armar el plan de acción del PEI."
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
      "Referente de club afiliado",
      "Otro",
    ])
    .setRequired(true);

  form
    .addMultipleChoiceItem()
    .setTitle("2. ¿A qué prioridad del PEI querés aportar una acción?")
    .setChoiceValues([
      "Crecimiento de la base formativa",
      "Formación y certificación de entrenadores",
      "Competencias y visibilidad institucional",
      "Sostenibilidad financiera y diversificación de ingresos",
      "Gobernanza, datos y evaluación",
      "Otra prioridad",
    ])
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle("3. ¿Qué acción concreta proponés? (qué habría que hacer)")
    .setHelpText("Ej.: Abrir escuelas en clubes, curso de certificación, torneo formativo, campaña de sponsors…")
    .setRequired(true);

  form
    .addTextItem()
    .setTitle("4. ¿Quién debería ser el responsable? (área, cargo o persona)")
    .setRequired(true);

  form
    .addTextItem()
    .setTitle("5. ¿En qué plazo? (año, semestre o fechas)")
    .setHelpText("Ej.: 2026–2027 · 2026-S1 · marzo–junio 2026")
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle("6. ¿Con qué recursos haría falta? (humanos, materiales, presupuesto aproximado)")
    .setRequired(false);

  form
    .addTextItem()
    .setTitle("7. ¿Con qué indicador (KPI) sabríamos si la acción avanzó?")
    .setHelpText("Ej.: escuelas abiertas, entrenadores certificados, participantes, sponsors firmados")
    .setRequired(false);

  form
    .addParagraphTextItem()
    .setTitle("8. (Opcional) ¿Otra acción que debería estar en el plan?")
    .setRequired(false);

  Logger.log("Pegá en Rumbo Deporte (módulo 6 · Plan de acción) este enlace:");
  Logger.log(
    "https://docs.google.com/forms/d/1cAP85LQY6MA9JneiTj-x8Tg0Mudit1rra1CNca_wqLg/viewform"
  );
}

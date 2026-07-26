/**
 * Rumbo — completar formulario Prioridades y objetivos YA CREADO
 * https://docs.google.com/forms/d/1TTuqNJTQOQQzjAXYHaQ6Flm1ytqAL6ynpAVWpU5cias/edit
 *
 * Ejecutar: fillRumboPrioridadesForm
 */
function fillRumboPrioridadesForm() {
  var FORM_ID = "1TTuqNJTQOQQzjAXYHaQ6Flm1ytqAL6ynpAVWpU5cias";
  var form = FormApp.openById(FORM_ID);

  form.setTitle("Rumbo — Prioridades y objetivos");
  form.setDescription(
    "Encuesta para priorizar focos del PEI y proponer objetivos medibles.\n" +
      "La comisión sintetizará las respuestas en Rumbo."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    "¡Gracias! Tu aporte ayuda a definir prioridades y objetivos del PEI."
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
      "Familiar de deportista",
      "Referente de club afiliado",
      "Otro",
    ])
    .setRequired(true);

  form
    .addCheckboxItem()
    .setTitle(
      "2. Marcá las prioridades que más importan para los próximos años (podés marcar varias)"
    )
    .setChoiceValues([
      "Crecimiento de la base formativa",
      "Formación y certificación de entrenadores",
      "Competencias y visibilidad",
      "Sostenibilidad financiera",
      "Gobernanza, datos y evaluación",
      "Inclusión e igualdad de género",
      "Infraestructura e instalaciones",
      "Otra (indicá en la siguiente pregunta)",
    ])
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "3. Ordená o explicá tu top 3 de prioridades (la más importante primero)"
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "4. ¿Qué resultado concreto debería lograrse en 2 años? (objetivo medible)"
    )
    .setHelpText(
      "Ej.: aumentar afiliados un X%, certificar N entrenadores, organizar N torneos…"
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "5. (Opcional) ¿Hay alguna prioridad u objetivo que falte y debería incluirse?"
    )
    .setRequired(false);

  Logger.log("Pegá en Rumbo (módulo 5) este enlace:");
  Logger.log(
    "https://docs.google.com/forms/d/1TTuqNJTQOQQzjAXYHaQ6Flm1ytqAL6ynpAVWpU5cias/viewform"
  );
}

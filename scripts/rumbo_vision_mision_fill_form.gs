/**
 * Rumbo Deporte — completar el formulario Visión / misión / valores YA CREADO
 *
 * Formulario:
 * https://docs.google.com/forms/d/1M9TIbGMtZsV-m6oLqGxa9xg2jeaQtk1XQErdI2JIpZA/edit
 *
 * 1. En el proyecto RUMBO DEPORTE de script.google.com, pegá esta función en Código.gs
 * 2. Ejecutá: fillRumboVisionMisionForm
 * 3. En Rumbo Deporte pegá el enlace RESPONDER (abajo)
 */
function fillRumboVisionMisionForm() {
  var FORM_ID = "1M9TIbGMtZsV-m6oLqGxa9xg2jeaQtk1XQErdI2JIpZA";
  var form = FormApp.openById(FORM_ID);

  form.setTitle("Rumbo Deporte — Visión, misión y valores");
  form.setDescription(
    "Encuesta para aportar a la visión, la misión y los valores del Plan Estratégico Institucional (PEI).\n" +
      "Respondé con tus palabras; la comisión sintetizará las respuestas en Rumbo Deporte."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    "¡Gracias! Tu aporte ayuda a definir la identidad del PEI en Rumbo Deporte."
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
    .addParagraphTextItem()
    .setTitle(
      "2. VISIÓN — En 2030, ¿cómo te gustaría que se reconozca a la organización?"
    )
    .setHelpText(
      "Imagen de futuro: qué querrían que digan de ustedes clubes, familias y comunidad."
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "3. MISIÓN — ¿Para qué existe la organización, en tus palabras?"
    )
    .setHelpText(
      "Propósito cotidiano: a quiénes sirve, qué hace y con qué sentido."
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle("4. VALORES — ¿Qué 3 valores no deberían negociarse?")
    .setHelpText(
      "Ej.: respeto, excelencia, inclusión, transparencia, trabajo en equipo…"
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "5. (Opcional) ¿Hay alguna frase o idea que debería aparecer sí o sí en la misión o la visión?"
    )
    .setRequired(false);

  Logger.log("Listo. Pegá en Rumbo Deporte este enlace:");
  Logger.log(
    "https://docs.google.com/forms/d/1M9TIbGMtZsV-m6oLqGxa9xg2jeaQtk1XQErdI2JIpZA/viewform"
  );
}

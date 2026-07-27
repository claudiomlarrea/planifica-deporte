/**
 * Rumbo Deporte — crear formulario Visión, misión y valores
 *
 * 1. Abrí https://script.google.com (misma cuenta dueña)
 * 2. Podés usar el proyecto RUMBO DEPORTE existente: Archivo → Nuevo → Archivo de secuencia
 *    o pegar esta función debajo de buildRumboFodaForm en Código.gs
 * 3. Ejecutá buildRumboVisionMisionForm
 * 4. En el registro de ejecución copiá el enlace corto / viewform
 * 5. Pegalo en Rumbo Deporte → módulo 4 · Visión, misión y valores
 */
function buildRumboVisionMisionForm() {
  var form = FormApp.create("Rumbo Deporte — Visión, misión y valores");

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

  Logger.log("EDITAR: " + form.getEditUrl());
  Logger.log("RESPONDER (pegar en Rumbo Deporte): " + form.getPublishedUrl());
}

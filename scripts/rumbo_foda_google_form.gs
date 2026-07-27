/**
 * Rumbo Deporte — completar preguntas del formulario FODA / DAFO
 *
 * Cómo usarlo (con la cuenta dueña del formulario, ej. investigacion@uccuyo.edu.ar):
 * 1. Abrí https://script.google.com
 * 2. Nuevo proyecto → pegá TODO este código
 * 3. Guardá y ejecutá la función buildRumboFodaForm
 * 4. La primera vez autorizá el acceso a Google Forms
 * 5. Volvé al formulario: deberían aparecer las preguntas
 *
 * Formulario: https://docs.google.com/forms/d/1De7XbHgphfoUvkHd5zbmMjs3Llb-mr_RafqEndhRU6Q/edit
 */
function buildRumboFodaForm() {
  var FORM_ID = "1De7XbHgphfoUvkHd5zbmMjs3Llb-mr_RafqEndhRU6Q";
  var form = FormApp.openById(FORM_ID);

  form.setTitle("Rumbo Deporte FODA");
  form.setDescription(
    "Encuesta para reunir aportes al análisis DAFO / FODA del Plan Estratégico Institucional (PEI).\n" +
      "Respondé con ejemplos concretos de tu club, federación o asociación.\n" +
      "La comisión sintetizará las respuestas en Rumbo Deporte."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    "¡Gracias! Tu aporte ayuda a construir el PEI. La comisión revisará las respuestas en Rumbo Deporte."
  );

  // Quitar ítems previos (ej. "Pregunta sin título")
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
      "2. FORTALEZAS — ¿Cuáles son las principales fortalezas internas de la organización?"
    )
    .setHelpText(
      "Recursos, personas, imagen, instalaciones, cultura, relación con clubes, etc. Escribí 2 a 5 ideas."
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "3. DEBILIDADES — ¿Qué debilidades internas deberían priorizarse?"
    )
    .setHelpText(
      "Lo que hoy limita el desarrollo: formación, finanzas, datos, comunicación, continuidad de dirigentes, etc."
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "4. OPORTUNIDADES — ¿Qué oportunidades del entorno conviene aprovechar?"
    )
    .setHelpText(
      "Escuelas, municipios, patrocinios, fondos, demanda de deporte formativo, alianzas, etc."
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle("5. AMENAZAS — ¿Qué amenazas externas preocupan más?")
    .setHelpText(
      "Competencia de otros deportes, costos, rotación, regulación, pérdida de voluntarios, etc."
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "6. (Opcional) Si tuvieras que elegir UNA prioridad para los próximos 2 años, ¿cuál sería?"
    )
    .setRequired(false);

  Logger.log("Formulario Rumbo Deporte FODA actualizado: " + form.getEditUrl());
}

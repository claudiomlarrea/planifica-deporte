/**
 * Rumbo Deporte — completar formulario Personas y voluntarios YA CREADO
 * https://docs.google.com/forms/d/1fRQ7Z7Yck2ncT2ztJAPFaDnZEislW7_V_PZeoV-QC4s/edit
 *
 * Ejecutar: fillRumboPersonasForm
 * Pegar viewform en Rumbo Deporte → módulo 8 · Personas y voluntarios
 */
function fillRumboPersonasForm() {
  var FORM_ID = "1fRQ7Z7Yck2ncT2ztJAPFaDnZEislW7_V_PZeoV-QC4s";
  var form = FormApp.openById(FORM_ID);

  form.setTitle("Rumbo Deporte — Personas y voluntarios");
  form.setDescription(
    "Encuesta para detectar roles críticos, brechas de formación y motivaciones del voluntariado que sostienen el PEI.\n" +
      "La comisión sintetizará las respuestas en Rumbo Deporte."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    "¡Gracias! Tu aporte ayuda a planificar personas y voluntariado del PEI."
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
      "Personal / staff",
      "Entrenador / cuerpo técnico",
      "Voluntario",
      "Socio / afiliado",
      "Familiar de deportista",
      "Referente de club afiliado",
      "Otro",
    ])
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "2. PERSONAL — ¿En qué roles hace falta más gente o más formación?"
    )
    .setHelpText(
      "Ej.: planificación, secretaría técnica, desarrollo de clubes, competencias, comunicación, tesorería…"
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "3. ¿Qué brechas de formación ves hoy en dirigentes, técnicos o staff?"
    )
    .setHelpText(
      "Ej.: gestión de proyectos, indicadores, pedagogía de iniciación, herramientas digitales…"
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "4. VOLUNTARIADO — ¿En qué tareas se necesitan voluntarios con más frecuencia?"
    )
    .setHelpText(
      "Ej.: mesas de control, logística, difusión, escuelas infantiles, redes, apoyo en eventos…"
    )
    .setRequired(true);

  form
    .addCheckboxItem()
    .setTitle("5. ¿Qué te motiva (o motivaría) a colaborar? (marcá las que apliquen)")
    .setChoiceValues([
      "Servicio a la comunidad",
      "Familia / hijos en el deporte",
      "Prestigio y pertenencia",
      "Experiencia profesional / CV",
      "Networking",
      "Aprendizaje y formación",
      "Otra",
    ])
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle(
      "6. ¿Qué formación o reconocimiento te ayudaría a seguir colaborando?"
    )
    .setHelpText(
      "Ej.: inducción, primeros auxilios, certificado anual, mención en asamblea, acceso a cursos…"
    )
    .setRequired(false);

  form
    .addParagraphTextItem()
    .setTitle(
      "7. (Opcional) ¿Alguna otra idea para mejorar el trabajo del personal o de los voluntarios?"
    )
    .setRequired(false);

  Logger.log("Pegá en Rumbo Deporte (módulo 8) este enlace:");
  Logger.log(
    "https://docs.google.com/forms/d/1fRQ7Z7Yck2ncT2ztJAPFaDnZEislW7_V_PZeoV-QC4s/viewform"
  );
}

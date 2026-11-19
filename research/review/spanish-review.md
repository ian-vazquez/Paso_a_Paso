# Spanish review — Paso a Paso

Draft Spanish by Claude, Nov 19, 2026. **Nothing here is reviewed yet**: every entry has `translation_reviewed: false`.
Register: **tú** everywhere (CLAUDE.md open decision 9).

## How to review

- Read each row: English on the left, Spanish on the right. Mark the **OK?** column with ✓, or write the fix.
- Rows marked **⚠** state an eligibility or exclusion rule (citizenship, income, age, GPA, service obligation, who can't apply).
  Check that the Spanish is **exactly as strict** as the English: no rule added, dropped or softened.
- You can also see it in place: open the PR preview link on your phone and tap **Español**.
  Card text there carries the note "Borrador: esta traducción aún no ha sido revisada."
- When an entry is approved, set its `translation_reviewed` to `true` in `data/scholarships.json` (Ian only).

## Choices the drafter made (please confirm or change)

| Choice | What the draft does |
|---|---|
| Names | Scholarship, sponsor, fund and school names stay in English (e.g. "UTEP Excellence Scholarship"). |
| FAFSA / TASFA | Kept as-is, with a short explanation in parentheses the first time it appears on a card: "FAFSA (la solicitud federal de ayuda financiera para estudiantes)", "TASFA (la solicitud de ayuda financiera estatal de Texas)". The UI flag labels carry the explanation too, since each card is read on its own. |
| Pell | Not mentioned anywhere in the current data or UI, so no translation was needed. |
| Other acronyms | Same treatment for GED, SAI, SAT/ACT and IRS Form 1040, which do appear. |
| English in parentheses | Some U.S. school terms keep the English word in parentheses so families can match it to the application: transcript, undergraduate, community college, homeschool, grants, tuition, junior/senior. |
| "Aplicar" | Used for "apply" (common in U.S. Spanish). "Solicitar" is the more formal alternative. |
| GPA | "promedio (GPA)". |
| Numbers and money | U.S. format kept ($1,000, 2.0, 30,000) so amounts match the English application. |
| Dates | Written out in Spanish in card text ("15 de diciembre de 2026"). Times: "11:59 p. m., hora del centro (CT)". |
| Quoted page wording | "fall 27, spring 28" (Dr. Juan Andrade Jr.) is a quote from the sponsor page, so it stays in English. |

## Lines to look at closely

- **amazon-future-engineer-2027 · requirements.other**: the English "a high school or college dual-credit course" can be read two ways. The draft reads it as "a high-school course or a college dual-credit course" in CS/engineering. Check against the sponsor page.
- **burger-king-scholars-2027 · notes**: "community applications" is translated literally ("solicitudes comunitarias") with the English in parentheses, since the English doesn't define it.
- **hispanic-scholarship-consortium-2027 · summary**: the English says "GPA 2.5 on a 4.0 scale" without "minimum", so the Spanish doesn't add "mínimo" either.

## Part 1 — Site text (src/i18n/es.json)

**On page now** = can appear on the current page. **Later** = for the January filters; not shown yet, but still worth a check.

### site

| Key | English | Spanish | OK? |
|---|---|---|---|
| `site.title` (on page now) | Scholarships you can apply for | Becas a las que puedes aplicar | |
| `site.tagline` (later) | Scholarships for El Paso students | Becas para estudiantes de El Paso | |
| `site.trust_line` (on page now) | No account. No personal info stored. | Sin cuenta. No guardamos tu información personal. | |
| `site.meta_description` (on page now) | A free list of scholarships for El Paso-area students. No account. No personal info stored. | Una lista gratuita de becas para estudiantes del área de El Paso. Sin cuenta. No guardamos tu información personal. | |
| `site.footer_note` (on page now) | Always confirm details on the scholarship's own website before you apply. Deadlines change. | Confirma siempre los detalles en el sitio web de la beca antes de aplicar. Las fechas límite cambian. | |

### page

| Key | English | Spanish | OK? |
|---|---|---|---|
| `page.intro` (on page now) | Scholarships El Paso-area students can apply for, soonest deadline first. Always check the official page before you apply. | Becas a las que pueden aplicar los estudiantes del área de El Paso, empezando por la fecha límite más próxima. Revisa siempre la página oficial antes de aplicar. | |
| `page.requirements_note` (on page now) | We list the main requirements we confirmed. Most applications ask for more (essays, documents, recommendations), so always read the full application on the official page. | Mostramos los requisitos principales que confirmamos. La mayoría de las solicitudes piden más (ensayos, documentos, cartas de recomendación), así que lee siempre la solicitud completa en la página oficial. | |

### sections

| Key | English | Spanish | OK? |
|---|---|---|---|
| `sections.open_now` (on page now) | Open now | Abiertas ahora | |
| `sections.opening_soon` (on page now) | Opening soon | Abren pronto | |
| `sections.dates_not_posted` (on page now) | Dates not posted yet | Fechas aún no publicadas | |
| `sections.open_now_empty` (on page now) | Nothing is open right now. See “Opening soon” below. | No hay becas abiertas en este momento. Mira “Abren pronto” más abajo. | |

### a11y

| Key | English | Spanish | OK? |
|---|---|---|---|
| `a11y.skip_to_content` (on page now) | Skip to content | Ir al contenido | |
| `a11y.language_switcher` (later) | Language | Idioma | |
| `a11y.opens_new_tab` (later) | opens in a new tab | se abre en una pestaña nueva | |

### search

| Key | English | Spanish | OK? |
|---|---|---|---|
| `search.label` (later) | Search scholarships | Buscar becas | |
| `search.placeholder` (later) | Name, sponsor, or keyword | Nombre, patrocinador o palabra clave | |
| `search.clear` (later) | Clear search | Borrar búsqueda | |

### filters

| Key | English | Spanish | OK? |
|---|---|---|---|
| `filters.heading` (later) | Filters | Filtros | |
| `filters.category` (later) | Type of scholarship | Tipo de beca | |
| `filters.gpa` (later) | My GPA | Mi promedio (GPA) | |
| `filters.gpa_help` (later) | Shows scholarships with no GPA rule, or a rule you already meet. | Muestra becas sin requisito de promedio, o con un requisito que ya cumples. | |
| `filters.residency` (later) | Who can apply | Quién puede aplicar | |
| `filters.degree_type` (later) | What I plan to study | Qué pienso estudiar | |
| `filters.no_essay` (later) | No essay required | Sin ensayo | |
| `filters.no_citizenship` (later) | Citizenship not required | Sin requisito de ciudadanía | |
| `filters.accepts_tasfa` (later) | Accepts TASFA | Acepta la TASFA (la solicitud de ayuda financiera estatal de Texas) | |
| `filters.show_closed` (later) | Also show closed scholarships that reopen | Mostrar también becas cerradas que vuelven a abrir | |
| `filters.reset` (later) | Clear all filters | Borrar todos los filtros | |

### categories

| Key | English | Spanish | OK? |
|---|---|---|---|
| `categories.merit` (later) | Merit | Mérito | |
| `categories.need_based` (later) | Need-based | Por necesidad económica | |
| `categories.first_gen` (later) | First-generation | Primera generación | |
| `categories.regional` (later) | El Paso / regional | El Paso / regional | |
| `categories.demographic` (later) | Demographic-specific | Para grupos específicos | |
| `categories.field_specific` (later) | Specific field of study | Para un campo de estudio específico | |

### residency

| Key | English | Spanish | OK? |
|---|---|---|---|
| `residency.el_paso_county` (later) | El Paso County | Condado de El Paso | |
| `residency.specific_districts` (later) | Specific districts | Distritos específicos | |
| `residency.specific_schools` (later) | Specific schools | Escuelas específicas | |
| `residency.texas` (later) | Texas | Texas | |
| `residency.national` (later) | Anywhere in the U.S. | Cualquier lugar de EE. UU. | |

### degree_types

| Key | English | Spanish | OK? |
|---|---|---|---|
| `degree_types.associate` (on page now) | Associate degree | Grado asociado | |
| `degree_types.bachelor` (on page now) | Bachelor's degree | Licenciatura | |
| `degree_types.trade_technical` (on page now) | Trade or technical program | Programa técnico o vocacional | |

### grade_levels

| Key | English | Spanish | OK? |
|---|---|---|---|
| `grade_levels.hs_junior` (on page now) | High school junior | Estudiante de 11.º grado (junior) de preparatoria | |
| `grade_levels.hs_senior` (on page now) | High school senior | Estudiante de 12.º grado (senior) de preparatoria | |
| `grade_levels.college` (on page now) | College student | Estudiante universitario | |

### demographics

| Key | English | Spanish | OK? |
|---|---|---|---|
| `demographics.hispanic` (later) | Hispanic or Latino | Hispano o latino | |
| `demographics.first_gen` (later) | First-generation college student | Primera generación en la universidad | |
| `demographics.female` (later) | Women | Mujeres | |
| `demographics.african_american` (later) | African American or Black | Afroamericano o negro | |
| `demographics.aapi` (later) | Asian American or Pacific Islander | Asiático-americano o de las islas del Pacífico | |
| `demographics.native_american` (later) | Native American | Nativo americano | |
| `demographics.military_connected` (later) | Military or veteran families | Familias militares o de veteranos | |

### fields_of_study

| Key | English | Spanish | OK? |
|---|---|---|---|
| `fields_of_study.stem` (later) | STEM | STEM (ciencias, tecnología, ingeniería y matemáticas) | |
| `fields_of_study.cs` (later) | Computer science | Ciencias de la computación | |
| `fields_of_study.nursing` (later) | Nursing | Enfermería | |
| `fields_of_study.education` (later) | Education or teaching | Educación o docencia | |
| `fields_of_study.hospitality` (later) | Hospitality or tourism | Hotelería o turismo | |
| `fields_of_study.business` (later) | Business | Negocios | |

### cycle_status

| Key | English | Spanish | OK? |
|---|---|---|---|
| `cycle_status.open` (later) | Open now | Abierta ahora | |
| `cycle_status.upcoming` (later) | Opens soon | Abre pronto | |
| `cycle_status.closed_reopens` (later) | Closed — reopens next cycle | Cerrada — vuelve a abrir el próximo ciclo | |
| `cycle_status.rolling` (later) | Rolling deadline | Fecha límite continua | |
| `cycle_status.unknown` (later) | Status not listed | Estado no especificado | |

### sort

| Key | English | Spanish | OK? |
|---|---|---|---|
| `sort.label` (later) | Sort by | Ordenar por | |
| `sort.deadline` (later) | Deadline soonest | Fecha límite más próxima | |
| `sort.amount` (later) | Largest amount | Cantidad más alta | |

### card

| Key | English | Spanish | OK? |
|---|---|---|---|
| `card.sponsor` (later) | Offered by | Ofrecida por | |
| `card.amount` (on page now) | Award | Monto | |
| `card.deadline` (on page now) | Deadline | Fecha límite | |
| `card.last_verified` (on page now) | Last verified | Verificada por última vez | |
| `card.source` (later) | Source | Fuente | |
| `card.apply` (later) | Apply | Aplicar | |
| `card.essay_required` (on page now) | Essay required | Requiere ensayo | |
| `card.no_essay_required` (on page now) | No essay | Sin ensayo | |
| `card.recs_needed` (on page now) | Recommendation letters: {count} | Cartas de recomendación: {count} | |
| `card.fafsa_required` (on page now) | FAFSA required | Requiere la FAFSA (la solicitud federal de ayuda financiera para estudiantes) | |
| `card.accepts_tasfa` (on page now) | Accepts TASFA | Acepta la TASFA (la solicitud de ayuda financiera estatal de Texas) | |
| `card.citizenship_required` (on page now) | U.S. citizenship or residency required | Requiere ciudadanía o residencia de EE. UU. | |
| `card.no_citizenship_required` (on page now) | No citizenship requirement | Sin requisito de ciudadanía | |
| `card.interview` (on page now) | Interview required | Requiere entrevista | |
| `card.renewable` (on page now) | Renewable | Renovable | |
| `card.gpa_min` (on page now) | Minimum GPA {gpa} | Promedio (GPA) mínimo de {gpa} | |
| `card.application_in_english` (on page now) | The application itself is in English. | La solicitud está en inglés. | |
| `card.summary_english_only` (on page now) | This summary has not been translated yet, so it is shown in English. | Este resumen aún no está traducido, así que se muestra en inglés. | |
| `card.who` (on page now) | Who it's for | Para quién es | |
| `card.requirements` (on page now) | Key requirements | Requisitos principales | |
| `card.official_page` (on page now) | Official page | Página oficial | |
| `card.check_dates` (on page now) | Check the official page for dates. | Consulta la página oficial para ver las fechas. | |
| `card.institutions` (on page now) | For students at {schools} | Para estudiantes de {schools} | |
| `card.no_fafsa_required` (on page now) | FAFSA not required | No requiere la FAFSA (la solicitud federal de ayuda financiera para estudiantes) | |
| `card.no_tasfa` (on page now) | Does not accept TASFA | No acepta la TASFA (la solicitud de ayuda financiera estatal de Texas) | |
| `card.no_interview` (on page now) | No interview | Sin entrevista | |
| `card.requirements_note` (on page now) | There may be more required application steps than those listed here. | Puede haber más pasos obligatorios en la solicitud que los que se muestran aquí. | |
| `card.draft_translation` (on page now) | Draft translation, not reviewed yet. | Borrador: esta traducción aún no ha sido revisada. | |

### value

| Key | English | Spanish | OK? |
|---|---|---|---|
| `value.not_listed` (later) | Not listed — check source | No especificado — consulta la fuente | |
| `value.yes` (on page now) | Yes | Sí | |
| `value.no` (on page now) | No | No | |

### results

| Key | English | Spanish | OK? |
|---|---|---|---|
| `results.count_one` (later) | 1 scholarship | 1 beca | |
| `results.count_other` (later) | {count} scholarships | {count} becas | |
| `results.empty_heading` (later) | No scholarships match these filters. | Ninguna beca coincide con estos filtros. | |
| `results.empty_body` (later) | Try removing a filter, lowering the GPA, or turning on scholarships that reopen next cycle. | Intenta quitar un filtro, bajar el promedio o mostrar las becas que vuelven a abrir el próximo ciclo. | |
| `results.loading` (later) | Loading scholarships… | Cargando becas… | |
| `results.load_error` (later) | The scholarship list could not be loaded. Please refresh the page. | No se pudo cargar la lista de becas. Por favor, actualiza la página. | |

## Part 2 — Scholarship text (data/scholarships.json)

Order on the card: amount, summary, requirements, notes. Empty English fields have no Spanish and are not listed.

### Burger King Scholars (General Track)

`burger-king-scholars-2027` · sponsor: Burger King Foundation · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $1,000–$60,000; most awards are $1,000–$5,000 | De $1,000 a $60,000; la mayoría de los premios son de $1,000 a $5,000 | |
| summary ⚠ | For Class of 2027 seniors living in the US with a GPA of 2.0 or higher. Awards range from $1,000 to $60,000, with most between $1,000 and $5,000. Selection weighs GPA, work experience, extracurriculars, financial need and community service. | Para estudiantes de último año (12.º grado) de la generación 2027 que viven en EE. UU. y tienen un promedio (GPA) de 2.0 o más. Los premios van de $1,000 a $60,000, y la mayoría son de entre $1,000 y $5,000. En la selección se toman en cuenta el promedio, la experiencia laboral, las actividades extracurriculares, la necesidad económica y el servicio comunitario. | |
| requirements.other | Needs a transcript and the first two pages of the most recent IRS Form 1040. | Se necesita un expediente académico (transcript) y las dos primeras páginas del Formulario 1040 del IRS más reciente (la declaración federal de impuestos). | |
| notes | Deadline is 11:59 PM CT on Dec 15, 2026. Only the first 30,000 community applications are reviewed. Run by Scholarship America. | La fecha límite es el 15 de diciembre de 2026 a las 11:59 p. m., hora del centro (CT). Solo se revisan las primeras 30,000 solicitudes comunitarias (community applications). La administra Scholarship America. | |

### Regions Riding Forward Scholarship Contest

`regions-riding-forward-q4-2026` · sponsor: Regions · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $8,000 | $8,000 | |
| summary ⚠ | Quarterly essay contest. Open to legal U.S. residents of an eligible state (Texas is one), age 16 or older, with a cumulative GPA of 2.0 or higher. You need at least one year (or 18 semester hours) left before your undergraduate graduation; if you are not in college yet, you must start your freshman year by the 2027–28 school year. | Concurso trimestral de ensayos. Abierto a residentes legales de EE. UU. que viven en un estado elegible (Texas es uno), de 16 años o más, con un promedio (GPA) acumulado de 2.0 o más. Te debe faltar por lo menos un año (o 18 horas semestrales) para graduarte de tu carrera universitaria (undergraduate); si todavía no estás en la universidad, debes empezar tu primer año a más tardar en el año escolar 2027–28. | |
| notes | This is the Q-4 contest: it opened Oct 1 and closes Dec 31, 2026 at 11:59:59 PM CT. The contest chart only covers 2026, so 2027 quarters are unconfirmed. | Este es el concurso del cuarto trimestre (Q-4): abrió el 1 de octubre y cierra el 31 de diciembre de 2026 a las 11:59:59 p. m., hora del centro (CT). La tabla del concurso solo cubre 2026, así que los trimestres de 2027 no están confirmados. | |

### Taco Bell Live Más Scholarship

`taco-bell-live-mas-2027` · sponsor: Taco Bell Foundation · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $5,000, $10,000 or $25,000 | $5,000, $10,000 o $25,000 | |
| summary ⚠ | For ages 16–26 who are on track for a diploma or GED, or enrolled in a two-year, four-year, vocational or trade program. Awards are $5,000, $10,000 or $25,000, renewable up to 3 times. Apply with a two-minute video or a 250–500-word essay; no GPA, test scores or résumé are needed. | Para jóvenes de 16 a 26 años que van en camino a obtener su diploma o GED (el equivalente al diploma de preparatoria), o que están inscritos en un programa de dos años, de cuatro años, vocacional o técnico. Los premios son de $5,000, $10,000 o $25,000, renovables hasta 3 veces. Aplica con un video de dos minutos o un ensayo de 250 a 500 palabras; no se necesita promedio (GPA), calificaciones de exámenes ni currículum. | |
| requirements.other | Submit a two-minute video or a 250–500-word essay. No GPA, test scores or résumé needed. | Envía un video de dos minutos o un ensayo de 250 a 500 palabras. No se necesita promedio (GPA), calificaciones de exámenes ni currículum. | |
| notes ⚠ | Open to legal residents of the 50 states or D.C., or dependent children of an active-duty U.S. service member. | Abierto a residentes legales de los 50 estados o de D.C., o a hijos e hijas dependientes de un miembro en servicio activo de las Fuerzas Armadas de EE. UU. | |

### Amazon Future Engineer Scholarship

`amazon-future-engineer-2027` · sponsor: Amazon · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $10,000 per year, up to $40,000 total | $10,000 por año, hasta $40,000 en total | |
| summary ⚠ | For U.S. high school seniors with financial need and a cumulative GPA of 2.3 or higher on a 4.0 scale who plan a bachelor's in computer science, computer engineering, data science, information systems, or electrical, automation, mechanical or industrial engineering, or a related field. $10,000 per year, up to $40,000 total. | Para estudiantes de último año de preparatoria en EE. UU. con necesidad económica y un promedio (GPA) acumulado de 2.3 o más en una escala de 4.0, que planean estudiar una licenciatura (bachelor's) en ciencias de la computación, ingeniería en computación, ciencia de datos, sistemas de información, o ingeniería eléctrica, de automatización, mecánica o industrial, o en un campo relacionado. $10,000 por año, hasta $40,000 en total. | |
| requirements.other ⚠ | Must be currently enrolled in or have finished a high school or college dual-credit course in computer science or engineering, or opt in to Amazon's assessment instead. Must be authorized to work in the U.S. | Debes estar tomando ahora, o haber terminado, un curso de ciencias de la computación o ingeniería de preparatoria o de crédito dual universitario (dual-credit), o bien elegir hacer la evaluación de Amazon en su lugar. Debes tener autorización para trabajar en EE. UU. | |

### APIA Scholars General Scholarship

`apia-scholars-general-2027` · sponsor: APIA Scholars · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $2,500 (one year) to $20,000 (multi-year) | De $2,500 (un año) a $20,000 (varios años) | |
| summary ⚠ | Open to all undergraduate students at U.S.-accredited colleges, with a focus on students at or below the poverty line and first-generation college students. Requires high financial need. You must be enrolling as an undergraduate (associate or bachelor's) and be a citizen, national or legal permanent resident of the U.S., Marshall Islands, FSM or Palau. | Abierta a todos los estudiantes de pregrado (undergraduate) en universidades con acreditación de EE. UU., con enfoque en estudiantes que están en el nivel de pobreza o por debajo de él y en estudiantes de primera generación en la universidad. Requiere una alta necesidad económica. Debes estar inscribiéndote como estudiante de pregrado (grado asociado o licenciatura) y ser ciudadano, nacional o residente permanente legal de EE. UU., las Islas Marshall, los Estados Federados de Micronesia (FSM) o Palaos. | |
| requirements.other ⚠ | High financial need. Citizen, national or legal permanent resident of the U.S., Marshall Islands, FSM or Palau. | Alta necesidad económica. Ciudadano, nacional o residente permanente legal de EE. UU., las Islas Marshall, los Estados Federados de Micronesia (FSM) o Palaos. | |

### UTEP Future Miner Scholarship Application

`utep-future-miner-2027` · sponsor: UTEP · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | Varies by scholarship; see the summary | Varía según la beca; consulta el resumen | |
| summary ⚠ | One application for incoming UTEP students. Submitting it gets you considered for the UTEP Excellence Scholarship (top 25% of junior class; $2,000–$8,000 per year, renewable up to 4 years), the Presidential Scholarship (up to 10 students; full cost of attendance, including on-campus housing), and many endowed scholarships, with automatic matching. You can apply before you are admitted: the application tells you to finish your UTEP admission while you wait for results. | Una sola solicitud para estudiantes que van a entrar a UTEP. Al enviarla, se te considera para la UTEP Excellence Scholarship (estar en el 25% más alto de la clase de 11.º grado [junior class]; de $2,000 a $8,000 por año, renovable hasta 4 años), la Presidential Scholarship (hasta 10 estudiantes; el costo total de asistencia, incluida la vivienda en el campus) y muchas becas de fondos dotados (endowed scholarships), con asignación automática. Puedes aplicar antes de que te admitan: la solicitud te indica que termines tu admisión a UTEP mientras esperas los resultados. | |
| requirements.other ⚠ | Optional extra section for the Terry Scholarship and the Miguel A. Loya Engineering Scholarship: two essays (overcoming a challenge, and leadership), for U.S. citizens or permanent residents, due Jan 11, 2027. | Sección adicional opcional para la Terry Scholarship y la Miguel A. Loya Engineering Scholarship: dos ensayos (sobre superar un reto y sobre liderazgo), para ciudadanos o residentes permanentes de EE. UU., con fecha límite el 11 de enero de 2027. | |
| notes | Submitting lets UTEP share your name, major, address, GPA, FAFSA information (including federal tax information) and email with scholarship donors. | Al enviarla, permites que UTEP comparta con los donantes de becas tu nombre, tu carrera, tu dirección, tu promedio (GPA), tu información de la FAFSA (la solicitud federal de ayuda financiera para estudiantes) (incluida tu información de impuestos federales) y tu correo electrónico. | |

### El Paso Community Foundation Scholarships

`el-paso-community-foundation` · sponsor: El Paso Community Foundation · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| summary | One portal, but each fund is its own application. Funds seen so far: Makios Technology Fund (computer/technology majors), El Paso Electric, El Paso Military Officers Association memorial, El Paso in Austin, Catherine L. McPike, Joe and Halina Kallaby/SEAot Leadership Award, and Fabens High School. Each fund's Preview PDF shows its eligibility without applying. | Un solo portal, pero cada fondo tiene su propia solicitud. Fondos vistos hasta ahora: Makios Technology Fund (carreras de computación/tecnología), El Paso Electric, El Paso Military Officers Association memorial, El Paso in Austin, Catherine L. McPike, Joe and Halina Kallaby/SEAot Leadership Award y Fabens High School. El PDF de vista previa (Preview PDF) de cada fondo muestra quién es elegible sin tener que aplicar. | |
| notes | Deadline is Feb 15, 2027, 11:59 PM CST, as shown in the logged-in portal. The public page (epcf.org) still says Jan 1–May 1 with no year; trust the portal. | La fecha límite es el 15 de febrero de 2027 a las 11:59 p. m., hora del centro (CST), como aparece en el portal después de iniciar sesión. La página pública (epcf.org) todavía dice del 1 de enero al 1 de mayo, sin año; confía en el portal. | |

### FirstLight Community Foundation Graduating Seniors Scholarship

`firstlight-graduating-seniors-2027` · sponsor: FirstLight Community Foundation · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| summary | Scholarship for graduating seniors from the FirstLight Community Foundation. Expected to open in January 2027. | Beca de la FirstLight Community Foundation para estudiantes de último año que se gradúan. Se espera que abra en enero de 2027. | |

### Hagan Scholarship

`hagan-scholarship-2027` · sponsor: Hagan Scholarships · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| summary ⚠ | For U.S. high school seniors graduating this year. Household income must not have exceeded $125,000. Cannot be used at a community college, junior college, or online institution. You must work 240 hours from Jan 1 to Sep 1, 2027, and the work must be paid. You must also keep a 4-year graduation schedule. | Para estudiantes de último año de preparatoria en EE. UU. que se gradúan este año. Los ingresos del hogar no deben haber superado $125,000. No se puede usar en un colegio comunitario (community college), un junior college ni una institución en línea. Debes trabajar 240 horas del 1 de enero al 1 de septiembre de 2027, y el trabajo debe ser pagado. También debes mantener un plan para graduarte en 4 años. | |
| requirements.other | One unsealed letter of recommendation. Finalists send the first 2 pages of the FAFSA showing the SAI. | Una carta de recomendación sin sellar. Los finalistas envían las 2 primeras páginas de la FAFSA (la solicitud federal de ayuda financiera para estudiantes) donde aparece el SAI (Student Aid Index, el índice de ayuda estudiantil). | |
| notes ⚠ | You must apply for federal and state grants if you are eligible. | Debes solicitar las ayudas federales y estatales (grants) si eres elegible. | |

### Equitable Excellence Scholarship

`equitable-excellence-2027` · sponsor: Equitable Foundation · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $5,000; up to 100 awards. Each recipient's educator of choice also receives a $500 gift card. | $5,000; hasta 100 premios. El educador o la educadora que elija cada ganador también recibe una tarjeta de regalo de $500. | |
| summary ⚠ | For high school seniors at a public school in the U.S., D.C., or Puerto Rico. Private and homeschooled students are not eligible. You must plan to enroll in a 2-year or 4-year college or university. Renewable for up to 3 years or until you earn a bachelor's degree. | Para estudiantes de último año de una preparatoria pública en EE. UU., D.C. o Puerto Rico. Los estudiantes de escuelas privadas y los que estudian en casa (homeschool) no son elegibles. Debes planear inscribirte en un colegio o universidad de 2 o 4 años. Renovable hasta por 3 años o hasta que obtengas tu licenciatura. | |
| notes ⚠ | Employees of Equitable, or anyone associated with Equitable, cannot apply. Also listed at https://scholarshipamerica.org/scholarship/equitableexcellence/ | Los empleados de Equitable, o cualquier persona asociada con Equitable, no pueden aplicar. También aparece en https://scholarshipamerica.org/scholarship/equitableexcellence/ | |

### Dr. Juan Andrade Jr. Scholarship

`dr-juan-andrade-jr-2027` · sponsor: USHLI · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | $1,000, one-time | $1,000, un solo pago | |
| summary ⚠ | For students enrolled or accepted as full-time undergraduates at a four-year or two-year institution, who must be full-time undergraduates by "fall 27, spring 28" (page wording). You must demonstrate financial need. Non-U.S. citizens are eligible to apply. | Para estudiantes inscritos o aceptados como estudiantes de pregrado (undergraduate) de tiempo completo en una institución de cuatro o de dos años, que deben ser estudiantes de pregrado de tiempo completo para "fall 27, spring 28" (texto de la página). Debes demostrar necesidad económica. Quienes no son ciudadanos de EE. UU. son elegibles para aplicar. | |
| requirements.other | 2 essay questions. 2 recommendations (1 academic, 1 from a professional or community service setting). Portrait picture, 1-page resume, and unofficial transcript. | 2 preguntas de ensayo. 2 recomendaciones (1 académica y 1 de un ámbito profesional o de servicio comunitario). Foto tipo retrato, currículum de 1 página y expediente académico no oficial (unofficial transcript). | |

### JFK Profile in Courage Essay Contest

`jfk-profile-in-courage-essay-2027` · sponsor: JFK Library · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | 1st place: $10,000. 2nd place: $3,000. 3 finalists: $1,000 each. 15 honorable mentions (no money). | 1.er lugar: $10,000. 2.º lugar: $3,000. 3 finalistas: $1,000 cada uno. 15 menciones honoríficas (sin dinero). | |
| summary ⚠ | Open to U.S. citizens in grades 9–12. Write one essay about someone who performed an act of political courage during or after 1917. Only the essay is judged. | Abierto a ciudadanos de EE. UU. de 9.º a 12.º grado. Escribe un ensayo sobre alguien que realizó un acto de valentía política durante 1917 o después. Solo se califica el ensayo. | |

### Army ROTC Scholarship

`army-rotc-scholarship-2027` · sponsor: U.S. Army · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| amount_display | Tuition covered 100% | Cubre el 100% de la colegiatura (tuition) | |
| summary ⚠ | Accepting this scholarship means a future service obligation of 8 years in the Army. For U.S. citizens at least 17 and under 31 years old who have a high school diploma and have taken the SAT or ACT. You must pass the Army physical fitness assessment, then the Army fitness test once your contract is complete. The scholarship can only be used at specific schools; check the official page. | Aceptar esta beca significa que tendrás una obligación de servicio de 8 años en el Ejército en el futuro. Para ciudadanos de EE. UU. de por lo menos 17 años y menores de 31 que tengan diploma de preparatoria y hayan tomado el SAT o el ACT (exámenes de admisión universitaria). Debes aprobar la evaluación de aptitud física del Ejército y, después, la prueba de aptitud física del Ejército una vez que tu contrato esté completo. La beca solo se puede usar en escuelas específicas; consulta la página oficial. | |
| requirements.other ⚠ | Accepting the scholarship means a future service obligation of 8 years in the Army. | Aceptar la beca significa que tendrás una obligación de servicio de 8 años en el Ejército en el futuro. | |
| notes | Multiple application rounds. The first round has passed. Next round: Jan 18, 2027. | Hay varias rondas de solicitud. La primera ronda ya pasó. Próxima ronda: 18 de enero de 2027. | |

### Hispanic Scholarship Consortium

`hispanic-scholarship-consortium-2027` · sponsor: Hispanic Scholarship Consortium · application language: `en` (Spanish cards show "La solicitud está en inglés.")

| Field | English | Spanish | OK? |
|---|---|---|---|
| summary ⚠ | For graduating high school seniors and current certificate, associate, and bachelor's degree students of Hispanic Latino heritage who live in Texas. GPA 2.5 on a 4.0 scale. You must plan to enroll full time or part time in a certificate, associate, or bachelor's degree program. Opens January 2027 for the 2027–28 year. | Para estudiantes de último año de preparatoria que se gradúan y estudiantes actuales de programas de certificado, grado asociado y licenciatura, de herencia hispana o latina, que viven en Texas. Promedio (GPA) de 2.5 en una escala de 4.0. Debes planear inscribirte de tiempo completo o de medio tiempo en un programa de certificado, grado asociado o licenciatura. Abre en enero de 2027 para el año 2027–28. | |

import streamlit as st
from openai import OpenAI

# OpenAI-Client einrichten
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("⚖️ FAIR")
st.subheader("Fast AI review for inmate Release")

# Add example cases
example_case_1 = """### Sachverhalt

**Verurteilung und Haftzeit:**
Der 32-jährige A wurde am 15. März 2021 vom Landgericht wegen schwerer Brandstiftung zu einer Freiheitsstrafe von zwei Jahren und acht Monaten verurteilt. Das Urteil ist seit dem 22. März 2021 rechtskräftig. Der A befindet sich derzeit in der Justizvollzugsanstalt (JVA) und hat am 15. Februar 2023 die Hälfte seiner Strafe verbüßt. Zwei Drittel der Strafe werden am 15. September 2023 vollstreckt sein.

**Hintergrund der Tat:**
A hat in einem unbedachten Moment einen Brand in einem leerstehenden Gebäude gelegt, der sich später auf angrenzende Wohnhäuser ausbreitete. Obwohl es keine Verletzten gab, entstanden erhebliche Sachschäden. A hat die Tat im Wesentlichen gestanden und bereut. Das Gericht wertete seine Einsichtnahme als positiv, stellte jedoch die Schwere der Tat und die Gefährdung der Allgemeinheit heraus.

**Bewährungshilfe und Rehabilitation:**
Während seiner Haftzeit zeigte A ein bemerkenswertes Verhalten. Er nahm aktiv an sämtlichen Rehabilitationsprogrammen teil, darunter eine Therapie zur Bewältigung von Impulsivität und ein Programm zur beruflichen Weiterbildung. A hat in der JVA eine Ausbildung zum Elektriker abgeschlossen und zeigt ein starkes Interesse an einer Berufslaufbahn nach der Haft.

**Familien- und Sozialverhältnisse:**
A ist verheiratet und hat zwei kleine Kinder, die in einer schwierigen Situation sind, da die Familie aufgrund seiner Haft in eine wirtschaftliche Notlage geraten ist. Seine Frau ist stark belastet und benötigt Unterstützung, um die Kinder zu betreuen und den Haushalt zu führen.

**Antrag auf vorzeitige Aussetzung:**
A hat am 1. Juli 2023 beim Gericht einen Antrag auf vorzeitige Aussetzung des Strafrestes zur Bewährung gestellt. Die Strafvollstreckungskammer des Landgerichts prüfte den Antrag und kam zu der Entscheidung, dass besondere Umstände im Sinne von § 57 Abs. 2 Nr. 2 StGB vorliegen."""

example_case_2 = """**Verurteilung und Haftzeit:**
Der 45-jährige B wurde am 12. Januar 2022 vom Landgericht wegen schwerer Körperverletzung zu einer Freiheitsstrafe von drei Jahren verurteilt. Das Urteil ist seit dem 19. Januar 2022 rechtskräftig. Der B befindet sich derzeit in der Justizvollzugsanstalt (JVA) und hat am 12. Januar 2024 die Hälfte seiner Strafe verbüßt. Zwei Drittel der Strafe werden am 12. Juli 2024 vollstreckt sein.

**Hintergrund der Tat:**
B verübte die Tat im Zuge eines Streits in einer Gaststätte, bei dem er einen anderen Mann schwer verletzte. Der Angriff erfolgte ohne direkte Provokation und war besonders brutal. Das Gericht bewertete die Tat als besonders schwerwiegend, da B ohne jegliche Rücksicht auf die Folgen agierte und den Verletzten mit einem Stock schlug, was zu schweren Verletzungen führte. B hat die Tat weitgehend gestanden, jedoch ohne echtes Bedauern zu zeigen.

**Bewährungshilfe und Rehabilitation:**
Während seiner Haftzeit zeigte B nur durchschnittliche Fortschritte. Er nahm an einigen Rehabilitationsprogrammen teil, zeigte jedoch wenig Engagement und wenig Einsicht in seine Taten. Die Berichte der JVA wiesen darauf hin, dass B Schwierigkeiten hatte, sich an die Regeln des Vollzugs zu halten, und es gab mehrere Vorfälle von Disziplinarverstößen.

**Familien- und Sozialverhältnisse:**
B ist ledig und hat keine Kinder. Er hat eine stabile familiäre Unterstützung durch seine Eltern, die regelmäßig Kontakt zu ihm haben und bereit sind, ihn nach der Haftzeit zu unterstützen. Seine familiären Verhältnisse sind weitgehend unauffällig und stellen keinen außergewöhnlichen Belastungsfaktor dar.

**Antrag auf vorzeitige Aussetzung:**
B hat am 1. Februar 2024 beim Gericht einen Antrag auf vorzeitige Aussetzung des Strafrestes zur Bewährung gestellt. Die Strafvollstreckungskammer des Landgerichts prüfte den Antrag und kam zu der Entscheidung, dass keine besonderen Umstände im Sinne von § 57 Abs. 2 Nr. 2 StGB vorliegen."""

# Add buttons for example cases
col1, col2 = st.columns(2)
with col1:
    if st.button("Beispiel 1"):
        case_files = example_case_1
        st.session_state.case_files = case_files
with col2:
    if st.button("Beispiel 2"):
        case_files = example_case_2
        st.session_state.case_files = case_files

# Update text area with example case if selected
case_files = st.text_area("Geben Sie Informationen zu den Fallakten ein:", value=st.session_state.get('case_files', ''), height=200)

def generiere_fiktive_aehnliche_faelle(case_files):
    prompt = f"""Basierend auf den folgenden Fallakten, generieren Sie 4-7 kurze, fiktive deutsche Fallbeschreibungen mit ähnlichen Kontexten. Jeder Fall sollte 2-3 Sätze lang sein und die Entscheidung (entlassen oder nicht entlassen) beinhalten.

    Fallakten:
    {case_files}

    Generieren Sie fiktive ähnliche deutsche Fälle:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    
    return response.choices[0].message.content.strip()

if st.button("Fall analysieren"):
    if case_files:
        # Argumente für und gegen die Entlassung generieren
        arguments_prompt = f"""Basierend auf den folgenden Fallakten, liefern Sie objektive Argumente für und gegen eine vorzeitige Entlassung unter Berücksichtigung dieser Kriterien:

Die Bewertung der Fälle soll auf folgenden Kriterien basieren:

### Argumente für die vorzeitige Aussetzung der Reststrafe zur Bewährung

1. Erfüllung der Voraussetzungen nach § 57 Abs. 2 StGB:
   - Erstmals Freiheitsstrafe und Strafmaß nicht über zwei Jahre
   - Besondere Umstände, die eine Aussetzung rechtfertigen

2. Positive Entwicklung während des Strafvollzugs (§ 57 Abs. 1 StGB):
   - Vorbildliches Verhalten und aktive Rehabilitation

3. Günstige Prognose für das Sicherheitsinteresse der Allgemeinheit (§ 57 Abs. 1 Nr. 2 StGB):
   - Keine Gefahr für die Allgemeinheit
   - Positive Prognose für zukünftiges Verhalten

### Argumente gegen die vorzeitige Aussetzung der Reststrafe zur Bewährung

1. Fehlende besondere Umstände gemäß § 57 Abs. 2 StGB:
   - Keine außergewöhnlichen, die Tat mildernden Umstände

2. Unzureichende Rehabilitation und Verhalten im Vollzug (§ 57 Abs. 1 StGB):
   - Keine signifikanten Fortschritte in der Rehabilitation
   - Nur regelgerechtes Verhalten reicht nicht aus

3. Negative Wahrnehmung in der Allgemeinheit (§ 57 Abs. 1 StGB):
   - Mögliche Beeinträchtigung des Vertrauens in die Strafjustiz

4. Nicht erfüllte Voraussetzungen des § 57 Abs. 1 StGB:
   - Zwei Drittel der Strafe nicht verbüßt
   - Fehlende Zustimmung der verurteilten Person
   - Hohe Rückfallgefahr

Bitte berücksichtigen Sie diese Kriterien bei der Bewertung des Falles und nennen Sie in Ihrer Begründung die relevanten Gesetzesartikel.

Fallakten:
{case_files}

Analyse:
"""
        arguments_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": arguments_prompt}],
            max_tokens=1000,
        )
        
        st.subheader("Analyse")
        st.write(arguments_response.choices[0].message.content)
        
        # Empfehlung generieren
        recommendation_prompt = f"Basierend auf den folgenden Fallakten und Argumenten, geben Sie eine prägnante Empfehlung, ob der Gefangene vorzeitig entlassen werden sollte oder nicht:\n\nFallakten:\n{case_files}\n\nArgumente:\n{arguments_response.choices[0].message.content}\n\nEmpfehlung:"
        recommendation_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": recommendation_prompt}],
            max_tokens=150,
        )
        
        # Empfehlung anzeigen
        st.subheader("Empfehlung")
        st.write(recommendation_response.choices[0].message.content)
        
        # Ähnliche Fälle generieren und anzeigen
        st.subheader("Ähnliche Fälle")
        similar_cases = generiere_fiktive_aehnliche_faelle(case_files)
        with st.expander("Ähnliche Fälle anzeigen"):
            st.markdown(similar_cases)
        
        st.write("Hinweis: Dies sind fiktive Fälle, die nur zu Vergleichszwecken generiert wurden.")
        
    else:
        st.warning("Bitte geben Sie Informationen zu den Fallakten ein.")

st.write("Hinweis: Dieses Tool dient nur zur Entscheidungsunterstützung. Endgültige Entscheidungen sollten von qualifizierten Fachleuten unter Berücksichtigung aller relevanten Faktoren getroffen werden.")

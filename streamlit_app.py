import streamlit as st
from openai import OpenAI

# OpenAI-Client einrichten
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("⚖️ FAIR")
st.subheader("Fast AI Review for Inmate Release")

# Eingabe für Fallakten
case_files = st.text_area("Geben Sie Informationen zu den Fallakten ein:", height=200)

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

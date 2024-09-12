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

1. Kriminelle Vorgeschichte und Art des Verbrechens
2. Verhalten während der Haft
3. Risiko für die öffentliche Sicherheit
4. Verbüßte Zeit und Richtlinien zur Strafzumessung
5. Plan für die Zeit nach der Entlassung

Geben Sie für jedes Kriterium spezifische Details aus den Fallakten an. Wenn Informationen zu einem Kriterium fehlen, geben Sie an, dass mehr Informationen benötigt werden.

Fallakten:
{case_files}

Analyse:
"""
        arguments_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": arguments_prompt}],
            max_tokens=1000,
        )
        
        # Argumente anzeigen
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Argumente für die Entlassung")
            st.write(arguments_response.choices[0].message.content.split("\n\nArgumente gegen die Entlassung:\n")[0])
        with col2:
            st.subheader("Argumente gegen die Entlassung")
            st.write(arguments_response.choices[0].message.content.split("\n\nArgumente gegen die Entlassung:\n")[1] if len(arguments_response.choices[0].message.content.split("\n\nArgumente gegen die Entlassung:\n")) > 1 else "Keine Argumente gegen die Entlassung gefunden.")
        
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

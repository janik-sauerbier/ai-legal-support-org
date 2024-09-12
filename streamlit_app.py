import streamlit as st
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("⚖️ Prisoner Release Decision Support")

# Input for case files
case_files = st.text_area("Enter case files information:", height=200)

def generate_fake_similar_cases(case_files):
    prompt = f"""Based on the following case files, generate 4-7 short, fictional German case descriptions with similar contexts. Each case should be 2-3 sentences long and include the decision (released or not released).

    Case files:
    {case_files}

    Generate fictional similar German cases:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    
    return response.choices[0].message.content.strip()

if st.button("Analyze Case"):
    if case_files:
        # Generate arguments for and against release
        arguments_prompt = f"""Based on the following case files, provide objective arguments for and against early release, considering these criteria:

1. Criminal History and Nature of the Crime
2. Behavior During Incarceration
3. Risk to Public Safety
4. Time Served and Sentencing Guidelines
5. Post-Release Plan

For each criterion, provide specific details from the case files. If information is lacking for any criterion, state that more information is needed.

Case files:
{case_files}

Analysis:
"""
        arguments_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": arguments_prompt}],
            max_tokens=1000,
        )
        
        # Display arguments
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Arguments for Release")
            st.write(arguments_response.choices[0].message.content.split("\n\nArguments against release:\n")[0])
        with col2:
            st.subheader("Arguments against Release")
            st.write(arguments_response.choices[0].message.content.split("\n\nArguments against release:\n")[1] if len(arguments_response.choices[0].message.content.split("\n\nArguments against release:\n")) > 1 else "No arguments against release found.")
        
        # Generate recommendation
        recommendation_prompt = f"Based on the following case files and arguments, provide a concise recommendation on whether the prisoner should be released early or not:\n\nCase files:\n{case_files}\n\nArguments:\n{arguments_response.choices[0].message.content}\n\nRecommendation:"
        recommendation_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": recommendation_prompt}],
            max_tokens=150,
        )
        
        # Display recommendation
        st.subheader("Recommendation")
        st.write(recommendation_response.choices[0].message.content)
        
        # Generate and display similar cases
        st.subheader("Similar Cases")
        similar_cases = generate_fake_similar_cases(case_files)
        with st.expander("View Similar Cases"):
            st.markdown(similar_cases)
        
        st.write("Note: These are fictional cases generated for comparison purposes only.")
        
    else:
        st.warning("Please enter case files information.")

st.write("Note: This tool is for decision support only. Final decisions should be made by qualified professionals considering all relevant factors.")

import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🚔 Early Prisoner Release Decision Support")

# Input for case files
case_files = st.text_area("Enter case files information:", height=200)

if st.button("Analyze Case"):
    if case_files:
        # Generate arguments for and against release
        arguments_prompt = f"Based on the following case files, provide objective arguments for and against early release:\n\n{case_files}\n\nArguments for release:\n1."
        arguments_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": arguments_prompt}],
            max_tokens=500,
        )
        arguments = arguments_response.choices[0].message.content.split("\n\nArguments against release:\n")
        
        # Display arguments
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Arguments for Release")
            st.write(arguments[0])
        with col2:
            st.subheader("Arguments against Release")
            st.write(arguments[1] if len(arguments) > 1 else "No arguments against release found.")
        
        # Generate recommendation
        recommendation_prompt = f"Based on the following case files and arguments, provide a concise recommendation on whether the prisoner should be released early or not:\n\nCase files:\n{case_files}\n\nArguments:\n{arguments_response.choices[0].message.content}\n\nRecommendation:"
        recommendation_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": recommendation_prompt}],
            max_tokens=150,
        )
        
        # Display recommendation
        st.subheader("Recommendation")
        st.write(recommendation_response.choices[0].message.content)
    else:
        st.warning("Please enter case files information.")

st.write("Note: This tool is for decision support only. Final decisions should be made by qualified professionals considering all relevant factors.")

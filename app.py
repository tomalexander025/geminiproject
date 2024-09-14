import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# Streamlit app
def main():
    st.title('Data Analysis App')

    # Input for Gemini API key
    api_key = st.text_input("Enter your Gemini API key here:", type="password")
    
    if api_key:
        # Configure the API key
        genai.configure(api_key=api_key)

        # File uploader
        uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=['xls', 'xlsx', 'csv'])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.write("Data Preview:")
            st.dataframe(df)

            # Input prompt
            prompt = st.text_area("Enter your analysis prompt here:", "Analyze the data and tell me how many of them has the occupation called 'Analyst' and also tell me their salary:")
            
            if st.button('Analyze'):
                # Convert the DataFrame to a string representation
                df_str = df.to_string(index=False)
                
                # Generate content using the AI model
                model = genai.GenerativeModel('gemini-pro')
                full_prompt = f"{prompt}\n\nData:\n{df_str}"
                response = model.generate_content(full_prompt)
                
                # Display the response
                st.write("Analysis Result:")
                st.write(response.text)
    else:
        st.warning("Please enter your Gemini API key.")

if __name__ == "__main__":
    main()

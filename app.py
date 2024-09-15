import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Helper function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Streamlit app
def main():
    st.title('AI Email Writing Assistant')

    # Add the link to help users access the Gemini-Pro API Key
    st.markdown(
        '[Click here to learn how to access the Gemini-Pro API key](https://ai.google.dev/api?lang=python)', 
        unsafe_allow_html=True
    )

    # Input for Gemini API key
    api_key = st.text_input("Enter your Gemini API key here:", type="password")
    
    if api_key:
        # Configure the API key
        genai.configure(api_key=api_key)

        # File uploader for optional document (PDF, DOCX, or TXT)
        uploaded_file = st.file_uploader("Upload a document for additional context (Optional)", type=['pdf', 'docx', 'txt'])

        file_text = ""
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                file_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                file_text = extract_text_from_docx(uploaded_file)
            elif uploaded_file.type == "text/plain":
                file_text = uploaded_file.read().decode("utf-8")

            st.write("Extracted File Content:")
            st.text(file_text)  # Display extracted file content for user reference

        # Input box for the prompt
        prompt = st.text_area("Enter your prompt:", "Write an email to HR asking if there are any Data Science fresher roles.")

        # Select the tone of the email
        tone = st.selectbox("Choose the tone of the email:", ["Professional", "Casual", "Formal", "Friendly", "Other"])

        # Append file content to the prompt if available
        if file_text:
            prompt += f"\n\nAdditional Context from Uploaded File:\n{file_text}"

        # Modify the prompt based on the selected tone
        prompt_with_tone = f"Write this email in a {tone.lower()} tone:\n\n{prompt}"

        # Generate the email if the button is clicked
        if st.button('Generate Email'):
            try:
                # Generate email content using the AI model
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt_with_tone)
                
                # Display generated content
                if hasattr(response, 'text'):
                    st.write("Generated Email:")
                    st.write(response.text)
                else:
                    st.error("No valid content generated. Check the API response.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

import streamlit as st
from spellchecker import SpellChecker
from docx import Document

# Title
st.title("📄 AI Spell Checker (.docx or Text)")
st.write("Upload a Word document or type to check spelling mistakes.")

spell = SpellChecker()

def read_docx(file):
    doc = Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

# File uploader
uploaded_file = st.file_uploader("Upload a Word (.docx) file", type=["docx"])

# Manual input
user_input = st.text_area("Or enter text here:")

text_to_check = ""

if uploaded_file:
    text_to_check = read_docx(uploaded_file)
    st.success("Text extracted from file.")
elif user_input.strip():
    text_to_check = user_input

if st.button("Check Spelling") and text_to_check.strip():
    words = text_to_check.split()
    misspelled = spell.unknown(words)

    if not misspelled:
        st.success("No spelling mistakes!")
    else:
        st.error(f"Found {len(misspelled)} mistake(s):")
        for word in misspelled:
            st.markdown(f"❌ **{word}** ➡️ Suggestion: `{spell.correction(word)}`")

    corrected = ' '.join([spell.correction(w) if w in misspelled else w for w in words])
    st.markdown("### ✅ Corrected Text")
    st.text_area("Corrected Output:", corrected, height=200)

import streamlit as st
from openai import AzureOpenAI
import os
import codecs
from dotenv import load_dotenv
from llm import explain_code, suggest_code_improvements, generate_xml_comments, generate_unit_tests
from utils import read_sourcecode_file


# This code comes from https://www.mytechramblings.com/posts/building-a-csharp-enhancing-app-using-openai-gpt4-and-streamlit/
# Repo: https://github.com/karlospn/building-a-csharp-enhancing-app-with-openai-and-streamlit

# AOAI Python API: https://github.com/openai/openai-python?tab=readme-ov-file
# https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python

# AOAI Python lib migration from 0.28 to 1.0 : https://github.com/openai/openai-python/discussions/742


load_dotenv()

if os.getenv('AZURE_OPENAI_ENDPOINT') is None:
    st.error("AZURE_OPENAI_ENDPOINT not set. Please set this environment variable and restart the app.")
if os.getenv('AZURE_OPENAI_CHATGPT_DEPLOYMENT') is None:
    st.error("AZURE_OPENAI_CHATGPT_DEPLOYMENT not set. Please set this environment variable and restart the app.")
if os.getenv('AZURE_OPENAI_API_KEY') is None:
    st.error("AZURE_OPENAI_API_KEY not set. Please set this environment variable and restart the app.")


config = """
AZURE_OPENAI_ENDPOINT={AZURE_OPENAI_ENDPOINT}
AZURE_OPENAI_CHATGPT_DEPLOYMENT={AZURE_OPENAI_CHATGPT_DEPLOYMENT}
"""
config = config.format(AZURE_OPENAI_ENDPOINT= os.getenv('AZURE_OPENAI_ENDPOINT'), AZURE_OPENAI_CHATGPT_DEPLOYMENT= os.getenv('AZURE_OPENAI_CHATGPT_DEPLOYMENT'))

with st.expander("Parameters"):
    st.code(config)

def clear_state():
    for key in st.session_state.keys():
        del st.session_state[key]


st.title("C# Code Companion")

uploaded_file = st.file_uploader(label="Add a csharp file", type=["cs"], accept_multiple_files=False, on_change=clear_state)
if uploaded_file is not None:
    
    csharp_code = read_sourcecode_file(uploaded_file)
        
    with st.expander("Source code"):
        st.code(csharp_code, language='csharp')

    if st.button("Add XML comments"):
        with st.spinner("Generating XML comments..."):
            if 'xml_comments_csharp_code' in st.session_state.keys():
                with st.expander("Source code with XML comments"):
                    st.code(st.session_state['xml_comments_csharp_code'], language='csharp')   
            else:
                with st.expander("Source code with XML comments"):
                    xml_comments_csharp_code = generate_xml_comments(csharp_code)
                    if xml_comments_csharp_code is not None:
                        xml_comments_csharp_code = xml_comments_csharp_code.strip("```").lstrip("csharp").strip()
                    st.code(xml_comments_csharp_code, language='csharp')          
                    st.session_state['xml_comments_csharp_code'] = xml_comments_csharp_code

    if st.button("Explain code"):
        with st.spinner("Explaining code..."):
            if 'csharp_code_explained' in st.session_state.keys():
                st.markdown(st.session_state['csharp_code_explained'])
            else:
                csharp_code_explained = explain_code(csharp_code)

                #csharp_code_explained = explain_code(csharp_code)
                st.markdown(csharp_code_explained)
                st.session_state['csharp_code_explained'] = csharp_code_explained

    if st.button("Suggest code improvements"):
        with st.spinner("Searching for improvements..."):
            if 'csharp_code_improvements' in st.session_state.keys():
                st.markdown(st.session_state['csharp_code_improvements'])
            else:
                csharp_code_improvements = suggest_code_improvements(csharp_code)
                st.markdown(csharp_code_improvements)
                st.session_state['csharp_code_improvements'] = csharp_code_improvements

    if st.button("Generate unit tests"):
         with st.spinner("Trying to generate Unit Tests..."):
            if 'unit_tests_csharp_code' in st.session_state.keys():
                with st.expander("Unit Tests source code"):
                    st.code(st.session_state['unit_tests_csharp_code'], language='csharp')   
            else:
                with st.expander("Unit Tests source code"):
                    unit_tests_csharp_code = generate_unit_tests(csharp_code)
                    unit_tests_csharp_code = unit_tests_csharp_code.strip("```").lstrip("csharp").strip()
                    st.code(unit_tests_csharp_code, language='csharp')          
                    st.session_state['unit_tests_csharp_code'] = unit_tests_csharp_code



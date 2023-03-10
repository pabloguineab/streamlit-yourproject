# gpt3 professional email generator by stefanrmmr - version June 2022
from pathlib import Path
import os
import openai
import streamlit as st
from streamlit import runtime
from fpdf import FPDF
import base64
from streamlit_extras.stoggle import stoggle
import io
from pathlib import Path
import os
import openai
import streamlit as st
from streamlit import runtime
from fpdf import FPDF
import base64
from streamlit_extras.stoggle import stoggle
from jinja2 import Environment, FileSystemLoader, select_autoescape
# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="rephraise", page_icon="img/rephraise_logo.png",layout="wide")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("invoice_template.html")

def gen_project_contents(project_contents):
    new_contents = []
    for section in project_contents:
        input_text = section
        rephrased_content = ""
        while len(rephrased_content) == 0:  # continue generating until non-empty completion is produced
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Write a section of an academic project on the topic {section}, with the title '{project_contents[0]}'. The section should discuss the topic and its relevance to the project, and it should have at least 5 paragraphs.",
                temperature=0.6,
                max_tokens=len(input_text)*4,
                top_p=0.8,
                best_of=2,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=None  # allow completion to continue until max_tokens is reached
            )

            rephrased_content = response.choices[0].text.strip()

        # replace existing section text with updated
        new_contents.append(rephrased_content)

    return new_contents

def get_pdf_download_link(pdf_bytes, filename):
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" target="_blank">Download file</a>'
    return href

def gen_project_format(title, sections):
    # update the sections data with more formal statements
    new_sections = []
    project_final_text = []  # create an empty list for storing the OpenAI response for each section
    for i, section in enumerate(sections):
        if i == 0:  # title
            new_sections.append(section)
        elif i == 1:  # introduction
            intro_text = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Write an introduction for an academic project on the topic {section}, with the title '{title}'. The introduction should provide background information on the topic and explain why it is important to the project.",
                temperature=0.6,
                max_tokens=200,
                top_p=0.8,
                frequency_penalty=0.0,
                presence_penalty=0.0
            ).choices[0].text.strip()
            new_sections.append(intro_text)
            project_final_text.append(intro_text)  # append the OpenAI response to project_final_text
        elif i == len(sections) - 1:  # conclusion
            conclusion_text = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Write a conclusion for an academic project on the topic {section}, with the title '{title}'. The conclusion should summarize the main points of the project and provide some insights or suggestions for future work.",
                temperature=0.6,
                max_tokens=200,
                top_p=0.8,
                frequency_penalty=0.0,
                presence_penalty=0.0
            ).choices[0].text.strip()
            new_sections.append(conclusion_text)
            project_final_text.append(conclusion_text)  # append the OpenAI response to project_final_text
        else:  # other sections
            section_text = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Write a section of an academic project on the topic {section}, with the title '{title}'. The section should discuss the topic and its relevance to the project, and it should have at least 5 paragraphs.",
                temperature=0.6,
                max_tokens=200,
                top_p=0.8,
                frequency_penalty=0.0,
                presence_penalty=0.0
            ).choices[0].text.strip()
            new_sections.append(section_text)
            project_final_text.append(section_text)  # append the OpenAI response to project_final_text

    # concatenate sections into one text
    contents_str = "\n\n".join([f"\n\nSection {i+1}: {section}" for i, section in enumerate(new_sections[1:-1])])
    
    return contents_str, project_final_text

def generate_pdf(project_title, project_contents):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    contents_str, project_final_text = gen_project_format(project_title, project_contents)
    pdf.multi_cell(0, 10, txt=contents_str)
    for section in project_contents:
        pdf.cell(200, 10, txt=section, ln=1)
        pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes, project_final_text

def main_gpt3projectgen():
    
    st.image('img/image_banner.png')  # TITLE and Creator information
    st.markdown('Generate Accurate & Quality Academic Projects in Just Seconds')
    st.write('\n')  # add spacing

    st.subheader('\nWhat is your project about?\n')
    with st.expander("SECTION - Project Detail Inputs", expanded=True):
        input_title = st.text_input('Title of the project', 'My Project Title')
        input_section1 = st.text_input('Section 1 (Introduction)', 'Introduction')
        input_section2 = st.text_input('Section 2', '')
        input_section3 = st.text_input('Section 3', '')
        input_section4 = st.text_input('Section 4', '')
        input_section5 = st.text_input('Section 5', '')
        input_section6 = st.text_input('Section 6', '')
        input_section7 = st.text_input('Section 7', '')
        input_section8 = st.text_input('Section 8', '')
        input_conclusion = st.text_input('Conclusion', 'Conclusion')

    sections = [input_title, input_section1, input_section2, input_section3, input_section4, input_section5, input_section6, input_section7, input_section8, input_conclusion]
    sections = [section for section in sections if section]  # remove empty sections
    split_sections = [sections[i:i+3] for i in range(0, len(sections), 3)]  # split into groups of 3 or less

    project_final_text = ""

    import io
    import base64
    import pdfkit
    # UI code
    project_title = st.text_input("Project Title")
    project_contents = st.text_area("Project Contents (one section per line)").split("\n")
    if st.button("Generate Project"):
        with st.spinner(text='Generating project...'):
            project_contents = gen_project_contents(project_contents)
            project_final_text = gen_project_format(project_title, project_contents)
        st.write(project_final_text)
        if st.button("Download Project"):
        html = template.render(
            project_title=project_title,
            project_final_text=project_final_text,

        )

        pdf = pdfkit.from_string(html, False)
        st.balloons()

        st.success("???? Your project was generated!")

        st.download_button(
            "?????? Download PDF",
            data=pdf,
            file_name="project.pdf",
            mime="application/octet-stream",
        )
            
     
if __name__ == '__main__':
    main_gpt3projectgen()

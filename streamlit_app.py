# gpt3 professional email generator by stefanrmmr - version June 2022
from pathlib import Path
import os
import openai
import streamlit as st
from streamlit import runtime
from fpdf import FPDF
import base64
from streamlit_extras.stoggle import stoggle

# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="rephraise", page_icon="img/rephraise_logo.png",)
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




def gen_project_contents(project_contents):

    # iterate through all separate sections
    for section in range(len(project_contents)):
        input_text = project_contents[section]
        rephrased_content = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write a section of an academic project on the topic {input_text}, with the title '{project_contents[0]}'. The section should discuss the topic and its relevance to the project, and it should have at least 5 paragraphs.",
            temperature=0.8,
            max_tokens=len(input_text)*5,
            top_p=0.8,
            best_of=2,
            frequency_penalty=0.0,
            presence_penalty=0.0)

        # replace existing section text with updated
        project_contents[section] = rephrased_content.get("choices")[0]['text']
    return project_contents


def gen_project_format(title, sections):
    # update the sections data with more formal statements
    sections = gen_project_contents(sections)
    # st.write(sections)  # view augmented contents

    contents_str, contents_length = "", 0
    for section in range(len(sections)):  # aggregate all sections into one
        contents_str = contents_str + f"\nSection {section+1}: " + sections[section]
        contents_length += len(sections[section])  # calc total chars

    project_final_text = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write an academic project with the title '{title}', consisting of the following sections:{contents_str}\n",
        temperature=0.6,
        max_tokens=3000,
        top_p=0.8,
        best_of=1,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return project_final_text.get("choices")[0]['text']


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

    project_text = gen_project_format(input_title, sections)

    st.write('\n\n\n\n\n')  # add spacing
    with st.expander("SECTION - Generated Text", expanded=True):
        st.write(project_text)

if project_text != "":
        st.write('\n')  # add spacing
        st.subheader('\nDownload your Project\n')       
        pdf = FPDF()  # pdf object
        pdf = FPDF(orientation="P", unit="mm", format="Legal")
        pdf.add_page()
        STRIPE_CHECKOUT = "https://buy.stripe.com/5kAdRQbCC70Y2hG8wx"
        pdf.set_font("Times")
        pdf.cell(60,10,'Introduction',0,1,'C');
        pdf.set_xy(20.0, 20.0)  # adjust x and y position to set the margins
        pdf.multi_cell(w=170.0, h=5.0, align="L", txt=project_text)  # use multi_cell to wrap the text
        st.markdown(
            f'<a href={STRIPE_CHECKOUT} class="button">👉 Get Complete Project --> Proceed to payment</a>',
            unsafe_allow_html=True,
        )
        st.download_button(
            "Download Preview",
            data=pdf.output(dest='S').encode('latin-1'),
            file_name="yourproject.pdf",
        )

        stoggle("Click me!", """🥷 Surprise!""",)
        
if __name__ == '__main__':
    if runtime.exists():
        main_gpt3emailgen()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
    
    
    

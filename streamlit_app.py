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



def gen_mail_contents(email_contents):

    # iterate through all seperate topics
    for topic in range(len(email_contents)):
        input_text = email_contents[topic]
        rephrased_content = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write an introduction for a research paper with the title {input_text}, The introduction should provide an overview of the research topic, its significance, and a summary of the contents in the paper and need to has minimum 7 paragraphs. The keywords of the project are {input_text}. After writing the introduction, continue developing the rest of the sections of the project.",
            # prompt=f"Rewrite the text to sound professional, elaborate and polite.\nText: {input_text}\nRewritten text:",
            temperature=0.8,
            max_tokens=len(input_text)*8,
            top_p=0.8,
            best_of=2,
            frequency_penalty=0.0,
            presence_penalty=0.0)

        # replace existing topic text with updated
        email_contents[topic] = rephrased_content.get("choices")[0]['text']
    return email_contents




def gen_mail_format(sender, recipient, style, email_contents):
    # update the contents data with more formal statements
    email_contents = gen_mail_contents(email_contents)
    # st.write(email_contents)  # view augmented contents

    contents_str, contents_length = "", 0
    for topic in range(len(email_contents)):  # aggregate all contents into one
        contents_str = contents_str + f"\nContent{topic+1}: " + email_contents[topic]
        contents_length += len(email_contents[topic])  # calc total chars

    email_final_text = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write an introduction for a research paper with the title  {contents_str}, The introduction should provide an overview of the research topic, its significance, and a summary of the contents in the paper and need to has minimum 7 paragraphs. After the introduction, the rest of the sections of the project are developed in detail.\n",
        # prompt=f"Write a professional sounding email text that includes all of the following contents separately.\nThe text needs to be written to adhere to the specified writing styles and abbreviations need to be replaced.\n\nSender: {sender}\nRecipient: {recipient} {contents_str}\nWriting Styles: motivated, formal\n\nEmail Text:",
        temperature=0.9,
        max_tokens= 4000,
        top_p=0.8,
        best_of=1,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return email_final_text.get("choices")[0]['text']


def main_gpt3emailgen():

    st.image('img/image_banner.png')  # TITLE and Creator information
    st.markdown('Generate Accurate & Quality Projects Degree in Just Seconds and get Full Marks This Course')
    st.write('\n')  # add spacing

    st.subheader('\nWhat is your Project about?\n')
    with st.expander("SECTION - Project Detail Inputs", expanded=True):

        input_c1 = st.text_input('Enter relevant information about the topic down below! (currently 2x seperate topics supported)', 'Title of the Project')
        input_c2 = st.text_input('Enter 10 keywords that you consider relevant to mention in the project', 'Keywords')
        input_c3 = st.text_input('Copy and Paste the Abstract', 'Abstract or Summary')

        email_text = ""  # initialize columns variables
        col1, col2, col3, space, col4 = st.columns([5, 5, 5, 0.5, 5])
        with col1:
            input_sender = st.text_input('N.Pages', '60')
        with col2:
            input_recipient = st.text_input('Font', 'Arial')
            
        with col3:
            input_style = st.selectbox('Citation format',
                                       ('APA', 'IEEE', 'Harvard'),
                                       index=0)
        with col4:
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing
            if st.button('Generate Project'):
                with st.spinner():

                    input_contents = []  # let the user input all the data
                    if (input_c1 != "") and (input_c1 != 'Title of the Project'):
                        input_contents.append(str(input_c1))
                    if (input_c2 != "") and (input_c2 != 'Keywords'):
                        input_contents.append(str(input_c2))

                    if (len(input_contents) == 0):  # remind user to provide data
                        st.write('Please fill in some contents for your message!')
                    if (len(input_sender) == 0) or (len(input_recipient) == 0):
                        st.write('Sender and Recipient names can not be empty!')

                    if (len(input_contents) >= 1):  # initiate gpt3 mail gen process
                        if (len(input_sender) != 0) and (len(input_recipient) != 0):
                            email_text = gen_mail_format(input_sender,
                                                         input_recipient,
                                                         input_style,
                                                         input_contents)
    if email_text != "":
        st.write('\n')  # add spacing
        st.subheader('\nDownload your Project\n')       
        pdf = FPDF()  # pdf object
        pdf = FPDF(orientation="P", unit="mm", format="Legal")
        pdf.add_page()
        STRIPE_CHECKOUT = "https://buy.stripe.com/14kdRQfSS1GEf4s8ww"
        pdf.set_font("Times", 12)
        pdf.set_xy(20.0, 20.0)  # adjust x and y position to set the margins
        pdf.multi_cell(w=170.0, h=5.0, align="L", txt=email_text)  # use multi_cell to wrap the text
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
    
    
    

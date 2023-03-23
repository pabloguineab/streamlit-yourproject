import os
import openai
import streamlit as st
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pdfkit

# Set the appropriate configuration for Streamlit and OpenAI
st.set_page_config(page_title="Research Project Generator", layout="wide")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Jinja2 environment and template
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("invoice_template.html")

def generate_pdf(project_title, project_contents):
    html = template.render(
        project_title=project_title,
        project_contents=project_contents,
    )
    pdf = pdfkit.from_string(html, False)
    return pdf

def generate_project_section(section_title, project_title, prompt, max_tokens=200):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=max_tokens,
        top_p=0.8,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    section_text = response.choices[0].text.strip()
    return f"{section_title}\n\n{section_text}\n"

def main():
    st.title("Research Project Generator")
    st.write("Generate a Research Project using YourProject.ai")

    project_title = st.text_input("Project Title")
    st.markdown("Enter the titles for the sections you want to include in the project (Introduction, Conclusion, etc.):")
    
    user_sections = st.text_area("Section Titles (one per line)").split("\n")

    if st.button("Generate Project"):
        with st.spinner(text='Generating project...'):
            project_contents = []
            for i, title in enumerate(user_sections):
                if i == 0:
                    prompt = f"Write an introduction for a research project titled '{project_title}'. The introduction should provide background information on the topic and explain why it is important to the project."
                elif i == len(user_sections) - 1:
                    prompt = f"Write a conclusion for a research project titled '{project_title}'. The conclusion should summarize the main points of the project and provide some insights or suggestions for future work."
                else:
                    prompt = f"Write a section of a research project on the topic {title}, with the title '{project_title}'. The section should discuss the topic and its relevance to the project, and it should have at least 5 paragraphs."
                section = generate_project_section(title, project_title, prompt)
                project_contents.append(section)
                st.write(section)
            if project_contents:
                pdf = generate_pdf(project_title, project_contents)
                st.balloons()
                st.success("🎉 Your project was generated!")
                st.download_button(
                    "Download PDF",
                    data=pdf,
                    file_name=f"{project_title}.pdf",
                    mime="application/octet-stream",
                )

if __name__ == "__main__":
    main()

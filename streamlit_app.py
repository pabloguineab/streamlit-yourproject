
    
import streamlit as st
import openai



# Define the fields
fields = ["Project Title", "Subject", "Area"]

# Initialize the form data
form_data = {"Project Title": "", "Subject": "", "Area": ""}

# Create a function to generate the content for a field
def generate_field(field):
    # Prompt the user for input
    prompt = "Enter the content for the " + field + " field:"
    content = st.text_input(prompt)
    
    # Use OpenAI to generate content for the field
    model_engine = "text-davinci-002"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    content += message
    return content

# Create a function to download the content as a PDF
def download_pdf(content):
    # TODO: Write the code to convert the content to a PDF and download it
    pass

# Main function to build the form
def main():
    # Add a title for the form
    st.title("Academic Project Generator")
    
    # Add a form for the user to enter the project details
    form_data["Project Title"] = st.text_input("Project Title")
    form_data["Subject"] = st.text_input("Subject")
    form_data["Area"] = st.text_input("Area")
    
    # Add a button to generate the content for each field
    for field in fields:
        st.write("")
        if st.button("Generate " + field):
            form_data[field] = generate_field(field)
    
    # Display the generated content for each field
    for field in fields:
        st.write("")
        st.write("### " + field)
        st.write(form_data[field])
    
    # Add a button to download the content as a PDF
    if st.button("Download PDF"):
        content = "\n".join([field + ": " + form_data[field] for field in fields])
        download_pdf(content)

# Run the form
if _name_ == "_main_":
    main()

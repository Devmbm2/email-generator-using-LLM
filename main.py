import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from pipelines import Pipeline
from projects import ProjectCollection
from helpers import sanitize_text

def create_email_generator_app(language_model, projects, sanitize):
    st.title("Cold Email Generator Tool")
    url_input = st.text_input("Enter a URL:", value="Paste the job post link here ...")
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            content_loader = WebBaseLoader([url_input])
            cleaned_data = sanitize(content_loader.load().pop().page_content)
            projects.load_projects()
            job_details = language_model.extract_positions(cleaned_data)
            for position in job_details:
                required_skills = position.get('skills', [])
                related_links = projects.search_links(required_skills)
                generated_email = language_model.compose_email(position, related_links)
                st.code(generated_email, language='markdown')
        except Exception as err:
            st.error(f"An Error Occurred: {err}")

if __name__ == "__main__":
    language_model = Pipeline()
    projects = ProjectCollection()
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    create_email_generator_app(language_model, projects, sanitize_text)

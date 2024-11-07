import streamlit as st
from backend.pdf_ingestion import load_and_split_pdf
from backend.vector_store import create_vector_store
from backend.analysis import analyze_resume
import os
import shutil

# def clear_all_inputs():
#     """
#     Clears all input fields and session states related to resume analysis.
#     """
#     st.session_state.resume_file = None
#     st.session_state.job_description = ""
#     st.session_state.vector_store = None
#     st.session_state.analysis = None

def render_main_app():
    """
    Main application including upload resume and analyse resume.
    """

    # applying custom cs
    with st.sidebar:

        # inputs
        st.header("Upload Resume")
        resume_file = st.file_uploader("Upload Resume in PDF format", type="pdf")

        # text area for job desc
        st.header("Add Job Description")
        job_description = st.text_area("Enter Job Description", height=300)
        
        if resume_file and job_description:
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)

            # saving uploaded file to a temp dir
            with open(os.path.join(temp_dir, resume_file.name),"wb") as f:
                f.write(resume_file.getbuffer())

            # load and split the pdf file into docs and chunks
            resume_file_path = os.path.join(temp_dir, resume_file.name)
            resume_docs, resume_chunks = load_and_split_pdf(resume_file_path)

            # create a vector store from chunks
            vector_store = create_vector_store(chunks=resume_chunks)
            st.session_state.vector_store = vector_store

            # remove the temp dir
            shutil.rmtree(temp_dir)

            # button to begin resume analysis
            if st.button("Analyze Resume", help="Click to analyze the resume"):
                # combining all the resume chunks to one , to send it for analysis
                full_resume = " ".join([doc.page_content for doc in resume_chunks])
                analysis = analyze_resume(full_resume=full_resume, description=job_description)
                st.session_state.analysis = analysis
        else:
            st.info("Please upload a resume and enter job description to begin.")
    
    # display analysis results if present in session state
    if "analysis" in st.session_state:
        st.header("Resume Job Compatibility Analysis")
        st.write(st.session_state.analysis)
    else:
        st.header("welcome to the Resume Analysis Tool!")
        st.subheader("Your one-stop solution for all your resume analysis requiremnets.")
        st.info("Do you want to check the resume compatibility with the job description? Then right away hit that upload resume button :)")

        steps = ["Upload a Resume", "Enter a Job Description", "Click on Analyze Resume"]
        st.markdown("\n".join([f"#### {i+1}. {step}"for i,step in enumerate(steps)]))




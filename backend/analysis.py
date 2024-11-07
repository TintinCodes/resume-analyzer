import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model_name="mixtral-8x7b-32768")

def analyze_resume(full_resume, description):
    """
    Main function to analyse the resume alongside the job description
    """

    # add more instruction to the prompt
    template = """
        You are a helpful AI assistant specialised in resume analysis. Your task is to analyse and compare the given resume with the job description.
        Always respond in the provided "Example Response Structure:". Do not miss anything from it. 
        Example Response Structure:

        **OVERVIEW**:
        - **Match Percentage**: [Calculate overall match percentage between the resume and job description]
        - **Match Skills**: [List the skills in the job description that match the resume]
        - **Unmatched Skills**: [List the skills in the job description that are missing in the resume]
        - **Company Names**: [List the names of the companies which are mentioned in professional experience.]

        **DETAILED ANALYSIS**:
        Provide a detailed analysis about:
        1. Overall match percentage between the resume and job description.
        2. List of skills from the job description that match the resume.
        3. List of skills from the job description that are missing in the resume.

        **Additional Comments**:
        Additional comments about the resume and suggestions for the recruiter or HR manager.

        Resume: {resume}
        Job Description: {job_description}

        Analysis:
    """

    prompt = PromptTemplate(input_variables=["resume", "job_description"],
                   template=template)
    chain = prompt | llm
    print(f"chain:{chain}")
    result = chain.invoke({"resume": full_resume, "job_description": description})

    print(f"result:{result}")
    return result.content



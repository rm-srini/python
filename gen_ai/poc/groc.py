from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import docx
from langchain_community.document_loaders import TextLoader
import chromadb
import pandas as pd

"""
Below block of code is docx library to read a MS word document and convert it into text format
As of now I have not done any splits, in the actual code based on the token size we can split using 
RecursiveCharacterTextSplitter
We Should also have capability to read .doc, .docx, .txt, .pdf, web based files 
"""
file_path = r'Resume_Srinivasan_1.6.docx'
doc = docx.Document(file_path)
resume_text = ""
for para in doc.paragraphs:
    resume_text += para.text + "\n"

"""
Conneting to ChatGroq which is a opensource AI interface which provides API 
reference to LLM models. In this code I have used LLAMA 3.1
"""
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    groq_api_key="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"
    # other params...
)


"""
Creating a prompt text to extract following details in JSON format from the resume
Name
Mobile Number
Email
Experience 
Skill
Role
Shot Description
"""
prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {data}
    ### INSTRUCTION:
    The text is from a resume
    Your job is to extract the information and return them in JSON format containing the following keys: 'name', 
    'mobile_number', 'email', 'experience', 'skills', 'role' and 'short description'.
    Only return the valid JSON.
    ### VALID JSON (NO PREAMBLE):
    """
)
chain_extract = prompt_extract | llm
res = chain_extract.invoke(input={"data": resume_text})

json_parser = JsonOutputParser()
resume_info = json_parser.parse(res.content)



"""
Creating a prompt text to extract following details in JSON format from the Job description 
Role
Experience 
Skill
Description
"""
documents = []
loader = TextLoader('job_description.txt')
documents.extend(loader.load())

prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    This is  text from the career's page of a website.
    Your job is to extract the job postings and return them in JSON format containing the following keys: 
    `role`, `experience`, `skills` and `description`.
    Only return the valid JSON.
    ### VALID JSON (NO PREAMBLE):
    """
)
chain_extract = prompt_extract | llm
res = chain_extract.invoke(input={"page_data": documents[0]})

json_parser = JsonOutputParser()
jd_info = json_parser.parse(res.content)


""""
Using Chroma DB which is a open source Vector DB we are performing a semantic search
to get the match between the JD and the resume
Lot of fine tuning can be done here, at a high level I'm just this code for POC
if the number is neared to 0 then its more close  
"""

resume_info['skills'] = ', '.join(resume_info['skills'])


client = chromadb.Client()
resume_collection = client.create_collection(name='resume_collection')
resume_collection.add(
    documents=[resume_info['skills'], resume_info['experience'], resume_info['role']],
    ids=['skills', 'exp', 'role']
)

skill_match_score = resume_collection.query(
    query_texts=[', '.join(jd_info['skills'])]
)['distances'][0][0]

exp_match_score = resume_collection.query(
    query_texts=[jd_info['experience']]
)['distances'][0][0]

role_match_score = resume_collection.query(
    query_texts=[jd_info['role']]
)['distances'][0][0]



resume_info['skill_match_score'] = skill_match_score
resume_info['exp_match_score'] = exp_match_score
resume_info['role_match_score'] = role_match_score


result = pd.DataFrame(resume_info, index=[0])
result.to_csv('output.csv', index=0)

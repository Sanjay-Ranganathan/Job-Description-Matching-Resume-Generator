from fastapi import FastAPI, Request
from llama_cpp import Llama
# from model import llm
from pydantic import BaseModel

llm = Llama(
    model_path='llama-7b.Q6_K.gguf',
    n_ctx=2048,
    n_threads=6
)

app = FastAPI()

class TxtPayload(BaseModel):
    JobDes:str
    ResText:str

@app.post('/analyze')
async def res_analyze(payload : TxtPayload):
    prompt = f"""
    You're a Professional Resume Rewriter with 100% resume shortlist possibility based on Job description.
    The Job description : 
    {payload.JobDes}
    ...
    Now For this Job Description, Rewrite this Resume As I told You
    {payload.ResText}
    Rewrite the resume so that it is tailored to the job. Use clear, professional formatting with the following sections:

    1. Summary
    2. Skills
    3. Professional Experience
    4. Education

    Use bullet points where appropriate. Make sure to incorporate keywords from the job description, and use concise language with action verbs (e.g., "Led", "Developed", "Implemented").

    Return only the formatted resume.
    """
    res = llm(prompt=prompt, max_tokens=1024)
    return {"Message" : "Successfully processed",
            "Resume" : res["choices"][0]["text"]}
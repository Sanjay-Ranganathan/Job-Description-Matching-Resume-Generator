import streamlit as st
import requests as rq
import pdfplumber as pr
from docx import Document
import io

doc = Document()

st.title("Resume Enchancer")
jobDes = st.text_area("Job Description",height=300)
file = st.file_uploader('Upload Resume',type=['pdf','docx'])
if st.button("Analyze"):
    res_con=''
    jdes = ''
    if file is None and not jobDes:
        st.warning("Please upload Resume and Job Description")
    if file is not None:
        with pr.open(file) as pdf:
            for page in pdf.pages:
                res_con+=page.extract_text()
    if jobDes:
        jdes = jobDes
    prompt = f"""
            You are a professional resume writer.
            Rewrite this resume to match the job description. 100% shortlisted.

            Job Description:
            {jdes}

            Resume:
            {res_con}

            Now rewrite the resume("ONLY GIVE RESUME CONTENTS"):
            """
    pld = {'prompt' : prompt, 'max_new_tokens' : 2048}
    res = rq.post("https://7dfc-35-190-186-202.ngrok-free.app/gen",json=pld)
    if res.status_code == 200:
        st.success("Resume Created")
        resume = res.json().get("output")
        # st.success(resume)
        flg=False
        for line in resume.strip().split('\n'):
            if line.strip()=='Now rewrite the resume("ONLY GIVE RESUME CONTENTS"):'.strip():
                flg = True
                continue
            #st.success(line+str(flg))
            if flg:
                doc.add_paragraph(line.strip())
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="Download Resume",
            data=buffer,
            file_name="Resume_New.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.warning(f"{res.status_code} : Internal Server Error")
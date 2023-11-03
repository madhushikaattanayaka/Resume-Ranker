from flask import Flask, render_template, request
import os
from model import ResumeRanker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rank', methods=['POST'])
def rank():
    resume_files = request.files.getlist('resume')
    job_description_file = request.files['job_description']

    resumes = []
    for resume_file in resume_files:
        resume = resume_file.read().decode('utf-8')
        resumes.append(resume)

    job_description = job_description_file.read().decode('utf-8')

    resume_ranker = ResumeRanker()
    ranked_resumes = resume_ranker.rank_resumes(resumes, job_description)

    return render_template('rank.html', ranked_resumes=ranked_resumes)

if __name__ == '__main__':
    app.run(debug=True)

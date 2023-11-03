import re
import os
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords as stp

class ResumeRanker:
    def __init__(self):
        self.stopwords = set(stp.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def lemmatize_text(self, text):
        return " ".join([self.lemmatizer.lemmatize(word) for word in re.findall(r'\w+', text)])
    
    def preprocess_text(self, text):
        text = text.lower()
        text = self.lemmatize_text(text)
        return text
    
    def rank_resumes(self, resumes, query):
        query = self.preprocess_text(query)
        resumes = [self.preprocess_text(resume) for resume in resumes]

        X = self.vectorizer.fit_transform(resumes)
        query_vector = self.vectorizer.transform([query])

        similarity = cosine_similarity(X, query_vector)
        similarity = similarity.flatten()

        ranked_resumes = [(resumes[i], similarity[i]) for i in range(len(resumes))]
        ranked_resumes = sorted(ranked_resumes, key=lambda x: x[1], reverse=True)

        return ranked_resumes

resume_ranker = ResumeRanker()

resumes = []
while True:
    resume_file = input("Enter the path to the resume text file, or type 'done' if you're finished: ")
    if resume_file.lower() == "done":
        break
    with open(resume_file, "r", encoding="utf8", errors='ignore') as file:
        resume = file.read()
    resumes.append(resume)

query = input("Enter the job description text: ")



ranked_resumes = resume_ranker.rank_resumes(resumes, query)

for i, (resume, score) in enumerate(ranked_resumes):
    file_path = resume_file[i]
    file_name = os.path.basename(file_path).split(".")[0]
    print("Resume file:", file_name)
    print("Cosine similarity score:", score)


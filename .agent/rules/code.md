---
trigger: always_on
---

All data work must be done inside Jupyter Notebooks

EDA

visualizations

insights

model interpretation

notes, conclusions

why this model? what does this graph show?



All core logic must be inside src/ Python files

preprocessing

embedding pipeline

feature extraction

ML model class

utility functions

API endpoints

agent code

UI scripts
→ No comments inside .py files



Code Style Rules

Human-written style (not AI-perfect)

Variable names should be short + meaningful

No long function names

Keep functions simple and modular



Notebook Rules

All explanations must be in markdown cells only

Explain:

why we used this model

why this metric matters

interpretation of every graph

mistakes & limitations

future improvements

No unnecessary text, make it crisp and insightful



ML Pipeline Rules

Reproducible

Use config files for model paths & params

Use embedding models like:

sentence-transformers/all-MiniLM-L6-v2

instructor-xl

Use cosine similarity for baseline

Use ML/DL ranking networks for advanced stage

Use JSON structured output

Use tools only when required

UI/Deployment Rules

Streamlit UI must be minimal, clean, functional

Backend: FastAPI with modular routes

Cloud deploy using Render / HF / Cloud Run

No unnecessary packages

Versioning Rules

Every stage of project saved in organized folders

Keep reproducible pipeline from data → model → UI
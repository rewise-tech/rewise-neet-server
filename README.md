# rewise-neet-server

### Quick start

```bash
# install deps (creates .venv managed by uv)
uv sync

# run dev server
uv run uvicorn main:app --reload

# question json 

{
    "source": "string",
    "year": "string",
    "subject": "string",
    "chapter": "string",
    "topic": "string",
    "question_number": "string",
    "question_text": "string",
    "has_diagram": true or false,
    "diagram_description": "string",
    "diagram_position": "string",
    "diagram_name": "string",
    "answer": "string",
    "solution": "string",
    "reviewed": true or false,
    "options": [
        {
            "label": "string",
            "text": "string",
            "has_diagram": true or false,
            "diagram_description": "string",          
            "diagram_name": "string"
        }
    ]
}

# question json sample


http://0.0.0.0:8000/api/process-questions/
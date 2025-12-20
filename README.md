# rewise-neet-server

### Quick start

```bash
# install deps (creates .venv managed by uv)
uv sync

# run dev server
uv run uvicorn app.main:app --reload



{
    "source": "string",
    "year": "string",
    "question_number": "string",
    "question_text": "string",
    "has_diagram": true or false,
    "diagram_description": "string",
    "diagram_position": "string",
    "diagram_name": "none",
    "answer": "string",
    "solution": "string",
    "reviewed": true or false,
    "options": [
        {
            "label": "string",
            "text": "string",
            "option_has_diagram": true or false,
            "option_diagram_description": "string",          
            "option_diagram_name": "none"
        }
    ],
}
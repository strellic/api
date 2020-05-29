# OCF API

An authenticated API for the OCF.

# Developing locally

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
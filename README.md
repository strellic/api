# OCF API

An authenticated API for the OCF.

# Developing locally

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
python -m uvicorn app.main:app --reload
```

# Testing 

If you're testing an application, make sure to point it at the port on localhost
specified by uvicorn.

You can also test endpoints directly at `/docs`. You can even test authenticated
endpoints by logging in on that page with OCF Keycloak SSO. Use a `client_id` of
`ocfapi` and a blank client secret, and it should log you in.
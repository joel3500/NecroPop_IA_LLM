Flask app that extracts a family graph (LLM) and renders a compact Graphviz tree.
Local: cd backend && pip install -r requirements.txt && python -m backend.main
Render: Blueprint with rootDir: backend, startCommand: gunicorn main:app …, apt.txt installs graphviz.
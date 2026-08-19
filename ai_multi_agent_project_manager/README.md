# AI Multi-Agent Project Management System

A beginner-friendly multi-agent software project manager built with Python + Flask.

## Included agents

1. Requirement Agent
2. Planning Agent
3. Development Agent (represented through development task generation)
4. Testing Agent
5. Risk Agent
6. Scheduling Agent
7. Progress Agent

## How to run in VS Code

### 1. Open the project

Extract the ZIP and open the folder in VS Code.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

If PowerShell blocks activation, you can avoid activation and use the venv Python directly:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe app.py
```

Or, if activation works:

```powershell
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 3. Open the website

Go to:

http://127.0.0.1:5000

### 4. Test it

Enter:

Build an online examination system with student login, admin panel, question management, exam timer, automatic evaluation and result generation.

Click **Analyze Project**.

## Architecture

Browser -> Flask API -> ProjectManager -> Specialized Agents -> JSON -> Dashboard

## Important

This version intentionally uses local Python logic and requires NO paid API key.

For a more advanced college project, the next upgrade is to connect each agent to an LLM and add shared memory, task dependencies, ML-based risk prediction, authentication, database storage, and project progress updates.

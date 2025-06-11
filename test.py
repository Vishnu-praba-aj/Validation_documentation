import time
import requests
import json
from jinja2 import Template
import google.generativeai as genai

GITHUB_API = "https://api.github.com"
BITBUCKET_API = "https://api.bitbucket.org/2.0"
REPO_URL = "https://github.com/tas-neem/sample"
MAX_FILES = 10 
LANGUAGES = [".java", ".js"]
EXCLUDE_DIRS = ["test", "tests", "mock", "docs", "examples", "node_modules", "build"]
CHUNK_SIZE = 2_000 

genai.configure(api_key="") 

def is_excluded(path):
    return any(part in path.split("/") for part in EXCLUDE_DIRS)

def get_github_files(repo_url):
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    branch = "main"
    tree_url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(tree_url)
    if res.status_code != 200:
        raise Exception(f"Error fetching tree: {res.status_code} {res.text}")
    files = res.json().get("tree", [])

    code_files = []
    for f in files:
        path = f["path"]
        if not path.endswith(tuple(LANGUAGES)) or is_excluded(path):
            continue
        if f["type"] != "blob":
            continue
        if len(code_files) >= MAX_FILES:
            break
        code_files.append(f)
    return owner, repo, branch, code_files

def get_bitbucket_files(repo_url):
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    branch = "main"
    files = []
    next_url = f"{BITBUCKET_API}/repositories/{owner}/{repo}/src/{branch}/"
    while next_url and len(files) < MAX_FILES:
        res = requests.get(next_url)
        if res.status_code != 200:
            break
        data = res.json()
        for val in data.get("values", []):
            path = val.get("path", "")
            if not path.endswith(tuple(LANGUAGES)) or is_excluded(path):
                continue
            if len(files) >= MAX_FILES:
                break
            files.append({"path": path})
        next_url = data.get("next")
    return owner, repo, branch, files

def download_file(owner, repo, branch, path, provider="github"):
    if provider == "github":
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    else:
        raw_url = f"https://bitbucket.org/{owner}/{repo}/raw/{branch}/{path}"
    res = requests.get(raw_url)
    return res.text if res.status_code == 200 else ""

def analyze_code(code):
    docs = []
    chunks = [code[i:i+CHUNK_SIZE] for i in range(0, len(code), CHUNK_SIZE)]
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    for i, chunk in enumerate(chunks):
        prompt = f"""
You are a highly skilled software documentation generator. Your goal is to analyze the following source code and produce structured, accurate, and complete technical documentation in JSON format.
Instructions:
Understand the code context, classes, functions, and data structures and Carefully extract:
  1. class_name: Name of the main class (or interface/module)
  2. purpose: High-level explanation of the class/module/function
  3. attributes: A list of class attributes with name,type (if inferrable), validations (e.g., non-null, regex, range checks)
  4. methods: A list of public or exposed methods with name, input parameters with types, return type (if applicable) and a clear description of the purpose
  5. inferred_requirements: Functional or business requirements the code is implementing
Format your response strictly in the following JSON schema:
{{
  "class": "...",
  "purpose": "...",
  "attributes": [
    {{ "name": "...", "type": "...", "validations": ["..."] }}
  ],
  "methods": [
    {{ "name": "...", "params": {{"param1": "type1"}}, "returns": "...", "description": "..." }}
  ],
  "requirements": [
    "..."
  ]
}}
Here is the source code chunk {i+1}/{len(chunks)}:
{chunk}
"""
        for attempt in range(3):  
            try:
                response = model.generate_content(prompt)
                parsed = json.loads(response.text)
                docs.append(parsed)
                break 
            except Exception as e:
                if "429" in str(e):
                    delay = 60
                    print(f"Rate limit hit for chunk {i+1}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Skipping chunk {i+1} due to error: {e}")
                    break
    return docs

HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head><title>Code Documentation</title></head>
<body>
<h1>AI-Generated Code Documentation</h1>
{% for doc in docs %}
  <h2>{{ doc.class }}</h2>
  <p><strong>Purpose:</strong> {{ doc.purpose }}</p>
  <h3>Attributes</h3>
  <ul>
    {% for attr in doc.attributes %}
      <li>{{ attr.name }} ({{ attr.type }}): {{ ", ".join(attr.validations) }}</li>
    {% endfor %}
  </ul>
  <h3>Methods</h3>
  <ul>
    {% for method in doc.methods %}
      <li>{{ method.name }}({{ method.params|join(', ') }}): {{ method.description }} {% if method.returns %}<em>→ {{ method.returns }}</em>{% endif %}</li>
    {% endfor %}
  </ul>
  <h3>Requirements</h3>
  <ul>
    {% for req in doc.requirements %}
      <li>{{ req }}</li>
    {% endfor %}
  </ul>
{% endfor %}
</body>
</html>
""")

def main():
    provider = "github" if "github.com" in REPO_URL else "bitbucket"
    if provider == "github":
        owner, repo, branch, files = get_github_files(REPO_URL)
    else:
        owner, repo, branch, files = get_bitbucket_files(REPO_URL)

    docs = []
    for file in files:
        print(f"Processing: {file['path']}")
        code = download_file(owner, repo, branch, file['path'], provider)
        try:
            file_docs = analyze_code(code)
            docs.extend(file_docs)
        except Exception as e:
            print(f"Error processing {file['path']}: {e}")

    html = HTML_TEMPLATE.render(docs=docs)
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Documentation generated ")

if __name__ == "__main__":
    main()

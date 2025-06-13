# Validation Documentation Extractor

This tool automatically extracts requirements and input validation rules from a repository and generates a well-formatted Markdown documentation file.

## Features

- **Automatic Code Analysis:** Scans code in a repository for validation logic.
- **AI-Powered Extraction:** Uses an LLM to identify and summarize validation rules.
- **Markdown Output:** Generates a clean, readable Markdown file with tables for each class/object.
- **Easy to Use:** Provide a repo URL and get your documentation.

## Usage

1. **Clone this repository:**
    ```sh
    git clone https://github.com/yourusername/validation-documentation.git
    cd validation-documentation
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the tool:**
    ```sh
    python main.py
    ```
    - Enter the GitHub repository URL when prompted.

4. **View the output:**
    - The tool generates a Markdown file named `<repo>_validation.md` in the current directory.
    - Open it in VS Code or any Markdown viewer for a formatted view.
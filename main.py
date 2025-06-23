import os
from input.handler import get_input_files
from core.processor import process_files

def main():
    source = input("Enter a repo URL: ").strip()
    repo_name = source.split("/")[-1].split("\\")[-1]
    file_objs = get_input_files(source)
    output_tables = process_files(file_objs)

    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{repo_name}_validation.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Validation Documentation: {repo_name}\n\n")
        for table in output_tables:
            f.write(table + "\n\n")
    print(f"Documentation generated: {output_path}")

if __name__ == "__main__":
    main()
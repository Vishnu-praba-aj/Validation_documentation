import os
from sentence_transformers import SentenceTransformer, util
from deepdiff import DeepDiff
from core.validation_processor import process_validation
from core.document_processor import process_document
from input.handler import handle_input
from utils.document_utils import parse_json

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(a, b):
    emb1 = model.encode(a, convert_to_tensor=True)
    emb2 = model.encode(b, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item()

def test_document_agent(file_path, fields_txt, user_prompt="", runs=3):
    result = handle_input(file_path, fields_txt)
    if result["type"] != "document":
        raise ValueError("Input must be a document")

    outputs = []
    for i in range(runs):
        response = process_document(result["text"], result["fields"], user_prompt)
        outputs.append(response)
        print(f"Run {i+1} Output:\n{response[:500]}...\n") 

    base = outputs[0]
    similarities = [semantic_similarity(base, other) for other in outputs[1:]]
    avg_score = sum(similarities) / len(similarities)
    print(f"DocumentAgent Semantic Consistency Score: {avg_score:.4f}")

    try:
        jsons = [parse_json(o) for o in outputs]
        diffs = [DeepDiff(jsons[0], j) for j in jsons[1:]]
        for idx, diff in enumerate(diffs):
            print(f"Run {idx+2} structural diff:\n{diff}\n")
    except Exception as e:
        print(f"Error parsing output to JSON: {e}")

def test_validation_agent(repo_url, runs=3):
    result = handle_input(repo_url)
    if result["type"] != "code_repo":
        raise ValueError("Input must be a code repo")

    outputs = []
    for i in range(runs):
        tables = process_validation(result["files"])
        output = "\n\n".join(tables)
        outputs.append(output)
        print(f"Run {i+1} Output:\n{output[:500]}...\n")

    base = outputs[0]
    similarities = [semantic_similarity(base, other) for other in outputs[1:]]
    avg_score = sum(similarities) / len(similarities)
    print(f"ValidationAgent Semantic Consistency Score: {avg_score:.4f}")

if __name__ == "__main__":
    test_document_agent(
        file_path="broker-template/account_summary.txt", 
        fields_txt="broker-template/custom_fields.txt", 
        user_prompt="Dates should be in format dd-mm-yyyy not like Jan,Feb", 
        runs=10
    )

    #test_validation_agent(
    #    repo_url="https://github.com/tas-neem/sample", 
    #    runs=10
    #)

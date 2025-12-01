from datasets import load_dataset
import csv
from pathlib import Path

# Removes special characters in the diff to avoid string encording errors
def clean_patch(patch: str) -> str:
    if patch is None:
        return ""
    
    cleaned_chars = []
    
    for char in patch:
        code = ord(char)
        if char in ("\t", "\n", "\r") or 32 <= code <= 126:
            cleaned_chars.append(char)
        else:
            cleaned_chars.append(" ")
    return "".join(cleaned_chars)

def main():
    commit_details = load_dataset("hao-li/AIDev", "pr_commit_details", split="train")

    project_root = Path(__file__).resolve().parents[1]

    csv_dir = project_root / "csv"
    csv_dir.mkdir(exist_ok=True)

    output_path = csv_dir / "pr_commit_details.csv"

    fieldnames = [
        "PRID",
        "PRSHA",
        "PRCOMMITMESSAGE",
        "PRFILE",
        "PRSTATUS",
        "PRADDS",
        "PRDELSS",
        "PRCHANGECOUNT",
        "PRDIFF",
    ]

    with output_path.open("w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in commit_details:
            patch_raw = row.get("patch", "")
            patch_clean = clean_patch(patch_raw)

            writer.writerow({
                "PRID": row.get("pr_id", ""),
                "PRSHA": row.get("sha", ""),
                "PRCOMMITMESSAGE": row.get("message", ""),
                "PRFILE": row.get("filename", ""),
                "PRSTATUS": row.get("status", ""),
                "PRADDS": row.get("additions", ""),
                "PRDELSS": row.get("deletions", ""),
                "PRCHANGECOUNT": row.get("changes", ""),
                "PRDIFF": patch_clean,
            })

    print(f"PR Commit Details CSV file written to {output_path}")

if __name__ == "__main__":
    main()
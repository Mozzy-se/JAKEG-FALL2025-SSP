# This file creates the CSV file that contains the requested headers and data
from datasets import load_dataset
import csv
from pathlib import Path

def main ():
    pull_requests = load_dataset("hao-li/AIDev", "all_pull_request", split="train")

    project_root = Path(__file__).resolve().parents[1]

    csv_dir = project_root / "csv"
    csv_dir.mkdir(exist_ok=True)

    output_path = csv_dir / "pull_requests.csv"

    fieldnames = [
        "TITLE",
        "ID",
        "AGENTNAME",
        "BODYSTRING",
        "REPOID",
        "REPOURL",
    ]

    with output_path.open("w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in pull_requests:
            writer.writerow({
                "TITLE": row.get("title", ""),
                "ID": row.get("id", ""),
                "AGENTNAME": row.get("agent", ""),
                "BODYSTRING": row.get("body", ""),
                "REPOID": row.get("repo_id", ""),
                "REPOURL": row.get("repo_url", ""),
            })
    
    print(f"Task 1 CSV file written to {output_path}")

if __name__ == "__main__":
    main()
from datasets import load_dataset
import csv
from pathlib import Path

def main():
    task_types = load_dataset("hao-li/AIDev", "pr_task_type", split="train")

    project_root = Path(__file__).resolve().parents[1]

    csv_dir = project_root / "csv"
    csv_dir.mkdir(exist_ok=True)

    output_path = csv_dir / "pr_task_types.csv"

    fieldnames = [
        "PRID",
        "PRTITLE",
        "PRREASON",
        "PRTYPE",
        "CONFIDENCE",
    ]

    with output_path.open("w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in task_types:
            writer.writerow({
                "PRID": row.get("id", ""),
                "PRTITLE": row.get("title", ""),
                "PRREASON": row.get("reason", ""),
                "PRTYPE": row.get("type", ""),
                "CONFIDENCE": row.get("confidence", ""),
            })

    print(f"PR Task Types CSV file written to {output_path}")

if __name__ == "__main__":
    main()
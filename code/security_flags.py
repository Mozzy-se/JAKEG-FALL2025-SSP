
import csv
from pathlib import Path


# Security keyword list provided from references
KEYWORDS = [
    "race", "racy", "buffer", "overflow", "stack", "integer", "signedness",
    "underflow", "improper", "unauthenticated", "gain access", "permission",
    "cross site", "css", "xss", "denial service", "dos", "crash", "deadlock",
    "injection", "request forgery", "csrf", "xsrf", "forged", "security",
    "vulnerability", "vulnerable", "exploit", "attack", "bypass",
    "backdoor", "threat", "expose", "breach", "violate", "fatal",
    "blacklist", "overrun", "insecure"
]


def contains_security_keywords(text: str) -> bool:
    if not text:
        return False

    t = text.lower()
    return any(keyword in t for keyword in KEYWORDS)


def main():
    project_root = Path(__file__).resolve().parents[1]
    csv_dir = project_root / "csv"

    pr_csv = csv_dir / "pull_requests.csv"      
    task_csv = csv_dir / "pr_task_types.csv"  


    out_path = csv_dir / "security_flags.csv"

    pr_data = {}   
    with pr_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pr_id = row["ID"]
            pr_data[pr_id] = {
                "title": row.get("TITLE", ""),
                "body": row.get("BODYSTRING", ""),
                "agent": row.get("AGENTNAME", "")
            }

    task_data = {}
    with task_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task_data[row["PRID"]] = {
                "type": row.get("PRTYPE", ""),
                "confidence": row.get("CONFIDENCE", "")
            }

    fieldnames = ["ID", "AGENT", "TYPE", "CONFIDENCE", "SECURITY"]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for pr_id, info in pr_data.items():

            tt = task_data.get(pr_id, {})
            pr_type = tt.get("type", "")
            confidence = tt.get("confidence", "")

            text_to_scan = (info["title"] + " " + info["body"]).lower()
            security_flag = 1 if contains_security_keywords(text_to_scan) else 0

            writer.writerow({
                "ID": pr_id,
                "AGENT": info["agent"],
                "TYPE": pr_type,
                "CONFIDENCE": confidence,
                "SECURITY": security_flag
            })

    print(f"Task 5 CSV file written to {out_path}")


if __name__ == "__main__":
    main()

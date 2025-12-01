# This file is here to load the datasets needed for project.
from datasets import load_dataset

dataset = load_dataset("hao-li/AIDev")

pull_requests = dataset["all_pull_request"]
repositories = dataset["all_repository"]
task_types = dataset["pr_task_type"]
commit_details = dataset["pr_commit_details"]

print(pull_requests[0])
import re
from pydriller import Repository

repo_url = "https://github.com/apache/lucene"

issue_ids = ["LUCENE-12", "LUCENE-17", "LUCENE-701", "LUCENE-1200", "LUCENE-1799"]

total_commits = 0
total_files_changed = 0
unique_files = set()
dmm_size = []
dmm_complexity = []
dmm_interfacing = []

for commit in Repository(repo_url).traverse_commits():
    match = re.search(r"LUCENE-\d+", commit.msg, re.IGNORECASE)
    if not match or match.group(0).upper() not in issue_ids:
        continue
    total_commits += 1
    commit_unique = set()
    for f in commit.modified_files:
        if f.new_path:
            unique_files.add(f.new_path)
            commit_unique.add(f.new_path)
    total_files_changed += len(commit_unique)
    if commit.dmm_unit_size is not None:
        dmm_size.append(commit.dmm_unit_size)
    if commit.dmm_unit_complexity is not None:
        dmm_complexity.append(commit.dmm_unit_complexity)
    if commit.dmm_unit_interfacing is not None:
        dmm_interfacing.append(commit.dmm_unit_interfacing)

all_dmm = dmm_size + dmm_complexity + dmm_interfacing
print(f"Total commits analyzed:          {total_commits}")
print(f"Average number of files changed: {total_files_changed / total_commits:.2f}")
print(f"Avg DMM metrics:                 {sum(all_dmm) / len(all_dmm):.4f}")

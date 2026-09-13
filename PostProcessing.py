import csv

INPUT_FILE = "articles.csv"
OUTPUT_FILE = "articles_sorted.csv"

with open(INPUT_FILE, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

def citation_count(row):
    return int(row["num_references"])
    

rows.sort(key=citation_count, reverse=True)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} articles to {OUTPUT_FILE}, sorted by citation count (descending)")
from tqdm import tqdm

vcf_file = "path/to/your/merged.vcf"
skipped = 0
total = 0

with open(vcf_file) as vcf:
    for _ in range(6):  # Skip headers
        next(vcf)
    
    for line in tqdm(vcf):
        total += 1
        vals = line.split()[9:]
        pos_vals = [i for i, val in enumerate(vals) if val == "1/1"]
        if len(pos_vals) <= 1:
            skipped += 1

print(f"Total lines: {total}, Skipped: {skipped}, Used: {total - skipped}")
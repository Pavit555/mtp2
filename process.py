import pandas as pd

def convert_vcf(input_vcf, output_file):
    with open(input_vcf, 'r') as f:
        lines = f.readlines()

    # Parse header
    header_line = ""
    data_lines = []
    for line in lines:
        if line.startswith("#CHROM"):
            header_line = line.strip().lstrip('#').split('\t')
        elif not line.startswith("#"):
            data_lines.append(line.strip().split('\t'))

    # Create DataFrame
    df = pd.DataFrame(data_lines, columns=header_line)

    # Convert CHROM name
    df['#CHROM'] = df['#CHROM'].replace({'NC_000913.3': '26'})

    # Replace missing IDs
    df['ID'] = df.apply(lambda row: row['ID'] if row['ID'] != '.' else f"coor_{row['POS']}", axis=1)

    # Standardize INFO, FORMAT, QUAL, FILTER
    df['INFO'] = 'PR'
    df['FORMAT'] = 'GT'
    df['QUAL'] = '.'
    df['FILTER'] = '.'

    # Extract only GT from sample fields
    sample_cols = df.columns[9:]
    for col in sample_cols:
        df[col] = df[col].apply(lambda x: x.split(":")[0] if x != './.:' else './.')

    # Final column order
    final_cols = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + list(sample_cols)
    df = df[final_cols]

    # Save to file
    df.to_csv(output_file, sep='\t', index=False)

# === USAGE ===
convert_vcf("joint_variants.vcf", "model_input_ready.tsv")
import pandas as pd

def convert_vcf(input_vcf, output_file):
    with open(input_vcf, 'r') as f:
        lines = f.readlines()

    # Separate metadata header and data
    metadata_headers = []
    header_line = ""
    data_lines = []

    for line in lines:
        if line.startswith("##"):
            metadata_headers.append(line.strip())
        elif line.startswith("#CHROM"):
            header_line = line.strip().lstrip('#').split('\t')
        elif not line.startswith("#"):
            data_lines.append(line.strip().split('\t'))

    # Create DataFrame
    df = pd.DataFrame(data_lines, columns=header_line)

    # Replace missing IDs with coordinates
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
    df[sample_cols] = df[sample_cols].replace({'./.': '0/0'})

    # Final column order
    final_cols = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + list(sample_cols)
    df = df[final_cols]

    # Rename CHROM to #CHROM for compatibility
    df.rename(columns={'CHROM': '#CHROM'}, inplace=True)

    # Write to file
    with open(output_file, 'w') as out:
        for line in metadata_headers:
            out.write(line + '\n')
        out.write('#' + '\t'.join(df.columns) + '\n')
        df.to_csv(out, sep='\t', index=False, header=False)
convert_vcf("merged.vcf", "model_input_ready.tsv")
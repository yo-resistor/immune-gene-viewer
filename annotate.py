import pandas as pd

def annotate_variants(input_path, output_path):
    df = pd.read_csv(input_path)
    # Dummy annotation — add a "Risk" column based on dummy logic
    df["Risk"] = df["Allele"].apply(lambda x: "High" if "B" in x else "Low")
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    annotate_variants("data/test_alleles.csv", "data/annotated.csv")
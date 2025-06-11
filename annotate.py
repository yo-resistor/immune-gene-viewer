import pandas as pd

def annotate_variants(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # Apply dummy logic based on allele values
    def risk_logic(allele):
        if "B*08" in allele:
            return "Very High"
        elif "B" in allele:
            return "High"
        elif "A" in allele:
            return "Moderate"
        else:
            return "Low"
    
    df["Risk"] = df["Allele"].apply(risk_logic)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "data/test_alleles.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "data/annotated.csv"
    annotate_variants(input_path, output_path)
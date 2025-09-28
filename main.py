import argparse
from agent.orchestrator import agent_loop

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    bank = args.target
    pdf_path = f"data/{bank}/{bank}_sample.pdf"
    csv_path = f"data/{bank}/{bank}_sample.csv"

    result = agent_loop(bank, pdf_path, csv_path)
    if result['success']:
        print("Parser generation succeeded")
    else:
        print("Parser generation failed")
        if result['last_error']:
            print(result['last_error'])

import os
import sys
import importlib
import google.generativeai as genai
from dotenv import dotenv_values

config = dotenv_values(".env")
API_KEY = config.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

def codegen_node(bank, csv_path, state):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    
    CODE_PROMPT = """


You are an expert Python developer. Write me a complete Python script that parses an bank statement PDF into a pandas DataFrame using pdfplumber. The script must exactly follow these rules:

1. Define a function `parse(pdf_path: str) -> pd.DataFrame`.
   - Use `pdfplumber` and `page.extract_words()` to get words with their x/y positions.
   - Define a helper function `normalize_word(w)` inside `parse` that converts the word dictionary to always have:
       * 'y_top' (use 'top' if exists, otherwise fallback to 'y_top' or 0)
       * 'y_bottom' (use 'bottom' if exists, otherwise fallback to 'y_bottom' or 0)
       * 'x_left' (use 'x0' if exists, otherwise fallback to 'x_left')
       * 'x_right' (use 'x1' if exists, otherwise fallback to 'x_right')
       * 'x_center' as the center between x_left and x_right
   - Use this helper to normalize all words before further processing.
   - Group words into rows based on their vertical position (use y tolerance ~3-4 on 'y_top').
   - For each row:
     * Skip headers that start with "Date" and footers containing "ChatGPT Powered".
     * Find the date token (dd-mm-yyyy).
     * Identify numeric tokens.
     * The rightmost numeric token is the Balance.
     * The second-rightmost numeric token is the transaction Amount.
     * Compute the x-position of the Amount and use clustering (two centroids: left=Debit, right=Credit) to decide whether the Amount goes into "Debit Amt" or "Credit Amt".
     * If there are fewer than 2 numeric tokens for clustering, assume the amount is a Debit Amt and Credit Amt is NaN.
     * Extract the Description as the text between the Date and the Amount.
   - Build rows with: `Date`, `Description`, `Debit Amt`, `Credit Amt`, `Balance`.
   - Convert `Debit Amt`, `Credit Amt`, and `Balance` to floats (NaN if missing).
   - Keep the Date in (dd-mm-yyyy) format.
   - Return the DataFrame.

Do not explain the code, do not add comments, and do not output anything except the exact Python code.



"""  

    refinement_notes = ""
    if state.get("last_error"):
        refinement_notes += f"\nThe last attempt failed with this runtime error:\n{state['last_error']}\n"
    if state.get("diff_text"):
        refinement_notes += f"\nThe last attempt failed with these DataFrame differences:\n{state['diff_text']}\n"

    prompt = CODE_PROMPT + refinement_notes

    response = model.generate_content(prompt)
    code = response.text.strip()
    
    if code.startswith("```"):
        code = code.split('\n', 1)[1] if '\n' in code else ''
    if code.endswith("```"):
        code = code[:-3].strip()

    parser_path = f"custom_parsers/{bank}_parser.py"
    with open(parser_path, "w", encoding="utf-8") as f:
        f.write(code)

    state['last_error'] = None
    state['diff_text'] = None
    return state

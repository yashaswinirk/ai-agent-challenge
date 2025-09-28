from pdfminer.high_level import extract_text

def planner_node(bank, pdf_path, state):
    if state['attempt'] == 1:
        try:
            sample_text = extract_text(pdf_path)[:1000]
            state['planning_notes'] = f"The PDF text starts with this structure:\n{sample_text}"
        except Exception:
            state['planning_notes'] = "Could not read PDF sample text."
    else:
        state['planning_notes'] = "Planning skipped on retry. Using Refiner's instructions."
    return state

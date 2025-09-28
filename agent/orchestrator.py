import os
from .planner import planner_node
from .codegen import codegen_node
from .tester import test_node
from .refiner import refiner_node

def agent_loop(bank, pdf_path, csv_path, max_attempts=3):
    os.makedirs("custom_parsers", exist_ok=True)
    
    state = {
        "attempt": 1,
        "last_error": None,
        "diff_text": None,
        "success": None,
        "max_attempts": max_attempts,
        "planning_notes": "",
        "next_step": "plan"
    }
    
    while state["next_step"] != 'end':
        current_step = state["next_step"]

        if current_step == 'plan':
            state = planner_node(bank, pdf_path, state)
            state["next_step"] = "codegen"
        elif current_step == 'codegen':
            state = codegen_node(bank, csv_path, state)
            state["next_step"] = "test"
        elif current_step == 'test':
            state = test_node(bank, pdf_path, csv_path, state)
            state["next_step"] = "refiner"
        elif current_step == 'refiner':
            state = refiner_node(state)
        else:
            break

    return state

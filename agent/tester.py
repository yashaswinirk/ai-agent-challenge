import os
import sys
import importlib
from difflib import unified_diff
from .utils import read_csv

def test_node(bank, pdf_path, csv_path, state):
    df_generated, df_expected = None, None
    success = False
    last_error = None
    diff_text = None

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        custom_parsers_dir = os.path.join(current_dir, "../custom_parsers")
        if custom_parsers_dir not in sys.path:
            sys.path.append(custom_parsers_dir)

        parser_module_name = f"{bank}_parser"

        if parser_module_name in sys.modules:
            parser = importlib.reload(sys.modules[parser_module_name])
        else:
            parser = importlib.import_module(parser_module_name)

        df_generated = parser.parse(pdf_path)
        df_expected = read_csv(csv_path)

        success = df_generated.equals(df_expected)

        if success:
            out_csv = os.path.join(os.path.dirname(pdf_path), f"{bank}_parsed.csv")
            df_generated.to_csv(out_csv, index=False)

    except Exception as e:
        success = False
        last_error = str(e)

    if not success and df_generated is not None and df_expected is not None:
        df_gen_str = df_generated.to_string(index=False)
        df_exp_str = df_expected.to_string(index=False)
        diff_text = "\n".join(unified_diff(
            df_gen_str.splitlines(),
            df_exp_str.splitlines(),
            fromfile="generated",
            tofile="expected",
            lineterm=""
        ))

    state['success'] = success
    state['last_error'] = last_error
    state['diff_text'] = diff_text

    print("==================================================================================================")
    print(f"State: {state}")
    print("==================================================================================================")
    return state

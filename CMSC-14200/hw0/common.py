"""
Module providing utility functions for working with the
Gradescope autograder.

- gen_validator_output: Generates a validator's output
  (optionally generating a JSON file that can be consumed
  by Gradescope's autograder)
"""

import contextlib
import json
import io
from pathlib import Path
from typing import Collection

from validators import Validator


def gen_validator_output(
    validators: Collection[Validator], gradescope_f: Path | None
) -> None:
    validator_output = io.StringIO()

    passes_all_validators = all(v.valid for v in validators)
    with contextlib.redirect_stdout(validator_output):
        if passes_all_validators:
            if gradescope_f is None:
                print("Your repository appears to be correctly set up.")
                print("Don't forget to submit it on Gradescope!")
            else:
                print("The files you have submitted appear to be **correct**.")
                print()
                print(
                    "Don't forget to click on the 'Code' tab to double-check "
                    "that all your files are there. You should do this in all "
                    "your homework submissions!"
                )
        else:
            if gradescope_f is None:
                print("There are a few issues with your repository:\n")
            else:
                print("# ERROR")
                print("There are a few issues with your submitted files:\n")

            for v in validators:
                if v.valid is not None and not v.valid:
                    print("-", v.error_msg, "\n" if not gradescope_f else "")

            if gradescope_f is not None:
                print("\n**Please correct these issues and re-submit your code**")

    if gradescope_f is not None:
        gradescope_json: dict[str, str | float] = {}
        gradescope_json["stdout_visibility"] = "hidden"
        gradescope_json["output_format"] = "md"
        gradescope_json["score"] = 1.0 if passes_all_validators else 0.0
        gradescope_json["output"] = validator_output.getvalue()

        with open(gradescope_f, "w") as f:
            json.dump(gradescope_json, f, indent=2)
    else:
        print(validator_output.getvalue())

"""Script para inferência em lote."""

import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--input-path", required=True)
    args = parser.parse_args()

    subprocess.run(
        [
            "python",
            "src/main.py",
            "infer",
            "--model-path",
            args.model_path,
            "--input-path",
            args.input_path,
        ],
        check=False,
    )

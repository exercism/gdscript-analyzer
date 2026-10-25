#!/usr/bin/env python3
"""Generate a representation of a GDScript solution."""

import argparse
import dataclasses
import json
import pathlib
import yaml

import gdtoolkit.linter


def gdlintrc() -> dict:
    """Load the gdlint config."""
    path = pathlib.Path("gdlintrc")
    if path.exists():
        return yaml.load(pathlib.Path("gdlintrc").read_text(), Loader=yaml.Loader)
    return gdtoolkit.linter.DEFAULT_CONFIG


def load_config(input_path: pathlib.Path) -> dict | None:
    """Return the contents of .meta/config.json if it exists, or None."""
    config_path = input_path / ".meta/config.json"
    if not config_path.exists():
        return None
    return json.loads((input_path / ".meta/config.json").read_text())


def solution_files(slug: str, input_path: pathlib.Path) -> list[pathlib.Path]:
    """Return the solution files, based on the config.json if available, or the slug."""
    config = load_config(input_path)
    if config:
        files = config.get("files", {}).get("solution", [])
        if files:
            return [input_path / file for file in files]
    return [(input_path / slug.replace("-", "_")).with_suffix(".gd")]


def format_comments(path: pathlib.Path, problems: list[gdtoolkit.linter.problem.Problem]) -> list[dict[str, str]]:
    return [
        {"comment": "gdscript.gdlint.finding", "params": dataclasses.asdict(problem) | {"file": path.name}}
        for problem in problems
    ]


def write_output(output_path: pathlib.Path, comments: list[dict], tags: list[str]) -> None:
    """Write the representer files."""
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    (output_path / "tags.json").write_text(json.dumps({"tags": tags}, indent=2) + "\n")
    (output_path / "analysis.json").write_text(json.dumps({"comments": comments}, indent=2, sort_keys=True) + "\n")


def arg_parser() -> argparse.ArgumentParser:
    """Return an ArgumentParser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    return parser


def main() -> None:
    """Generate a representation."""
    args = arg_parser().parse_args()
    slug = args.slug
    input_path = pathlib.Path(args.input_dir)
    output_path = pathlib.Path(args.output_dir)

    print(f"== Analyzing {args.slug!r} ==")
    comments = []
    config = gdlintrc()
    for solution_file in solution_files(slug, input_path):
        comments.extend(format_comments(solution_file, gdtoolkit.linter.lint_code(solution_file.read_text())))

    tags = []

    write_output(output_path, comments, tags)
    print(f"== Done {args.slug!r} ==")


if __name__ == "__main__":
    main()

#!/usr/bin/env sh

# Synopsis:
# Run the analyzer on a solution.

# Arguments:
# $1: exercise slug
# $2: path to solution folder
# $3: path to output directory

# Output:
# Writes the analysis results to an analysis.json file in the passed-in output directory.
# The analysis results are formatted according to the specifications at https://github.com/exercism/docs/blob/main/building/tooling/analyzers/interface.md

# Example:
# ./bin/run.sh two-fer path/to/solution/folder/ path/to/output/directory/

python3 "${0%.*}.py" "$@"

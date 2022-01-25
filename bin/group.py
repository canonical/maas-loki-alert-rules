#!/usr/bin/env python3

# Copyright 2022 Canonical Ltd.  This software is licensed under the
# Apache License version 2 (see the file LICENSE).

import argparse
import sys
from glob import glob

import yaml


class Group:
    alerts = {"name": "alerts", "rules": []}

    def __init__(self, snippet_path, out_path):
        self.snippet_path = snippet_path
        self.out_path = out_path

    def load_snippets(self):
        for snippet in glob(self.snippet_path):
            with open(snippet) as f:
                snippet_content = yaml.load(f.read(), Loader=yaml.FullLoader)
                self.add_snippet(snippet_content)

    def add_snippet(self, snippet):
        if type(snippet) == list:
            self.alerts["rules"].extend(snippet)
        else:
            self.alerts["rules"].append(snippet)

    def data(self):
        return {"groups": [self.alerts]}

    def to_yaml(self):
        with open(self.out_path, 'w') as f:
            f.write(yaml.dump(self.data()))


class TestGroup(Group):
    tests = {"rule_files": [], "tests": []}

    def __init__(self, snippet_path, test_out_path, out_path):
        self.tests["rule_files"].append(out_path)
        super().__init__(snippet_path, test_out_path)

    def add_snippet(self, snippet):
        self.tests["tests"].extend(snippet)

    def data(self):
        return self.tests


def main():
    parser = argparse.ArgumentParser(description="Builds a groups file for direct loki use of rules")
    parser.add_argument("--rules", help="blob path for rules files to be loaded from")
    parser.add_argument("--tests", help="blob path for test files to be loaded from")
    parser.add_argument("--out", help="full path to output the file to")
    parser.add_argument("--test_out", help="full path to output the test file to")

    args = parser.parse_args(sys.argv[1:])
    
    group = Group(args.rules, args.out)
    group.load_snippets()
    group.to_yaml()

    if args.tests:
        test_group = TestGroup(args.tests, args.test_out, args.out)
        test_group.load_snippets()
        test_group.to_yaml()


if __name__ == "__main__":
    main()

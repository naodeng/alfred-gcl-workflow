#!/usr/bin/env python3
import json
import string
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "generate_content.py"
sys.path.insert(0, str(ROOT))

import generate_content  # noqa: E402


def run_query(query):
    output = subprocess.check_output(
        [sys.executable, str(SCRIPT), query],
        text=True,
    )
    data = json.loads(output)
    return data["items"][0]


def run_without_arg():
    output = subprocess.check_output(
        [sys.executable, str(SCRIPT)],
        text=True,
    )
    data = json.loads(output)
    return data["items"][0]


class ParseInputTests(unittest.TestCase):
    def test_parse_loop_mode(self):
        mode, length = generate_content.parse_input("10")
        self.assertEqual(mode, "loop_number")
        self.assertEqual(length, 10)

    def test_parse_letters_mode(self):
        mode, length = generate_content.parse_input("a 16")
        self.assertEqual(mode, "letters")
        self.assertEqual(length, 16)

    def test_parse_alnum_mode_case_insensitive(self):
        mode, length = generate_content.parse_input("AN 24")
        self.assertEqual(mode, "alnum")
        self.assertEqual(length, 24)

    def test_parse_all_chars_mode(self):
        mode, length = generate_content.parse_input("ans 32")
        self.assertEqual(mode, "all_chars")
        self.assertEqual(length, 32)

    def test_parse_invalid_input(self):
        mode, length = generate_content.parse_input("foo")
        self.assertIsNone(mode)
        self.assertIsNone(length)


class BuildResultTests(unittest.TestCase):
    def test_loop_number_pattern(self):
        result = generate_content.build_result("loop_number", 13)
        self.assertEqual(result, "1234567890123")

    def test_letters_charset(self):
        result = generate_content.build_result("letters", 200)
        self.assertEqual(len(result), 200)
        self.assertTrue(set(result) <= set(string.ascii_letters))

    def test_alnum_charset(self):
        allowed = set(string.digits + string.ascii_letters)
        result = generate_content.build_result("alnum", 200)
        self.assertEqual(len(result), 200)
        self.assertTrue(set(result) <= allowed)

    def test_all_chars_charset(self):
        allowed = set(string.digits + string.ascii_letters + "!@#$%^&*()-_=+[]{};:,.<>/?")
        result = generate_content.build_result("all_chars", 200)
        self.assertEqual(len(result), 200)
        self.assertTrue(set(result) <= allowed)


class EndToEndTests(unittest.TestCase):
    def test_empty_input_prompts_format(self):
        item = run_without_arg()
        self.assertFalse(item["valid"])
        self.assertIn("输入模式和长度", item["title"])

    def test_invalid_input(self):
        item = run_query("abc")
        self.assertFalse(item["valid"])
        self.assertIn("输入格式不正确", item["title"])

    def test_min_length_validation(self):
        item = run_query("0")
        self.assertFalse(item["valid"])
        self.assertIn("长度至少为 1", item["title"])

    def test_max_length_validation(self):
        item = run_query("ans 20001")
        self.assertFalse(item["valid"])
        self.assertIn("长度最多 20000", item["title"])

    def test_loop_output(self):
        item = run_query("10")
        self.assertTrue(item["valid"])
        self.assertEqual(item["title"], "1234567890")

    def test_letters_output(self):
        item = run_query("a 64")
        self.assertTrue(item["valid"])
        self.assertEqual(len(item["title"]), 64)
        self.assertTrue(set(item["title"]) <= set(string.ascii_letters))

    def test_alnum_output(self):
        item = run_query("an 64")
        allowed = set(string.digits + string.ascii_letters)
        self.assertTrue(item["valid"])
        self.assertEqual(len(item["title"]), 64)
        self.assertTrue(set(item["title"]) <= allowed)

    def test_all_chars_output(self):
        item = run_query("ans 64")
        allowed = set(string.digits + string.ascii_letters + "!@#$%^&*()-_=+[]{};:,.<>/?")
        self.assertTrue(item["valid"])
        self.assertEqual(len(item["title"]), 64)
        self.assertTrue(set(item["title"]) <= allowed)

    def test_length_20000_output(self):
        item = run_query("an 20000")
        self.assertTrue(item["valid"])
        self.assertEqual(len(item["title"]), 20000)


if __name__ == "__main__":
    unittest.main()

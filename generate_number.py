#!/usr/bin/env python3
"""
Alfred Script Filter: Generation for different character lengths (gcl).
Usage:
- gcl <length>         -> outputs 1234567890 in loop with specified length
- gcl a <length>       -> random letters
- gcl an <length>      -> random digits + letters
- gcl ans <length>     -> random digits + letters + symbols
"""
import json
import random
import string
import sys


def parse_input(query):
    tokens = query.split()
    if len(tokens) == 1 and tokens[0].isdigit():
        return "loop_number", int(tokens[0])

    if len(tokens) == 2 and tokens[1].isdigit():
        mode_token = tokens[0].lower()
        mode_map = {
            "a": "letters",
            "an": "alnum",
            "ans": "all_chars",
        }
        if mode_token in mode_map:
            return mode_map[mode_token], int(tokens[1])

    return None, None


def build_result(mode, length):
    if mode == "loop_number":
        base = "1234567890"
        repeat, remainder = divmod(length, len(base))
        return (base * repeat) + base[:remainder]

    if mode == "letters":
        pool = string.ascii_letters
    elif mode == "alnum":
        pool = string.digits + string.ascii_letters
    else:
        pool = string.digits + string.ascii_letters + "!@#$%^&*()-_=+[]{};:,.<>/?"
    return "".join(random.choice(pool) for _ in range(length))


def main():
    query = (sys.argv[1].strip() if len(sys.argv) > 1 else "").strip()
    if not query:
        print(json.dumps({
            "items": [{
                "title": "输入模式和长度",
                "subtitle": "例如: gcl 10 / gcl a 10 / gcl an 10 / gcl ans 10",
                "valid": False,
                "autocomplete": "gcl "
            }]
        }, ensure_ascii=False))
        return

    mode, length = parse_input(query)
    if mode is None:
        print(json.dumps({
            "items": [{
                "title": "输入格式不正确",
                "subtitle": "用法: gcl 10 / gcl a 10 / gcl an 10 / gcl ans 10",
                "valid": False
            }]
        }, ensure_ascii=False))
        return

    if length < 1:
        print(json.dumps({
            "items": [{
                "title": "长度至少为 1",
                "subtitle": "例如: gcl 10",
                "valid": False
            }]
        }, ensure_ascii=False))
        return
    if length > 20000:
        print(json.dumps({
            "items": [{
                "title": "长度最多 20000",
                "subtitle": "当前输入: " + query,
                "valid": False
            }]
        }, ensure_ascii=False))
        return

    result = build_result(mode, length)
    mode_text = {
        "loop_number": "循环数字",
        "letters": "字母随机",
        "alnum": "数字+字母随机",
        "all_chars": "数字+字母+符号随机",
    }[mode]

    print(json.dumps({
        "items": [{
            "title": result,
            "subtitle": f"{mode_text} · 长度 {length} · ⌘L 大号显示 · ⌘C 复制",
            "arg": result,
            "valid": True
        }]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

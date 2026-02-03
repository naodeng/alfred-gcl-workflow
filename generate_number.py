#!/usr/bin/env python3
"""
Alfred Script Filter: Generation for different character lengths (gcl).
Usage: gcl <length> → generates a random number with the specified digit length.
"""
import json
import random
import sys


def main():
    query = (sys.argv[1].strip() if len(sys.argv) > 1 else "").strip()
    if not query:
        print(json.dumps({
            "items": [{
                "title": "输入数字长度",
                "subtitle": "例如: gcl 10 → 生成 10 位数字",
                "valid": False,
                "autocomplete": "gcl "
            }]
        }, ensure_ascii=False))
        return

    if not query.isdigit():
        print(json.dumps({
            "items": [{
                "title": "请输入有效的数字",
                "subtitle": "长度应为正整数，例如: 10",
                "valid": False
            }]
        }, ensure_ascii=False))
        return

    length = int(query)
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

    min_val = 10 ** (length - 1)
    max_val = (10 ** length) - 1
    num = random.randint(min_val, max_val)
    result = str(num)

    print(json.dumps({
        "items": [{
            "title": result,
            "subtitle": f"{length} 位数字 · ⌘L 大号显示 · ⌘C 复制",
            "arg": result,
            "valid": True
        }]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

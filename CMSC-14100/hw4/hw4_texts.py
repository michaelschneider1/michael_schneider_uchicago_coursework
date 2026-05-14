"""
CMSC 14100
Winter 2025

Module to load texts.
"""
import sys

def load_text(filename):
    """
    Try to load text files.
    """
    try: 
        with open(filename) as f:
            return f.read().strip()
    except FileNotFoundError as e:
        print(f"Cannot open text file: {filename}", file=sys.stderr)
        sys.exit(1)
    
# Texts
CALCULUS = load_text("texts/33283-t.txt")
CHRISTMAS = load_text("texts/pg46.txt")
ENGINE = load_text("texts/pg71292.txt")
IBM = load_text("texts/pg27468.txt")
PROPOSAL = load_text("texts/pg1080.txt")
POOH = load_text("texts/pg67098.txt")
EASY = load_text("texts/dale-chall-word-list.txt").split()

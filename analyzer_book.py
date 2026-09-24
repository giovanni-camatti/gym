import argparse
import time
import string
from collections import Counter

def parse_arguments():
    # argparse automatically provides the --help/-h option
    parser = argparse.ArgumentParser(description="Analyze letter frequencies in a text file.")
    
    # Required positional argument
    parser.add_argument("filepath", type=str, help="Path to the input text file")
    
    # Optional arguments
    parser.add_argument("--histogram", action="store_true", help="Display an ASCII histogram of frequencies")
    parser.add_argument("--skip-preamble", action="store_true", help="Skip Project Gutenberg preamble and license")
    parser.add_argument("--stats", action="store_true", help="Print basic book statistics (chars, words, lines)")
    
    return parser.parse_args()

def main():
    start_time = time.time()
    args = parse_arguments()
    
    try:
        with open(args.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{args.filepath}' was not found.")
        return

    # [Optional Spec] Skip preamble and license
    if args.skip_preamble:
        start_idx = 0
        end_idx = len(lines)
        for i, line in enumerate(lines):
            if "*** START OF THE PROJECT GUTENBERG" in line:
                start_idx = i + 1
            elif "*** END OF THE PROJECT GUTENBERG" in line:
                end_idx = i
                break
        lines = lines[start_idx:end_idx]

    # [Optional Spec] Print basic book stats
    if args.stats:
        num_lines = len(lines)
        num_words = sum(len(line.split()) for line in lines)
        num_chars = sum(len(line) for line in lines)
        print("--- Book Statistics ---")
        print(f"Lines:      {num_lines:,}")
        print(f"Words:      {num_words:,}")
        print(f"Characters: {num_chars:,}")
        print("-" * 23 + "\n")

    # Count letters
    text = "".join(lines).lower()
    letter_counts = Counter(char for char in text if char in string.ascii_lowercase)
    total_letters = sum(letter_counts.values())

    # Calculate relative frequencies
    rel_freq = {char: (count / total_letters) for char, count in letter_counts.items()}
    
    # Print results
    print("--- Letter Frequencies ---")
    # Sort alphabetically
    for char in string.ascii_lowercase:
        freq = rel_freq.get(char, 0.0)
        
        # Display histogram if requested
        if args.histogram:
            # Scale bar length to a max of 50 characters
            max_freq = max(rel_freq.values()) if rel_freq else 1
            bar_length = int((freq / max_freq) * 50)
            bar = '█' * bar_length
            print(f"{char.upper()}: {freq:>6.2%} | {bar}")
        else:
            print(f"{char.upper()}: {freq:.2%}")

    # Total Elapsed Time
    elapsed_time = time.time() - start_time
    print(f"\nTotal elapsed time: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    main()
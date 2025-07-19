#!/usr/bin/env python3
"""
Standalone Summarization Script

Usage:
    python summarize.py transcript_file.txt [--type summary_type] [--output output_file.txt]
"""

import argparse
import sys
from pathlib import Path
from modules.summarizer import Summarizer


def extract_transcript_text(file_path: str) -> str:
    """Extract the main text from a transcript file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this is a formatted transcript file with sections
    start_marker = '=== FULL TEXT ==='
    end_marker = '=== SEGMENTS WITH TIMESTAMPS ==='
    
    if start_marker in content and end_marker in content:
        # Extract the full text section
        start_index = content.find(start_marker) + len(start_marker)
        end_index = content.find(end_marker)
        return content[start_index:end_index].strip()
    else:
        # Assume the entire file is the transcript
        return content.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Summarize transcript files using OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python summarize.py data/transcripts/my_transcript.txt
  python summarize.py transcript.txt --output summary.txt
  python summarize.py transcript.txt --model gpt-4
        """
    )
    
    parser.add_argument(
        "transcript_file",
        help="Path to transcript file to summarize"
    )
    
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path (if not specified, prints to console)"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-4-turbo",
        help="OpenAI model to use (default: gpt-4-turbo)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not Path(args.transcript_file).exists():
        print(f"Error: Transcript file not found: {args.transcript_file}")
        return 1
    
    try:
        print(f"📄 Reading transcript: {args.transcript_file}")
        text = extract_transcript_text(args.transcript_file)
        
        print(f"📝 Generating comprehensive summary...")
        print(f"🤖 Using model: {args.model}")
        
        # Initialize summarizer
        summarizer = Summarizer(model=args.model)
        
        if args.output:
            # Save to file
            output_file = summarizer.summarize_to_file(text, args.output)
            print(f"✅ Summary saved to: {output_file}")
        else:
            # Print to console
            summary = summarizer.summarize_text(text)
            print(f"\n=== COMPREHENSIVE SUMMARY ===")
            print(summary)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
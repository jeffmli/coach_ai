#!/usr/bin/env python3
"""
Simple AI Transcription and Summarization Pipeline

This script uses whisper command line for transcription and then summarizes the result.
"""

import argparse
import sys
import subprocess
from pathlib import Path
from pipeline.summarizer import Summarizer


def run_whisper_transcription(video_file: str, model: str = "small", output_dir: str = "transcripts/") -> str:
    """
    Run whisper command line transcription
    
    Args:
        video_file: Path to video file
        model: Whisper model size
        output_dir: Output directory for transcripts
        
    Returns:
        Path to generated transcript file
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Run whisper command
    cmd = [
        "whisper", 
        video_file, 
        "--model", model, 
        "--output_format", "txt", 
        "--output_dir", output_dir
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Whisper transcription failed: {result.stderr}")
    
    # Find the generated transcript file
    video_name = Path(video_file).stem
    transcript_file = Path(output_dir) / f"{video_name}.txt"
    
    if not transcript_file.exists():
        raise RuntimeError(f"Expected transcript file not found: {transcript_file}")
    
    return str(transcript_file)


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Simple AI Transcription and Summarization Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py coaching_session_#1.mov
  python main.py coaching_session_#1.mov --model small
  python main.py coaching_session_#1.mov --model small --output-dir transcripts/
        """
    )
    
    parser.add_argument(
        "video_file",
        help="Path to video file"
    )
    
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size for transcription (default: small)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="data/transcripts/",
        help="Output directory for transcripts (default: data/transcripts/)"
    )
    
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Also generate a summary after transcription"
    )
    
    args = parser.parse_args()
    
    # Validate video file exists
    if not Path(args.video_file).exists():
        print(f"Error: Video file not found: {args.video_file}")
        return 1
    
    try:
        print(f"📹 Processing video: {args.video_file}")
        print(f"🤖 Using Whisper model: {args.model}")
        print()
        
        # Run transcription
        transcript_file = run_whisper_transcription(
            args.video_file,
            args.model,
            args.output_dir
        )
        
        print(f"✅ Transcription complete: {transcript_file}")
        
        # Generate summary if requested
        if args.summarize:
            print("📝 Generating summary...")
            
            # Read transcript
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_text = f.read()
            
            # Generate summary
            summarizer = Summarizer()
            summary_file = Path(args.output_dir) / f"{Path(args.video_file).stem}_summary.txt"
            summarizer.summarize_to_file(transcript_text, str(summary_file))
            
            print(f"✅ Summary complete: {summary_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
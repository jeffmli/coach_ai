# AI Transcription and Summarization Commands

This document contains all the commands to use the AI transcription and summarization system.

## Setup Commands

### Initial Setup
```bash
# Activate virtual environment
cd "/Users/jeffreyli/Desktop/1. Projects/coach_ai"
source venv/bin/activate

# Create project directory structure
python main.py --setup

# Validate environment (check dependencies and API keys)
python main.py --validate-env
```

### Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

## Full Pipeline Commands

### Basic Video Processing (Transcription + Summarization)
```bash
# Basic usage - processes video file through complete pipeline
python main.py "data/input/your_video.mov"

# Use different Whisper models (for transcription speed/accuracy)
python main.py "data/input/your_video.mov" --whisper-model tiny     # Fastest
python main.py "data/input/your_video.mov" --whisper-model small    # Good balance
python main.py "data/input/your_video.mov" --whisper-model base     # Default
python main.py "data/input/your_video.mov" --whisper-model medium   # Better accuracy
python main.py "data/input/your_video.mov" --whisper-model large    # Best accuracy

# Specify language for transcription
python main.py "data/input/your_video.mov" --language en

# Custom output directory
python main.py "data/input/your_video.mov" --output-dir results/

# Keep temporary audio files (for debugging)
python main.py "data/input/your_video.mov" --keep-temp

# Combine multiple options
python main.py "data/input/your_video.mov" --whisper-model small --language en
```

## Summarization Only Commands

### Using the Standalone Summarizer
```bash
# Basic summarization (prints to console)
python summarize.py data/transcripts/your_transcript.txt

# Save summary to file
python summarize.py data/transcripts/your_transcript.txt --output my_summary.txt

# Specify different OpenAI model
python summarize.py data/transcripts/your_transcript.txt --model gpt-4

# Combine options
python summarize.py data/transcripts/your_transcript.txt --output summary.txt --model gpt-4

# Get help
python summarize.py --help
```

### Example with Actual Files
```bash
# Summarize the coaching session transcript
python summarize.py data/transcripts/coaching_session_#1_transcript_20250719_102310.txt

# Save to file
python summarize.py data/transcripts/coaching_session_#1_transcript_20250719_102310.txt --output coaching_summary.txt

# Use GPT-4 model
python summarize.py data/transcripts/coaching_session_#1_transcript_20250719_102310.txt --model gpt-4
```

## Summary Format

The summarizer generates a comprehensive summary with four structured sections:

| Section | Description |
|---------|-------------|
| **Key Points** | Main topics, themes, and important information discussed |
| **Key Learnings** | Main lessons, insights, or knowledge gained from the conversation |
| **Key Questions for Reflection** | Thoughtful questions to encourage deeper thinking and personal application |
| **Action Items** | Specific, actionable steps or tasks mentioned or implied |

## Whisper Model Comparison

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `tiny` | Fastest | Basic | Quick drafts, testing |
| `small` | Fast | Good | Balanced speed/quality |
| `base` | Medium | Good | Default choice |
| `medium` | Slow | Better | Higher accuracy needed |
| `large` | Slowest | Best | Maximum accuracy |

## File Structure

The system organizes files as follows:

```
coach_ai/
├── data/
│   ├── input/           # Place your .mov/.mp4 files here
│   ├── transcripts/     # Generated transcripts (.txt)
│   ├── summaries/       # Generated summaries (.txt)
│   ├── temp/           # Temporary audio files
│   └── metadata/       # Processing metadata (.json)
├── main.py             # Full pipeline command
├── summarize.py        # Summarization-only command
└── requirements.txt    # Dependencies
```

## Output Files

### Transcript Files
- **Location**: `data/transcripts/`
- **Format**: `{filename}_transcript_{timestamp}.txt`
- **Contains**: Full transcription with timestamps and metadata

### Summary Files  
- **Location**: `data/summaries/`
- **Format**: `{filename}_summary_{timestamp}.txt`
- **Contains**: Comprehensive summary with Key Points, Key Learnings, Reflection Questions, and Action Items

### Metadata Files
- **Location**: `data/metadata/` 
- **Format**: `{filename}_metadata.json`
- **Contains**: Processing information, models used, duration, etc.

## Troubleshooting

### Environment Issues
```bash
# Check if everything is configured
python main.py --validate-env

# Common issues and solutions:
# - Missing OPENAI_API_KEY: Set your API key
# - Missing ffmpeg: brew install ffmpeg
# - Package issues: pip install -r requirements.txt
```

### Performance Tips
- Use `tiny` or `small` Whisper models for faster processing
- For very long videos (>2 hours), consider using `medium` model with patience
- GPU acceleration will significantly speed up Whisper (if available)
- Comprehensive summaries provide structured insights across all four key areas

### File Compatibility
- **Supported formats**: MP4, MOV
- **Audio extraction**: Automatic via ffmpeg
- **Large files**: No size limit, but processing time scales with duration

## Examples

### Complete Workflow Example
```bash
# 1. Setup (first time only)
python main.py --setup
python main.py --validate-env

# 2. Process a coaching session
python main.py "data/input/coaching_session_#2.mov"

# 3. Generate additional summaries from existing transcript
python summarize.py "data/transcripts/coaching_session_#1_transcript_20250719_102310.txt" --output coaching_session_1_summary.txt

# 4. Review outputs
ls data/transcripts/
ls data/summaries/
```

### Batch Processing Multiple Videos
```bash
# Process multiple videos (manual approach)
for video in data/input/*.mov; do
    echo "Processing $video..."
    python main.py "$video"
done
```

---

**Note**: Always ensure you're in the project directory and have activated the virtual environment before running commands.
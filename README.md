# AI Coach Transcription and Summarization Pipeline

A simple yet powerful pipeline for transcribing video/audio files and generating comprehensive summaries using OpenAI's Whisper and GPT models.

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- FFmpeg (for Whisper audio processing)

### Installation

1. **Clone and navigate to the project**
   ```bash
   cd coach_ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Install FFmpeg** (if not already installed)
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt update && sudo apt install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### 🎥 Transcription Only

Convert video/audio files to text using OpenAI's Whisper:

```bash
# Basic transcription
python main.py your_video.mp4

# Use different Whisper model (tiny, base, small, medium, large)
python main.py your_video.mp4 --model medium

# Custom output directory
python main.py your_video.mp4 --output-dir my_transcripts/
```

**Output**: Creates a text file in `transcripts/` (or your specified directory) with the full transcript.

### 📝 Summarization Only

Generate summaries from existing transcript files:

```bash
# Summarize a transcript file
python summarize.py transcripts/your_transcript.txt

# Save summary to file
python summarize.py transcripts/your_transcript.txt --output summary.txt

# Use different GPT model
python summarize.py transcripts/your_transcript.txt --model gpt-4
```

**Output**: Creates a comprehensive summary with:
- 🧠 Key Points
- 💡 Key Learnings
- 🤔 Key Questions for Reflection
- ✅ Action Items

### 🚀 Full Pipeline (Transcription + Summarization)

Run the complete pipeline in one command:

```bash
# Transcribe AND summarize
python main.py your_video.mp4 --summarize

# Full pipeline with custom settings
python main.py coaching_session.mov --model medium --output-dir sessions/ --summarize
```

**Output**: Creates both transcript and summary files in your specified directory.

## Examples

### Basic Usage
```bash
# Transcribe a coaching session
python main.py coaching_session_1.mov

# Transcribe and summarize in one go
python main.py coaching_session_1.mov --summarize
```

### Advanced Usage
```bash
# High-quality transcription with summary
python main.py interview.mp4 --model large --summarize --output-dir interviews/

# Summarize an existing transcript with GPT-4
python summarize.py transcripts/meeting.txt --model gpt-4 --output meeting_summary.txt
```

## File Structure

```
coach_ai/
├── main.py              # Main pipeline script
├── summarize.py         # Standalone summarization
├── pipeline/            # Core modules
│   ├── __init__.py
│   └── summarizer.py    # Summarization logic
├── transcripts/         # Default output directory
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## Supported File Formats

Whisper supports most audio/video formats:
- **Video**: MP4, MOV, AVI, MKV, WebM
- **Audio**: MP3, WAV, FLAC, M4A, OGG

## Configuration

### Whisper Models
- **tiny**: Fastest, least accurate (~39 MB)
- **base**: Good balance (~74 MB)
- **small**: Better accuracy (~244 MB) - *Default*
- **medium**: High accuracy (~769 MB)
- **large**: Best accuracy (~1550 MB)

### GPT Models
- **gpt-4-turbo**: Best quality - *Default*
- **gpt-4**: High quality
- **gpt-3.5-turbo**: Faster, lower cost

## Tips

1. **For long videos**: Use `small` or `base` Whisper models for faster processing
2. **For important content**: Use `medium` or `large` Whisper models for better accuracy
3. **Cost optimization**: Use `gpt-3.5-turbo` for summarization if budget is a concern
4. **Batch processing**: You can run multiple files by creating a simple bash loop

## Troubleshooting

### Common Issues

**"No module named 'openai'"**
```bash
pip install -r requirements.txt
```

**"Whisper command not found"**
- Ensure openai-whisper is installed: `pip install openai-whisper`
- Check if whisper is in your PATH

**"OpenAI API key error"**
- Verify your `.env` file contains the correct API key
- Ensure the key has sufficient credits

**"FFmpeg not found"**
- Install FFmpeg following the setup instructions above

### Getting Help

For issues or questions:
1. Check that all dependencies are installed
2. Verify your OpenAI API key is valid
3. Ensure input files are in supported formats
4. Check the console output for specific error messages
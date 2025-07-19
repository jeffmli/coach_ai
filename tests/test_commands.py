#!/usr/bin/env python3
"""
Simple tests for main.py and summarize.py commands
"""

import pytest
import os
import tempfile
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.summarizer import Summarizer


class TestTranscription:
    """Test transcription functionality"""
    
    @pytest.fixture
    def dummy_video_file(self):
        """Create a temporary dummy video file for testing"""
        with tempfile.NamedTemporaryFile(suffix='.mov', delete=False) as f:
            f.write(b'dummy video content')
            yield f.name
        os.unlink(f.name)
    
    @patch('main.subprocess.run')
    def test_transcription_success(self, mock_subprocess, dummy_video_file, tmp_path):
        """Test that transcription works successfully"""
        # Mock successful whisper subprocess call
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stderr = ""
        
        # Create expected transcript file
        video_name = Path(dummy_video_file).stem
        expected_transcript_file = tmp_path / f"{video_name}.txt"
        expected_transcript_file.write_text("Test transcript content")
        
        from main import run_whisper_transcription
        
        with patch('pathlib.Path.exists', return_value=True):
            result = run_whisper_transcription(dummy_video_file, model="tiny", 
                                             output_dir=str(tmp_path))
            assert str(expected_transcript_file) in result


class TestSummarization:
    """Test summarization functionality"""
    
    @pytest.fixture
    def test_transcript(self, tmp_path):
        """Create a test transcript file"""
        content = """This is a coaching session transcript.
        
Coach: Welcome to our session today. What would you like to work on?
Client: I'm struggling with work-life balance and feeling overwhelmed.
Coach: Can you tell me more about what makes you feel overwhelmed?
Client: I have too many projects and not enough time to complete them all.
"""
        transcript_file = tmp_path / "test_transcript.txt"
        transcript_file.write_text(content)
        return str(transcript_file)
    
    @patch('pipeline.summarizer.OpenAI')
    def test_summarization_success(self, mock_openai, test_transcript):
        """Test that summarization works successfully"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """🧠 Key Points
This is a test summary.

💡 Key Learnings
Test learning point.

✅ Action Items
Complete the test."""
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            summarizer = Summarizer()
            
            with open(test_transcript, 'r') as f:
                transcript_text = f.read()
            
            result = summarizer.summarize_text(transcript_text)
            
            assert "Key Points" in result
            assert "Key Learnings" in result
            assert "Action Items" in result


class TestFullPipeline:
    """Test the full pipeline integration"""
    
    def test_main_help_command(self):
        """Test that main.py --help works"""
        result = subprocess.run([sys.executable, 'main.py', '--help'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        assert result.returncode == 0
        assert 'Simple AI Transcription and Summarization Pipeline' in result.stdout
    
    def test_summarize_help_command(self):
        """Test that summarize.py --help works"""
        result = subprocess.run([sys.executable, 'summarize.py', '--help'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        assert result.returncode == 0
        assert 'Summarize transcript files using OpenAI' in result.stdout
    
    def test_missing_files_handled(self):
        """Test that missing files are handled gracefully"""
        # Test main.py with non-existent video file
        result = subprocess.run([sys.executable, 'main.py', 'nonexistent.mov'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        assert result.returncode == 1
        assert 'Error: Video file not found' in result.stdout
        
        # Test summarize.py with non-existent transcript file
        result = subprocess.run([sys.executable, 'summarize.py', 'nonexistent.txt'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        assert result.returncode == 1
        assert 'Error: Transcript file not found' in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
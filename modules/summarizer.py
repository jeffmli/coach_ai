from openai import OpenAI
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Summarizer:
    """Handles text summarization using OpenAI's API"""
    
    # Comprehensive summary prompt template
    SUMMARIZATION_PROMPT = """Analyze the following transcript and generate a well-written, narrative-style summary that captures the essence of the conversation. Structure the output into clearly labeled sections to make it easy to digest and reflect on. Specifically, include the following:

🧠 Key Points
Provide a narrative overview of the main topics and themes discussed. Focus on the core ideas, significant insights, and recurring concepts that shaped the conversation. Present this in a flowing, readable paragraph or bulleted narrative form.

💡 Key Learnings
Summarize the most important takeaways and lessons from the conversation. Highlight meaningful realizations, strategies, or principles that emerged. This section should feel like the distilled wisdom someone would walk away with after reading the transcript.

🤔 Key Questions for Reflection
Offer a set of thoughtful, reflective questions that encourage deeper thinking about the themes discussed. These questions should help the reader consider how the insights might apply to their own life, work, or mindset.

✅ Action Items
List any specific actions, next steps, or commitments mentioned in the transcript. These should be clear, actionable tasks—whether explicitly stated or reasonably implied—that a person could implement based on the conversation.

Transcript:
{text}"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo"):
        """
        Initialize Summarizer with OpenAI API key and model
        
        Args:
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY env var)
            model: OpenAI model to use for summarization
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens_per_request = 4000  # Conservative limit for input text
        
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text (rough approximation)
        
        Args:
            text: Input text
            
        Returns:
            int: Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4
    
    def chunk_text(self, text: str, max_tokens: int = None) -> List[str]:
        """
        Split text into chunks that fit within token limits
        
        Args:
            text: Text to chunk
            max_tokens: Maximum tokens per chunk
            
        Returns:
            List[str]: List of text chunks
        """
        if max_tokens is None:
            max_tokens = self.max_tokens_per_request
        
        # If text is small enough, return as single chunk
        if self.count_tokens(text) <= max_tokens:
            return [text]
        
        # Split by paragraphs first, then by sentences if needed
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # Check if adding this paragraph exceeds limit
            test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            
            if self.count_tokens(test_chunk) <= max_tokens:
                current_chunk = test_chunk
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph
                
                # If single paragraph is too long, split by sentences
                if self.count_tokens(current_chunk) > max_tokens:
                    sentence_chunks = self._split_by_sentences(current_chunk, max_tokens)
                    chunks.extend(sentence_chunks[:-1])
                    current_chunk = sentence_chunks[-1] if sentence_chunks else ""
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_by_sentences(self, text: str, max_tokens: int) -> List[str]:
        """Split text by sentences when paragraphs are too long"""
        import re
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            test_chunk = current_chunk + ". " + sentence if current_chunk else sentence
            
            if self.count_tokens(test_chunk) <= max_tokens:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def summarize_text(self, text: str) -> str:
        """
        Summarize text using OpenAI API with comprehensive format
        
        Args:
            text: Text to summarize
            
        Returns:
            str: Generated comprehensive summary
            
        Raises:
            RuntimeError: If API call fails
        """
        # Check if text needs chunking
        chunks = self.chunk_text(text)
        
        if len(chunks) == 1:
            return self._summarize_single_chunk(chunks[0])
        else:
            return self._summarize_multiple_chunks(chunks)
    
    def _summarize_single_chunk(self, text: str) -> str:
        """Summarize a single chunk of text"""
        prompt = self.SUMMARIZATION_PROMPT.format(text=text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def _summarize_multiple_chunks(self, chunks: List[str]) -> str:
        """Summarize multiple chunks and combine results"""
        chunk_summaries = []
        
        # Summarize each chunk
        for i, chunk in enumerate(chunks):
            try:
                summary = self._summarize_single_chunk(chunk)
                chunk_summaries.append(f"Part {i+1}:\n{summary}")
            except Exception as e:
                chunk_summaries.append(f"Part {i+1}: [Error summarizing this section: {str(e)}]")
        
        # Combine chunk summaries
        combined_text = "\n\n".join(chunk_summaries)
        
        # Create final summary with our comprehensive format
        final_prompt = f"""Combine and consolidate the following section summaries into a single comprehensive summary with the format:

## Key Points
## Key Learnings  
## Key Questions for Reflection
## Action Items

Section Summaries to Combine:
{combined_text}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, concise summaries."},
                    {"role": "user", "content": final_prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # If final combination fails, return the chunk summaries
            return combined_text
    
    
    def summarize_to_file(self, text: str, output_path: str) -> str:
        """
        Summarize text and save to file
        
        Args:
            text: Text to summarize
            output_path: Path for output file
            
        Returns:
            str: Path to saved summary file
        """
        summary = self.summarize_text(text)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create formatted output
        content = []
        content.append("=== COMPREHENSIVE SUMMARY ===")
        content.append("")
        content.append(summary)
        content.append("")
        content.append("=== METADATA ===")
        content.append(f"Model Used: {self.model}")
        content.append(f"Original Text Length: {len(text)} characters")
        content.append(f"Summary Length: {len(summary)} characters")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return str(output_path)
    

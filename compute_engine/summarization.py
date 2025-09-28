import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from typing import List, Optional

# Initialize model and tokenizer with 8-bit quantization
model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(
    model_name,
    device_map="auto",
    load_in_8bit=True
)

def chunk_text(text: str, max_chunk_size: int = 512) -> List[str]:
    """Split text into chunks that fit within model's max token limit."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        word_tokens = len(tokenizer.encode(word))
        if current_size + word_tokens > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = word_tokens
        else:
            current_chunk.append(word)
            current_size += word_tokens
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def generate_summary(text: str, summary_type: str = "short") -> Optional[str]:
    """Generate summary using Pegasus model."""
    try:
        # Set parameters based on summary type
        max_length = 130 if summary_type == "short" else 250
        min_length = 30 if summary_type == "short" else 150
        num_beams = 4
        
        # Split text into chunks
        chunks = chunk_text(text)
        summaries = []
        
        # Process each chunk
        for chunk in chunks:
            inputs = tokenizer(chunk, max_length=1024, truncation=True, return_tensors="pt")
            inputs = inputs.to(model.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    length_penalty=2.0,
                    early_stopping=True
                )
            
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)
        
        # Combine chunk summaries
        final_summary = " ".join(summaries)
        
        # Format based on summary type
        if summary_type == "short":
            points = final_summary.split(". ")
            final_summary = "\n• " + "\n• ".join(point.strip() for point in points if point)
        
        return final_summary
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None
from openai import OpenAI
import tiktoken

# Token cost estimates per 1K tokens (based on OpenAI pricing as of 2023)
MODEL_COSTS = {
    "gpt-3.5-turbo": {
        "input": 0.0015,  # $0.0015 per 1K input tokens
        "output": 0.002   # $0.002 per 1K output tokens
    },
    "gpt-4": {
        "input": 0.03,    # $0.03 per 1K input tokens
        "output": 0.06    # $0.06 per 1K output tokens
    }
}

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback method (approximate)
        return len(text) // 4  # Rough approximation

def estimate_cost(num_tokens, model="gpt-3.5-turbo", input_output_ratio=0.75):
    """Estimate the cost of a request based on token count and model."""
    if model not in MODEL_COSTS:
        model = "gpt-3.5-turbo"  # Default fallback
    
    # Approximate split between input and output tokens
    input_tokens = int(num_tokens * input_output_ratio)
    output_tokens = num_tokens - input_tokens
    
    # Calculate cost
    input_cost = (input_tokens / 1000) * MODEL_COSTS[model]["input"]
    output_cost = (output_tokens / 1000) * MODEL_COSTS[model]["output"]
    
    return input_cost + output_cost

def summarize_text(text, length="short", api_key=None, model="gpt-3.5-turbo", return_tokens=False):
    """Summarize text using the specified OpenAI model."""
    if not api_key:
        raise ValueError("API key is required.")

    prompt_map = {
        "short": "Summarize this text in 1-2 sentences:",
        "medium": "Summarize this text in a short paragraph:",
        "long": "Summarize this text in detail:",
    }

    prompt = f"{prompt_map.get(length, 'Summarize this text:')}\n{text.strip()}"

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )

    summary = response.choices[0].message.content.strip()
    usage = response.usage
    
    # Count tokens in the response if requested
    if return_tokens:
        # Since the API response gives us the tokens used, use that
        output_tokens = response.usage.completion_tokens
        return summary, output_tokens
    
    return summary, usage

def summarize_file(file_text, filename, length="medium", api_key=None, model="gpt-3.5-turbo", return_tokens=False):
    """Summarize the content of a file with context about the file."""
    if not api_key:
        raise ValueError("API key is required.")
    
    if not file_text or not file_text.strip():
        raise ValueError("File text is empty or could not be processed.")
    
    # Create a prompt that includes file context
    file_prompt = f"""
    This is a summary request for a file named '{filename}'.
    Please provide a {length} summary of the following document content:
    
    {file_text[:9000]}  # Limit text size to avoid token limits
    """
    
    client = OpenAI(api_key=api_key)
    
    # Choose the appropriate model
    # For file summarization, use the 16k token model if using gpt-3.5
    model_to_use = "gpt-3.5-turbo-16k" if model == "gpt-3.5-turbo" else model
    
    response = client.chat.completions.create(
        model=model_to_use,
        messages=[{"role": "user", "content": file_prompt}],
        temperature=0.5,
        max_tokens=800,
    )
    
    summary = response.choices[0].message.content.strip()
    
    # Count tokens in the response if requested
    if return_tokens:
        # Since the API response gives us the tokens used, use that
        output_tokens = response.usage.completion_tokens
        return summary, output_tokens
    
    return summary
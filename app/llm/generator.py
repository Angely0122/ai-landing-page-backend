import os
import json
from openai import AzureOpenAI
from .prompts import build_landing_page_prompt, build_section_regenerate_prompt

# Initialize Azure OpenAI client
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")

if not AZURE_ENDPOINT or not AZURE_API_KEY:
    raise ValueError("AZURE_ENDPOINT or AZURE_API_KEY not found in environment variables")

client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version="2024-10-21",
    azure_endpoint=AZURE_ENDPOINT
)

def generate_page_spec(user_input: dict, crawled_data: list = None) -> dict:
    """
    Generate a complete landing page spec using Azure OpenAI
    
    Args:
        user_input: dict with industry, offer, target_audience, brand_tone
        crawled_data: optional list of crawled website data
    
    Returns:
        dict: page specification JSON
    """
    try:
        prompt = build_landing_page_prompt(user_input, crawled_data)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON generation expert. Return ONLY valid JSON, no markdown code blocks, no extra text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        # Extract response text
        response_text = response.choices[0].message.content
        
        # Parse JSON
        page_spec = json.loads(response_text)
        return page_spec
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")
    except Exception as e:
        raise Exception(f"Error generating page spec: {str(e)}")


def regenerate_section(section: dict, user_input: dict) -> dict:
    """
    Regenerate a single section with new prompt
    
    Args:
        section: the section object to regenerate
        user_input: context about the page (industry, offer, etc)
    
    Returns:
        dict: updated section
    """
    try:
        prompt = build_section_regenerate_prompt(section, user_input)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON generation expert. Return ONLY valid JSON, no markdown code blocks, no extra text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract response text
        response_text = response.choices[0].message.content
        
        # Parse JSON
        updated_section = json.loads(response_text)
        return updated_section
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")
    except Exception as e:
        raise Exception(f"Error regenerating section: {str(e)}")
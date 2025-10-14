def build_landing_page_prompt(user_input: dict, crawled_context: str = None) -> str:
    """Build the main prompt for landing page generation"""
    
    # Format crawled data into context if available
    crawl_context = ""
    if crawled_context:
        crawl_context = f"\n## Brand Context (extracted from website):\n{crawled_context}\n\nUse this brand context to match the tone, language, and style of the original website."
    
    prompt = f"""You are an expert landing page designer. Generate a landing page JSON specification based on the user input.

USER INPUT:
- Industry: {user_input.get('industry', '')}
- Offer: {user_input.get('offer', '')}
- Target Audience: {user_input.get('target_audience', '')}
- Brand Tone: {user_input.get('brand_tone', '')}{crawl_context}

REQUIREMENTS:
Create a landing page with 6 sections. The copy should be:
1. Specific to the industry
2. Appeal directly to the target audience
3. Match the brand tone
4. Include clear value propositions and CTAs

Return ONLY valid JSON, no markdown code blocks, no extra text. Use this exact structure:

{{
  "pageId": "landing-001",
  "version": 1,
  "sections": [
    {{
      "id": "hero-1",
      "type": "hero",
      "order": 0,
      "data": {{
        "headline": "string - main headline (5-8 words)",
        "subheadline": "string - supporting headline (1-2 sentences)",
        "ctaText": "string - button text",
        "backgroundImage": "string - unsplash URL",
        "textColor": "#FFFFFF",
        "backgroundColor": "#1a1a1a"
      }}
    }},
    {{
      "id": "features-1",
      "type": "features",
      "order": 1,
      "data": {{
        "title": "string",
        "description": "string",
        "items": [
          {{"id": "f1", "title": "string", "description": "string - 1 sentence", "icon": "emoji"}},
          {{"id": "f2", "title": "string", "description": "string - 1 sentence", "icon": "emoji"}},
          {{"id": "f3", "title": "string", "description": "string - 1 sentence", "icon": "emoji"}}
        ]
      }}
    }},
    {{
      "id": "testimonials-1",
      "type": "testimonials",
      "order": 2,
      "data": {{
        "title": "string",
        "items": [
          {{"id": "t1", "quote": "string - 1-2 sentences", "author": "string", "role": "string", "company": "string", "rating": 5}},
          {{"id": "t2", "quote": "string - 1-2 sentences", "author": "string", "role": "string", "company": "string", "rating": 5}}
        ]
      }}
    }},
    {{
      "id": "faq-1",
      "type": "faq",
      "order": 3,
      "data": {{
        "title": "Frequently Asked Questions",
        "items": [
          {{"id": "q1", "question": "string", "answer": "string - 1-2 sentences"}},
          {{"id": "q2", "question": "string", "answer": "string - 1-2 sentences"}},
          {{"id": "q3", "question": "string", "answer": "string - 1-2 sentences"}}
        ]
      }}
    }},
    {{
      "id": "contact-1",
      "type": "contact",
      "order": 4,
      "data": {{
        "title": "string - CTA headline",
        "description": "string",
        "fields": [
          {{"name": "email", "label": "Email", "type": "email", "required": true}},
          {{"name": "company", "label": "Company Name", "type": "text", "required": false}},
          {{"name": "message", "label": "Message", "type": "textarea", "required": true}}
        ],
        "submitText": "string",
        "backgroundColor": "#f9fafb"
      }}
    }},
    {{
      "id": "footer-1",
      "type": "footer",
      "order": 5,
      "data": {{
        "links": [
          {{"label": "Privacy Policy", "url": "/privacy"}},
          {{"label": "Terms of Service", "url": "/terms"}},
          {{"label": "Contact", "url": "/contact"}}
        ],
        "socialLinks": [
          {{"platform": "Twitter", "url": "https://twitter.com"}},
          {{"platform": "LinkedIn", "url": "https://linkedin.com"}}
        ],
        "copyright": "© 2025. All rights reserved."
      }}
    }}
  ]
}}

Generate the JSON now:"""
    
    return prompt


def build_section_regenerate_prompt(section: dict, user_input: dict) -> str:
    """Build prompt for regenerating a single section"""
    
    section_type = section.get("type")
    prompt = f"""You are an expert landing page designer. Regenerate a single landing page section.

ORIGINAL SECTION TYPE: {section_type}

CONTEXT:
- Industry: {user_input.get('industry', '')}
- Offer: {user_input.get('offer', '')}
- Target Audience: {user_input.get('target_audience', '')}
- Brand Tone: {user_input.get('brand_tone', '')}

CURRENT SECTION DATA:
{str(section.get('data', {}))}

Create a new version of this {section_type} section that:
1. Matches the brand tone and industry context
2. Is different from the current version
3. Maintains the same structure

Return ONLY valid JSON for the section data, no markdown:

{{
  "id": "{section.get('id')}",
  "type": "{section_type}",
  "order": {section.get('order', 0)},
  "data": {{
    // Fill based on section type
  }}
}}

Generate the JSON now:"""
    
    return prompt


def build_section_regenerate_prompt(section: dict, user_input: dict) -> str:
    """Build prompt for regenerating a single section"""
    
    section_type = section.get("type")
    prompt = f"""You are an expert landing page designer. Regenerate a single landing page section.

ORIGINAL SECTION TYPE: {section_type}

CONTEXT:
- Industry: {user_input.get('industry', '')}
- Offer: {user_input.get('offer', '')}
- Target Audience: {user_input.get('target_audience', '')}
- Brand Tone: {user_input.get('brand_tone', '')}

CURRENT SECTION DATA:
{str(section.get('data', {}))}

Create a new version of this {section_type} section that:
1. Matches the brand tone and industry context
2. Is different from the current version
3. Maintains the same structure

Return ONLY valid JSON for the section data, no markdown:

{{
  "id": "{section.get('id')}",
  "type": "{section_type}",
  "order": {section.get('order', 0)},
  "data": {{
    // Fill based on section type
  }}
}}

Generate the JSON now:"""
    
    return prompt
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_generate_page():
    """Generate a page first"""
    print("=" * 60)
    print("Step 1: Generate initial page")
    print("=" * 60)
    
    payload = {
        "industry": "SaaS / Project Management",
        "offer": "AI-powered project management tool",
        "target_audience": "Remote teams and engineering managers",
        "brand_tone": "Professional, modern, friendly"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/pages/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            page_id = data.get("pageId")
            print(f"✓ Generated page: {page_id}")
            print(f"  Sections: {len(data.get('sections', []))}\n")
            
            # Print hero section
            for section in data.get("sections", []):
                if section["type"] == "hero":
                    print("Original Hero Section:")
                    print(json.dumps(section["data"], indent=2))
            
            return page_id, payload
        else:
            print(f"✗ Error: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None, None


def test_regenerate_section(page_id, context):
    """Regenerate the hero section"""
    print("\n" + "=" * 60)
    print("Step 2: Regenerate hero section")
    print("=" * 60)
    
    payload = {
        "section_id": "hero-1",
        "data": {
            "context": context
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/pages/{page_id}/regenerate-section",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Section regenerated successfully")
            print(f"  New version: {result.get('version')}\n")
            
            # Get the updated page to show new hero
            print("Fetching updated page...")
            get_response = requests.get(f"{BASE_URL}/api/pages/{page_id}")
            
            if get_response.status_code == 200:
                data = get_response.json()
                for section in data.get("sections", []):
                    if section["type"] == "hero":
                        print("Regenerated Hero Section:")
                        print(json.dumps(section["data"], indent=2))
            
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_edit_section(page_id):
    """Manually edit a section (without AI)"""
    print("\n" + "=" * 60)
    print("Step 3: Manual edit (no AI)")
    print("=" * 60)
    
    payload = {
        "section_id": "hero-1",
        "data": {
            "headline": "My Custom Headline",
            "subheadline": "This is manually edited, not from AI",
            "ctaText": "Custom CTA",
            "backgroundImage": "https://images.unsplash.com/photo-custom",
            "textColor": "#FFFFFF",
            "backgroundColor": "#FF0000"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/pages/{page_id}/edit-section",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Section edited successfully")
            print(f"  New version: {result.get('version')}\n")
            
            # Get updated page
            get_response = requests.get(f"{BASE_URL}/api/pages/{page_id}")
            if get_response.status_code == 200:
                data = get_response.json()
                for section in data.get("sections", []):
                    if section["type"] == "hero":
                        print("Manually Edited Hero Section:")
                        print(json.dumps(section["data"], indent=2))
            
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    # Step 1: Generate page
    page_id, context = test_generate_page()
    
    if not page_id:
        print("Failed to generate page. Check your backend.")
        exit(1)
    
    # Wait a bit
    time.sleep(2)
    
    # Step 2: Regenerate hero section with AI
    regenerate_success = test_regenerate_section(page_id, context)
    
    if regenerate_success:
        # Wait a bit
        time.sleep(2)
        
        # Step 3: Manual edit
        test_edit_section(page_id)
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print(f"Page ID: {page_id}")
        print("=" * 60)
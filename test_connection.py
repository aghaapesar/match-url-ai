#!/usr/bin/env python3
"""Test script to verify AI API connection"""

import yaml
import requests
import json
from pathlib import Path

def test_liara_connection():
    # Read config
    config_path = Path("config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    ai_config = config.get("ai", {})
    
    base_url = ai_config.get("compatible_base_url")
    api_key = ai_config.get("compatible_api_key")
    model = ai_config.get("model")
    
    print("="*60)
    print("Testing Liara AI Connection")
    print("="*60)
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print(f"API Key (last 10 chars): ...{api_key[-10:]}")
    print("="*60)
    
    # Construct URL
    if base_url.endswith('/v1'):
        url = f"{base_url}/chat/completions"
    else:
        url = f"{base_url}/v1/chat/completions"
    
    print(f"\nFull URL: {url}\n")
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": "You are a test assistant. Always respond in JSON format."},
            {"role": "user", "content": "Reply with JSON: {\"status\": \"success\"}"}
        ],
        "max_tokens": 50,
        "response_format": {"type": "json_object"}
    }
    
    print("Sending test request...")
    print(f"Headers: {json.dumps({k: v[:20] + '...' if k == 'Authorization' else v for k, v in headers.items()}, indent=2)}")
    print(f"Payload: {json.dumps({k: v for k, v in payload.items() if k != 'messages'}, indent=2)}")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text[:500]}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! Connection is working.")
            data = response.json()
            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                print(f"Model response: {content}")
        else:
            print(f"❌ FAILED with status {response.status_code}")
            print(f"Error: {response.text}")
            
            # Common issues
            print("\n" + "="*60)
            print("Troubleshooting:")
            print("="*60)
            if response.status_code == 401:
                print("- Check if your API key is correct and active")
                print("- Verify the API key hasn't expired")
                print("- Make sure you're using the correct project ID in the URL")
            elif response.status_code == 404:
                print("- Check if the URL is correct")
                print("- Verify the model name is correct for your provider")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("\nCheck:")
        print("- Internet connection")
        print("- Firewall settings")
        print("- URL is accessible")

if __name__ == "__main__":
    test_liara_connection()


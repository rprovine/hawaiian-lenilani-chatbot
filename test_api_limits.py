#!/usr/bin/env python3
"""Test Claude API limits and find optimal settings"""
import anthropic
import time
import os
from dotenv import load_dotenv

load_dotenv()

def test_build_tier_limits():
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("Testing Build tier API limits...")
    
    # Test with different models
    models = [
        "claude-3-haiku-20240307",  # Fastest, cheapest
        "claude-3-5-sonnet-20241022",  # Current model in use
    ]
    
    for model in models:
        print(f"\nTesting {model}...")
        success_count = 0
        error_count = 0
        
        for i in range(5):
            try:
                print(f"  Request {i+1}...", end="")
                start_time = time.time()
                
                response = client.messages.create(
                    model=model,
                    max_tokens=50,
                    messages=[{"role": "user", "content": f"Say hello {i}"}]
                )
                
                elapsed = time.time() - start_time
                print(f" ✅ Success in {elapsed:.2f}s")
                success_count += 1
                
                # Delay between requests
                time.sleep(2.0)  # Increased delay
                
            except Exception as e:
                error_count += 1
                if "529" in str(e):
                    print(f" ❌ Overloaded")
                    print("    Waiting 15 seconds before retry...")
                    time.sleep(15)
                else:
                    print(f" ❌ Error: {e}")
                    break
        
        print(f"  Results: {success_count} success, {error_count} errors")

if __name__ == "__main__":
    test_build_tier_limits()
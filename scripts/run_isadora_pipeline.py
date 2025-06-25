import requests
import os
from datetime import datetime
import sys


def trigger_pipeline():
    print("🚀 Starting Isadora Pipeline...")
    print(f"🕐 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

    # Get environment variables
    pipeline_url = os.getenv('PIPELINE_URL')
    bearer_token = os.getenv('BEARER_TOKEN')
    custom_message = os.getenv('CUSTOM_MESSAGE', 'Scheduled pipeline run')

    print(f"📡 Endpoint: {pipeline_url}")
    print(f"🎯 Trigger: schedule")
    print(f"💬 Message: {custom_message}")
    print(f"🔑 Using {'***' if bearer_token else 'No token'} {'✅ Yes' if bearer_token else '❌ No'}")
    print("-" * 50)

    if not pipeline_url or not bearer_token:
        print("❌ Missing required environment variables")
        sys.exit(1)

    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'message': custom_message,
        'trigger_source': 'github_actions',
        'timestamp': datetime.utcnow().isoformat()
    }

    try:
        # Use a shorter timeout and don't wait for completion
        response = requests.post(
            pipeline_url,
            json=payload,
            headers=headers,
            timeout=30  # 30 second timeout
        )

        if response.status_code in [200, 202]:
            print("✅ Pipeline triggered successfully!")
            print(f"📊 Status Code: {response.status_code}")
            try:
                result = response.json()
                print(f"📝 Response: {result}")
            except:
                print(f"📝 Response: {response.text[:200]}...")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            print(f"📝 Response: {response.text[:200]}...")

    except requests.exceptions.Timeout:
        print("⏰ Request timed out after 30 seconds")
        print("✅ Pipeline likely started successfully (timeout is expected for long-running processes)")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    trigger_pipeline()
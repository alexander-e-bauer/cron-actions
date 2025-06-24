import requests
import json
import os
import sys
from datetime import datetime, timezone


def run_isadora_pipeline():
    # Get environment variables
    pipeline_url = os.getenv('PIPELINE_URL', 'https://isadora-pipeline-772695820577.us-central1.run.app/run-pipeline')
    bearer_token = os.getenv('BEARER_TOKEN')
    custom_message = os.getenv('CUSTOM_MESSAGE', 'Scheduled pipeline run')

    # Check if bearer token is provided
    if not bearer_token:
        print("❌ Error: BEARER_TOKEN environment variable is required")
        print("Please set the ISADORA_BEARER_TOKEN secret in your repository settings")
        sys.exit(1)

    # Get GitHub event information
    github_event_name = os.getenv('GITHUB_EVENT_NAME', 'unknown')
    current_time = datetime.now(timezone.utc)

    # Prepare headers exactly as in your curl command
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'GitHub-Actions-Isadora-Pipeline',
        'Accept': 'application/json'
    }

    try:
        print("🚀 Starting Isadora Pipeline...")
        print(f"🕐 Time: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"📡 Endpoint: {pipeline_url}")
        print(f"🎯 Trigger: {github_event_name}")
        print(f"💬 Message: {custom_message}")
        print(f"🔑 Using Bearer Token: {'✅ Yes' if bearer_token else '❌ No'}")
        print("-" * 50)

        # Send POST request (matching your curl command exactly)
        response = requests.post(
            pipeline_url,
            headers=headers,
            timeout=120  # 2 minutes timeout for pipeline operations
        )

        # Check if request was successful
        response.raise_for_status()

        print("✅ Pipeline request successful!")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")

        # Try to parse JSON response if available
        try:
            response_json = response.json()
            print(f"📦 Response JSON:")
            print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print(f"📄 Response Text: {response.text}")

        # Log success metrics
        print("-" * 50)
        print(f"⏱️  Request Duration: {response.elapsed.total_seconds():.2f} seconds")
        print(f"📈 Repository: {os.getenv('GITHUB_REPOSITORY', 'unknown')}")
        print(f"🔄 Run ID: {os.getenv('GITHUB_RUN_ID', 'unknown')}")

        if github_event_name == 'schedule':
            print(f"⏰ Scheduled pipeline completed successfully at {current_time.strftime('%H:%M UTC')}")

        return True

    except requests.exceptions.Timeout:
        print("⏱️ Request timed out after 2 minutes")
        print("This might be normal if the pipeline takes a long time to process")
        sys.exit(1)

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"📊 Status Code: {e.response.status_code}")
        print(f"📄 Response: {e.response.text}")

        # Log specific error details
        if e.response.status_code == 401:
            print("🔐 Authentication failed - check your bearer token")
        elif e.response.status_code == 403:
            print("🚫 Access forbidden - check your permissions")
        elif e.response.status_code == 404:
            print("🔍 Endpoint not found - check the URL")
        elif e.response.status_code >= 500:
            print("🔧 Server error - the pipeline service might be down")

        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_isadora_pipeline()
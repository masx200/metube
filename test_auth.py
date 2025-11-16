#!/usr/bin/env python3
"""
测试 HTTP 基本身份验证功能的脚本
"""

import os
import sys
import base64
import requests
import json

def test_auth():
    """测试身份验证功能"""

    # 设置测试环境变量
    os.environ['ENABLE_HTTP_AUTH'] = 'true'
    os.environ['HTTP_AUTH_USERNAME'] = 'testuser'
    os.environ['HTTP_AUTH_PASSWORD'] = 'testpass'
    os.environ['HTTP_AUTH_REALM'] = 'MeTube Test Realm'

    print("Testing HTTP Basic Authentication for MeTube")
    print("=" * 50)

    base_url = "http://localhost:8081"

    # 测试用例 1: 无身份验证的请求
    print("\n1. Testing request without authentication...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 401:
            print("✓ Correctly rejected unauthenticated request")
            print(f"  Status: {response.status_code}")
            print(f"  WWW-Authenticate: {response.headers.get('WWW-Authenticate', 'Not found')}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Connection failed - make sure MeTube is running on localhost:8081")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    # 测试用例 2: 正确的凭据
    print("\n2. Testing request with correct credentials...")
    credentials = base64.b64encode(b"testuser:testpass").decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    try:
        response = requests.get(f"{base_url}/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ Successfully authenticated with correct credentials")
            print(f"  Status: {response.status_code}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # 测试用例 3: 错误的凭据
    print("\n3. Testing request with incorrect credentials...")
    wrong_credentials = base64.b64encode(b"wronguser:wrongpass").decode('utf-8')
    wrong_headers = {'Authorization': f'Basic {wrong_credentials}'}

    try:
        response = requests.get(f"{base_url}/", headers=wrong_headers, timeout=5)
        if response.status_code == 401:
            print("✓ Correctly rejected incorrect credentials")
            print(f"  Status: {response.status_code}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # 测试用例 4: API 端点
    print("\n4. Testing API endpoint...")
    try:
        response = requests.get(f"{base_url}/version", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ API endpoint accessible with authentication")
            version_data = response.json()
            print(f"  Version info: {json.dumps(version_data, indent=2)}")
        else:
            print(f"✗ API endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n" + "=" * 50)
    print("Authentication testing completed!")
    return True

if __name__ == "__main__":
    print("This script tests the HTTP Basic Authentication feature.")
    print("Make sure MeTube is running with the following environment variables:")
    print("  ENABLE_HTTP_AUTH=true")
    print("  HTTP_AUTH_USERNAME=testuser")
    print("  HTTP_AUTH_PASSWORD=testpass")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    try:
        input()
        test_auth()
    except KeyboardInterrupt:
        print("\nTesting cancelled.")
# Slack MCP 서버

FastMCP를 이용한 Slack API 통합 서버입니다.

## 기능

1. 메시지 전송 (`send_slack_message`)
2. 채널 목록 조회 (`get_slack_channels`)
3. 채널 메시지 히스토리 조회 (`get_slack_channel_history`)
4. 다이렉트 메시지 전송 (`send_slack_direct_message`)

## 설치 및 설정

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
- `.env` 파일을 생성하고 다음 내용을 추가:
```
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
```

## 실행 방법

```bash
python slack_mcp_server.py
```

또는 FastMCP CLI를 사용:

```bash
fastmcp run slack_mcp_server.py
```

## Slack App 설정

1. [Slack API 페이지](https://api.slack.com/apps)에서 새 앱 생성
2. Bot Token Scopes에 다음 권한 추가:
   - channels:read
   - channels:history
   - chat:write
   - im:read
   - im:write
   - im:history
   - users:read
3. 앱을 워크스페이스에 설치하고 Bot User OAuth Token을 `.env` 파일에 설정
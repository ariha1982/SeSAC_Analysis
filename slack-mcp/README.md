# Slack MCP

FastMCP를 활용한 Slack API 통합 도구입니다.

## 기능

### 기본 기능
- 채널 관리
  - 채널 목록 조회
  - 채널 히스토리 조회
- 메시지 관리
  - 메시지 전송
  - 메시지 수정
  - 메시지 삭제
  - 메시지 댓글 달기
  - 메시지 예약 전송
  - 예약된 메시지 조회/삭제
  - 다이렉트 메시지 전송

### 추가 기능
- 파일 관리
  - 파일 업로드
- 이모지 반응
  - 이모지 반응 추가
  - 이모지 반응 삭제
- 검색
  - 메시지 검색
- 사용자 관리
  - 사용자 목록 조회

## 설치 방법

### 1. 가상환경 설정

#### Poetry 사용 시
```bash
# Poetry 설치 (macOS, Linux)
curl -sSL https://install.python-poetry.org | python3 -

# Poetry 설치 (Windows PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# 프로젝트 의존성 설치
poetry install
```

#### pip 사용 시
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
## macOS/Linux
source .venv/bin/activate
## Windows
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가합니다:
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_USER_TOKEN=xoxp-your-user-token  # 선택사항: 일부 고급 기능에 필요
```

## Slack App 설정

### 1. App 생성
1. [Slack API 페이지](https://api.slack.com/apps)에서 새 앱 생성
2. "From scratch" 선택
3. 앱 이름과 워크스페이스 선택

### 2. Bot Token Scopes 설정
OAuth & Permissions 페이지에서 다음 스코프 추가:

#### Bot Token Scopes
- `channels:history` - 채널 메시지 히스토리 조회
- `channels:read` - 채널 목록 및 정보 조회
- `chat:write` - 메시지 전송
- `chat:write.customize` - 사용자 지정 메시지 전송
- `files:read` - 파일 정보 조회
- `files:write` - 파일 업로드
- `reactions:read` - 이모지 반응 조회
- `reactions:write` - 이모지 반응 추가/삭제
- `users:read` - 사용자 정보 조회
- `users:read.email` - 사용자 이메일 조회
- `im:history` - DM 히스토리 조회
- `im:read` - DM 채널 정보 조회
- `im:write` - DM 전송
- `mpim:history` - 그룹 DM 히스토리 조회
- `mpim:read` - 그룹 DM 정보 조회
- `mpim:write` - 그룹 DM 전송

#### User Token Scopes (고급 기능용)
- `search:read` - 메시지 검색

### 3. 앱 설치
1. OAuth & Permissions 페이지에서 "Install App to Workspace" 클릭
2. 권한 검토 후 허용
3. Bot User OAuth Token을 복사하여 `.env` 파일에 설정

## 사용 방법

### 서버 실행

#### 기본 실행
```python
python slack_mcp_server.py
```

#### 개발 모드 실행
```bash
fastmcp dev slack_mcp_server.py
```
개발 모드에서는 MCP Inspector가 실행되어 실시간으로 도구 호출을 모니터링하고 디버깅할 수 있습니다.

### MCP 도구 목록

#### 채널 관리
- `get_slack_channels()`: 접근 가능한 모든 Slack 채널 목록 조회
- `get_slack_channel_history(channel_id, limit=10)`: 특정 채널의 메시지 히스토리 조회

#### 메시지 관리
- `send_slack_message(channel, text)`: 채널에 메시지 전송
- `send_slack_comment(channel, text, timestamp)`: 메시지에 댓글 달기
- `update_slack_message(channel, timestamp, new_text)`: 메시지 수정
- `delete_slack_message(channel, timestamp)`: 메시지 삭제
- `schedule_slack_message(channel, send_at, text)`: 메시지 예약 전송
- `get_slack_scheduled_list(channel=None)`: 예약된 메시지 목록 조회
- `delete_slack_scheduled_message(channel, scheduled_message_id)`: 예약된 메시지 삭제
- `send_slack_direct_message(user_id, text)`: 사용자에게 DM 전송

#### 파일 관리
- `upload_slack_file(channel_id, file_path, title=None)`: 파일 업로드

#### 이모지 반응
- `add_slack_reaction(channel, timestamp, reaction)`: 메시지에 이모지 반응 추가
- `remove_slack_reaction(channel, timestamp, reaction)`: 메시지에서 이모지 반응 제거

#### 검색
- `search_slack_messages(query, count=20)`: 메시지 검색

#### 사용자 관리
- `get_slack_users()`: 워크스페이스의 모든 사용자 목록 조회

## 주의사항

- 일부 기능은 Bot 토큰 권한이 필요합니다.
- 고급 기능(예: 메시지 검색)은 User 토큰이 필요할 수 있습니다.
- 모든 API 호출은 Slack의 rate limiting 정책을 따릅니다.

## 라이선스

MIT License
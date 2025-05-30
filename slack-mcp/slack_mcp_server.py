"""FastMCP를 이용한 Slack MCP 서버 구현 모듈입니다."""

from fastmcp import FastMCP
from slack_api import SlackAPIClient
from typing import Dict, Any, List, Optional

# FastMCP 서버 인스턴스 생성
mcp = FastMCP()
slack_client = SlackAPIClient()

@mcp.tool()
async def send_slack_message(channel: str, text: str) -> Dict[str, Any]:
    """지정된 Slack 채널에 메시지를 전송합니다.
    
    Args:
        channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
        text (str): 전송할 메시지 내용
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.send_message(channel, text)
    except ValueError as e:
        return {"ok": False, "error": str(e)}

@mcp.tool()
async def send_slack_comment(channel: str, text: str, timezone: str) -> Dict[str, Any]:
    """지정된 Slack 채널의 메시지에 댓글을 답니다.
    
    Args:
        channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
        text (str): 전송할 댓글 내용
        timezone (str): 댓글을 달 메시지의 타임스탬프
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.send_comment(channel, text, timezone)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    
@mcp.tool()
async def update_slack_message(channel: str, timestamp: str, new_text: str) -> Dict[str, Any]:
    """지정된 Slack 채널에 전송한 메시지를 편집합니다.
    
    Args:
        channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: C1234567890)
        timestamp (str): 편집할 메시지의 타임스탬프 (예: 1748521071.720959)
        new_text (str): 새로운 메시지 내용
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.update_message(channel, timestamp, new_text)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    
@mcp.tool()
async def delete_slack_message(channel: str, timestamp: str) -> Dict[str, Any]:
    """지정된 Slack 채널에 전송한 메시지를 편집합니다.
    
    Args:
        channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: C1234567890)
        timestamp (str): 삭제할 메시지의 타임스탬프 (예: 1748521071.720959)
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.delete_message(channel, timestamp)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    
@mcp.tool()
async def schedule_slack_message(channel: str, send_at: str, text: str) -> Dict[str, Any]:
    """지정된 Slack 채널에 메시지를 예약합니다.
    
    Args:
        channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: C1234567890, #general)
        send_at (str): 삭제할 메시지의 타임스탬프 (예: 1748521071.720959)
        text (str): 전송할 메시지 내용
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.schedule_message(channel, send_at, text)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    
@mcp.tool()
async def get_slack_scheduled_list(channel: Optional[str] = None) -> Dict[str, Any]:
    """메시지 예약 목록을 조회합니다.
    
    Args:
        channel (str, optional): 기본값은 Null로 모든 채널 조회, 채널 이름 입력 시 해당 채널 조회
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.get_scheduled_list(channel)
    except ValueError as e:
        return {"ok": False, "error": str(e)}

@mcp.tool()
async def delete_slack_scheduled_message(channel: str, scheduled_message_id: str) -> Dict[str, Any]:
    """예약된 메세지를 삭제합니다.
    
    Args:
        channel (str): 예약된 메시지가 존재하는 채널 ID(예: C1234567890)
        scheduled_message_id (str): 삭제할 메시지의 예약 ID (예: Q08US8GRVKN)
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.delete_scheduled_message(channel, scheduled_message_id)
    except ValueError as e:
        return {"ok": False, "error": str(e)}

@mcp.tool()
async def get_slack_channels() -> List[Dict[str, Any]]:
    """접근 가능한 모든 Slack 채널 목록을 조회합니다.
    
    Returns:
        List[Dict[str, Any]]: 채널 목록 (각 채널의 ID, 이름, 상태 등 포함)
    """
    try:
        return slack_client.get_channels()
    except ValueError as e:
        return [{"ok": False, "error": str(e)}]

@mcp.tool()
async def get_slack_channel_history(channel_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """지정된 채널의 메시지 히스토리를 조회합니다.
    
    Args:
        channel_id (str): 조회할 채널의 ID
        limit (int, optional): 조회할 메시지 수. 기본값은 10, 최대 100
        
    Returns:
        List[Dict[str, Any]]: 메시지 목록 (각 메시지의 내용, 작성자, 시간 등 포함)
    """
    try:
        return slack_client.get_channel_history(channel_id, limit)
    except ValueError as e:
        return [{"ok": False, "error": str(e)}]

@mcp.tool()
async def send_slack_direct_message(user_id: str, text: str) -> Dict[str, Any]:
    """특정 사용자에게 다이렉트 메시지를 전송합니다.
    
    Args:
        user_id (str): 메시지를 받을 사용자의 ID
        text (str): 전송할 메시지 내용
        
    Returns:
        Dict[str, Any]: 메시지 전송 결과
    """
    try:
        return slack_client.send_direct_message(user_id, text)
    except ValueError as e:
        return {"ok": False, "error": str(e)}

# 선택 기능 구현
@mcp.tool()
async def get_slack_users() -> List[Dict[str, Any]]:
    """워크스페이스의 모든 사용자 목록을 조회합니다.
    
    Returns:
        List[Dict[str, Any]]: 사용자 목록 (각 사용자의 ID, 이름, 상태 등 포함)
    """
    try:
        return slack_client.get_users()
    except ValueError as e:
        return [{"ok": False, "error": str(e)}]

@mcp.tool()
async def search_slack_messages(query: str, count: int = 20) -> List[Dict[str, Any]]:
    """메시지를 검색합니다.
    
    Args:
        query (str): 검색할 키워드
        count (int, optional): 검색 결과 수. 기본값은 20
        
    Returns:
        List[Dict[str, Any]]: 검색된 메시지 목록
    """
    try:
        return slack_client.search_messages(query, count)
    except ValueError as e:
        return [{"ok": False, "error": str(e)}]

@mcp.tool()
async def upload_slack_file(channel_id: str, file_path: str, title: Optional[str] = None) -> Dict[str, Any]:
    """파일을 채널에 업로드합니다.
    
    Args:
        channel_id (str): 파일을 공유할 채널 ID
        file_path (str): 업로드할 파일의 경로
        title (Optional[str], optional): 파일의 제목(반드시 큰 따옴표로 감싸야합니다)
        
    Returns:
        Dict[str, Any]: 파일 업로드 결과
    """
    try:
        return slack_client.upload_file(channel_id, file_path, title)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

@mcp.tool()
async def add_slack_reaction(channel: str, timestamp: str, reaction: str) -> Dict[str, Any]:
    """메시지에 이모지 반응을 추가합니다.
    
    Args:
        channel (str): 메시지가 있는 채널 ID
        timestamp (str): 메시지의 타임스탬프
        reaction (str): 추가할 이모지 이름 (콜론 제외)
        
    Returns:
        Dict[str, Any]: 반응 추가 결과
    """
    try:
        return slack_client.add_reaction(channel, timestamp, reaction)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    
@mcp.tool()
async def remove_slack_reaction(channel: str, timestamp: str, reaction: str) -> Dict[str, Any]:
    """메시지에 추가한 이모지 반응을 삭제합니다.
    
    Args:
        channel (str): 메시지가 있는 채널 ID
        timestamp (str): 메시지의 타임스탬프
        reaction (str): 추가할 이모지 이름 (콜론 제외)
        
    Returns:
        Dict[str, Any]: 반응 추가 결과
    """
    try:
        return slack_client.remove_reaction(channel, timestamp, reaction)
    except ValueError as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # FastMCP 서버 실행
    mcp.run()
"""Slack API와 상호작용하는 클라이언트 모듈입니다."""

import os
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

class SlackAPIClient:
    """Slack API와 상호작용하는 클라이언트 클래스입니다.
    
    이 클래스는 Slack API의 다양한 엔드포인트를 호출하여 메시지 전송, 채널 관리,
    사용자 관리 등의 기능을 제공합니다.
    
    Attributes:
        token (str): Slack Bot User OAuth Token
        base_url (str): Slack API의 기본 URL
        headers (Dict[str, str]): API 요청에 사용될 헤더
    """
    
    def __init__(self) -> None:
        """환경 변수에서 Slack 토큰을 로드하여 클라이언트를 초기화합니다."""
        load_dotenv()
        self.token = os.getenv("SLACK_BOT_TOKEN")
        self.user_token = os.getenv("SLACK_USER_TOKEN")
        if not self.token:
            raise ValueError("SLACK_BOT_TOKEN이 환경 변수에 설정되어 있지 않습니다.")
        
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def _make_request(self, method: str, endpoint: str, use_user_token: bool = False, **kwargs) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = self.headers.copy()

            # 토큰 전환
            if use_user_token:
                if not self.user_token:
                    raise ValueError("SLACK_USER_TOKEN이 환경 변수에 설정되어 있지 않습니다.")
                headers["Authorization"] = f"Bearer {self.user_token}"

            # multipart 요청일 경우 Content-Type 제거
            if "files" in kwargs:
                headers.pop("Content-Type", None)

            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            
            data = response.json()
            if not data["ok"]:
                raise ValueError(f"Slack API 오류: {data.get('error', '알 수 없는 오류')}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API 요청 실패: {str(e)}")

    
    def send_message(self, channel: str, text: str) -> Dict[str, Any]:
        """지정된 채널에 메시지를 전송합니다.
        
        Args:
            channel (str): 메시지를 전송할 채널 ID 또는 이름
            text (str): 전송할 메시지 내용
            
        Returns:
            Dict[str, Any]: 메시지 전송 결과
        """
        return self._make_request(
            "POST",
            "chat.postMessage",
            json={"channel": channel, "text": text}
        )
    
    def get_channels(self) -> List[Dict[str, Any]]:
        """접근 가능한 모든 채널 목록을 조회합니다.
        
        Returns:
            List[Dict[str, Any]]: 채널 목록 (각 채널의 ID, 이름, 상태 등 포함)
        """
        response = self._make_request("GET", "conversations.list")
        return response["channels"]
    
    def get_channel_history(self, channel_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """지정된 채널의 메시지 히스토리를 조회합니다.
        
        Args:
            channel_id (str): 조회할 채널의 ID
            limit (int, optional): 조회할 메시지 수. 기본값은 10, 최대 100
            
        Returns:
            List[Dict[str, Any]]: 메시지 목록 (각 메시지의 내용, 작성자, 시간 등 포함)
        """
        limit = min(max(1, limit), 100)  # limit 값을 1~100 사이로 제한
        response = self._make_request(
            "GET",
            "conversations.history",
            params={"channel": channel_id, "limit": limit}
        )
        return response["messages"]
    
    def send_direct_message(self, user_id: str, text: str) -> Dict[str, Any]:
        """특정 사용자에게 다이렉트 메시지를 전송합니다.
        
        Args:
            user_id (str): 메시지를 받을 사용자의 ID
            text (str): 전송할 메시지 내용
            
        Returns:
            Dict[str, Any]: 메시지 전송 결과
        """
        # 1. DM 채널 생성 또는 조회
        response = self._make_request(
            "POST",
            "conversations.open",
            json={"users": user_id}
        )
        channel_id = response["channel"]["id"]
        
        # 2. 메시지 전송
        return self.send_message(channel_id, text)
    
    def get_users(self) -> List[Dict[str, Any]]:
        """워크스페이스의 모든 사용자 목록을 조회합니다.
        
        Returns:
            List[Dict[str, Any]]: 사용자 목록 (각 사용자의 ID, 이름, 상태 등 포함)
        """
        response = self._make_request("GET", "users.list")
        return response["members"]
    
    def search_messages(self, query: str, count: int = 20) -> List[Dict[str, Any]]:
        """메시지를 검색합니다.
        
        Args:
            query (str): 검색할 키워드
            count (int, optional): 검색 결과 수. 기본값은 20
            
        Returns:
            List[Dict[str, Any]]: 검색된 메시지 목록
        """
        response = self._make_request(
            "GET",
            "search.messages",
            use_user_token=True,
            params={"query": query, "count": count}
        )
        return response["messages"]["matches"]
    
    def upload_file(self, channel_id: str, file_path: str, title: Optional[str] = None) -> Dict[str, Any]:
        """파일을 채널에 업로드합니다.
        
        Args:
            channel_id (str): 파일을 공유할 채널 ID
            file_path (str): 업로드할 파일의 경로
            title (Optional[str], optional): 파일의 제목
            
        Returns:
            Dict[str, Any]: 파일 업로드 결과
        
        Raises:
            ValueError: API 요청 실패 시
            FileNotFoundError: 파일이 존재하지 않을 때
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Step 1: Get upload URL and file_id
        upload_info = self._make_request("POST", "files.getUploadURLExternal?filename=" + filename + "&length=" + str(file_size))
        
        upload_url = upload_info["upload_url"]
        file_id = upload_info["file_id"]

        # Step 2: Upload file to provided URL
        with open(file_path, "rb") as f:
            upload_response = requests.post(
                upload_url,
                headers={"Content-Type": "application/octet-stream"},
                data=f
            )
            upload_response.raise_for_status()
        test = "checkpoint"

        # Step 3: Complete the upload
        complete_response = self._make_request("POST", "files.completeUploadExternal", json={
            "files": [{
                "id": file_id,
                "title": title
            }],
            "channel_id": channel_id
        })
        return complete_response
    
    def add_reaction(self, channel: str, timestamp: str, reaction: str) -> Dict[str, Any]:
        """메시지에 이모지 반응을 추가합니다.
        
        Args:
            channel (str): 메시지가 있는 채널 ID
            timestamp (str): 메시지의 타임스탬프
            reaction (str): 추가할 이모지 이름 (콜론 제외)
            
        Returns:
            Dict[str, Any]: 반응 추가 결과
        """
        return self._make_request(
            "POST",
            "reactions.add",
            json={
                "channel": channel,
                "timestamp": timestamp,
                "name": reaction
            }
        )
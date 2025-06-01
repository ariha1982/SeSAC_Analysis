"""Slack API와 상호작용하는 클라이언트 모듈입니다."""

import os
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

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
            channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
            text (str): 전송할 메시지 내용
            
        Returns:
            Dict[str, Any]: 메시지 전송 결과
        """
        response = self._make_request(
            "POST",
            "chat.postMessage",
            json={"channel": channel, "text": text}
        )

        return_response = {}
        if response["ok"]:
            return_response = {
                "ok": True,
                "description": "🎉 메시지 전송에 성공했습니다 🎉",
                "message": {
                    "text": text,
                    "channel": channel,
                    "ts": response["ts"]
                }
            }
        else:
            return_response = {
                "ok": False,
                "error": response["error"]
            }

        return return_response
    
    def send_comment(self, channel: str, text: str, timestamp: str) -> Dict[str, Any]:
        """지정된 채널의 메시지에 댓글을 답니다.
        
        Args:
            channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
            text (str): 전송할 댓글 내용
            timestamp (str): 댓글을 달 메시지의 타임스탬프 (예: 1748521071.720959)

        Returns:
            Dict[str, Any]: 메시지 전송 결과
        """
        response = self._make_request(
            "POST",
            "chat.postMessage",
            json={"channel": channel, "text": text, "thread_ts": timestamp}
        )

        return_response = {}
        if response["ok"]:
            return_response = {
                "ok": True,
                "description": "🎉 댓글 전송에 성공했습니다 🎉",
                "message": {
                    "text": text,
                    "channel": channel,
                    "ts": response["ts"]
                }
            }
        else:
            return_response = {
                "ok": False,
                "description": "❌ 댓글 전송에 실패했습니다 ❌",
                "error": response["error"]
            }

        return return_response
    
    def update_message(self, channel: str, timestamp: str, new_text: str) -> Dict[str, Any]:
        """지정된 채널에 메시지를 편집합니다.
        
        Args:
            channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
            timestamp (str): 편집할 메시지의 타임스탬프 (예: 1748521071.720959)
            new_text (str): 편집할 새로운 메시지 내용
            
        Returns:
            Dict[str, Any]: 메시지 수정 결과
        """
        response = self._make_request(
            "POST",
            "chat.update",
            json={"channel": channel, "ts": timestamp, "text": new_text}    
        )

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "✏️ 메시지 수정에 성공했습니다 ✏️",
                "channel": response["channel"],
                "timestamp": response["ts"],
                "message": {
                    "text": response["message"]["text"],
                    "thread_ts": response["message"]["thread_ts"]
                }
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 메시지 수정에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
    def delete_message(self, channel: str, timestamp: str) -> Dict[str, Any]:
        """지정된 채널에 메시지를 삭제합니다.
        
        Args:
            channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
            timestamp (str): 삭제할 메시지의 타임스탬프 (예: 1748521071.720959)
            
        Returns:
            Dict[str, Any]: 메시지 삭제 결과
        """
        response = self._make_request(
            "POST",
            "chat.delete",
            json={"channel": channel, "ts": timestamp}    
        )

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "🎉 메시지 삭제에 성공했습니다 🎉"
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 메시지 삭제에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
    def schedule_message(self, channel: str, send_at: str, text: str) -> Dict[str, Any]:
        """지정된 채널에 메시지를 예약합니다.
        
        Args:
            channel (str): 메시지를 전송할 채널 ID 또는 이름 (예: #general, C1234567890)
            send_at (str): 메시지를 전송할 시간 (예: 2025-05-30 10:00)
            text (str): 전송할 메시지 내용
            
        Returns:
            Dict[str, Any]: 메시지 전송 결과
        """
        kst = timezone(timedelta(hours=9))
        unixtime = int(datetime.strptime(send_at, "%Y-%m-%d %H:%M").replace(tzinfo=kst).timestamp())

        response = self._make_request(
            "POST",
            "chat.scheduleMessage",
            json={"channel": channel, "post_at": unixtime, "text": text}    
        )

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "🎉 메시지 예약에 성공했습니다 🎉",
                "scheduled_message_id": response["scheduled_message_id"],
                "channel": response["channel"],
                "post_at": response["post_at"],
                "message": response["message"]["text"]
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 메시지 예약에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
    def get_scheduled_list(self, channel: Optional[str] = None) -> Dict[str, Any]:
        """예약된 메시지 목록을 조회합니다.
        
        Args:
            channel (str, optional): 기본값은 Null로 모든 채널 조회, 채널 ID 입력 시 해당 채널 조회
            
        Returns:
            Dict[str, Any]: 예약된 메시지 목록
        """
        
        if channel is None:
            channel = ""
        response = self._make_request(
            "POST",
            "chat.scheduledMessages.list?channel=" + channel    
        )

        formatted_response = {}
        if response["ok"]:
            formatted_messages = []
            for message in response["scheduled_messages"]:
                formatted_messages.append({
                    "scheduled_message_id": message["id"],
                    "channel": message["channel_id"],
                    "post_at": message["post_at"],
                    "message": message["text"]
                })
            
            formatted_response = {
                "ok": True,
                "description": "📋 예약된 메시지 목록 조회에 성공했습니다 📋",
                "messages": formatted_messages
            }

        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 예약된 메시지 목록 조회에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
    def delete_scheduled_message(self, channel: str, scheduled_message_id: str) -> Dict[str, Any]:
        """지정 채널의 예약 메시지를 삭제합니다.
        
        Args:
            channel (str): 예약된 메시지가 존재하는 채널 ID (예: C1234567890)
            scheduled_message_id (str): 삭제할 메시지의 예약 ID (예: Q08US8GRVKN)
            
        Returns:
            Dict[str, Any]: 메시지 전송 결과
        """
        response = self._make_request(
            "POST",
            "chat.deleteScheduledMessage",  
            json={"channel": channel, "scheduled_message_id": scheduled_message_id}
        )

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "🎉 예약 메시지 삭제에 성공했습니다 🎉"
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 예약 메시지 삭제에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
    def get_channels(self) -> List[Dict[str, Any]]:
        """접근 가능한 모든 채널 목록을 조회합니다.
        Args:
            없음

        Returns:
            List[Dict[str, Any]]: 채널 목록 (각 채널의 ID, 이름, 상태 등 포함)
        """
        response = self._make_request("GET", "conversations.list")

        formatted_response = {}
        if response["ok"]:
            formatted_channels = []
            for channel in response["channels"]:
                formatted_channels.append({
                    "id": channel["id"],
                    "name": channel["name"],
                    "description": channel["purpose"]["value"],
                    "is_private": channel["is_private"],
                    "creator": channel["creator"],
                    "is_member": channel["is_member"],
                    "member_count": channel["num_members"]
                })
            formatted_response = {
                "ok": True,
                "description": "📋 채널 목록 조회에 성공했습니다 📋",
                "channels": formatted_channels
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 채널 목록 조회에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
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

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "📜 메시지 히스토리 조회에 성공했습니다 📜",
                "messages": response["messages"]
            }

        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 메시지 히스토리 조회에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
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

        formatted_response = {}
        if response["ok"]:
            formatted_users = []
            for user in response["members"]:
                formatted_users.append({
                    "user_id": user["id"],
                    "slack_name": user["name"],
                    "deleted": user["deleted"],
                    "is_bot": user["is_bot"],
                    "is_admin": user["is_admin"],
                    "is_owner": user["is_owner"],
                    "profile": {
                        "real_name": user["profile"]["real_name"],
                        "display_name": user["profile"]["display_name"],
                        "first_name": user["profile"]["first_name"],
                        "last_name": user["profile"]["last_name"],
                        "phone": user["profile"]["phone"],
                        "skype": user["profile"]["skype"],
                        "status_text": user["profile"]["status_text"],
                        "status_text_canonical": user["profile"]["status_text_canonical"],
                        "status_emoji": user["profile"]["status_emoji"]
                    }
                })
            
            formatted_response = {
                "ok": True,
                "description": "📋 사용자 목록 조회에 성공했습니다 📋",
                "users": formatted_users
            }
            
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 사용자 목록 조회에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
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

        formatted_response = {}
        if response["ok"]:
            formatted_messages = []
            for message in response["messages"]["matches"]:
                formatted_messages.append({
                    "iid": message["iid"],
                    "type": message["type"],
                    "text": message["text"],
                    "team": message["team"],
                    "score": message["score"],
                    "channel": {
                        "id": message["channel"]["id"],
                        "name": message["channel"]["name"],
                    },
                    "user_id": message["user"],
                    "user_name": message["username"],
                    "timestamp": message["ts"]
                })

            formatted_response = {
                "ok": True,
                "description": "🔍 메시지 검색에 성공했습니다 🔍",
                "messages": formatted_messages
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 메시지 검색에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
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

        formatted_response = {}
        if complete_response["ok"]:
            formatted_files = []
            for file in complete_response["files"]:
                formatted_files.append({
                    "id": file["id"],
                    "title": file["title"],
                    "timestamp": file["timestamp"]
                })

            formatted_response = {
                "ok": True,
                "description": "🎉 파일 업로드에 성공했습니다 🎉",
                "file_id": formatted_files
            }

        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 파일 업로드에 실패했습니다 ❌",
                "error": complete_response["error"]
            }

        return formatted_response
    
    def add_reaction(self, channel: str, timestamp: str, reaction: str) -> Dict[str, Any]:
        """메시지에 이모지 반응을 추가합니다.
        
        Args:
            channel (str): 메시지가 있는 채널 ID (예: C1234567890)
            timestamp (str): 메시지의 타임스탬프 (예: 1748521071.720959)
            reaction (str): 추가할 이모지 이름 (콜론 제외, 영어로 입력)
            
        Returns:
            Dict[str, Any]: 반응 추가 결과
        """

        response = self._make_request(
            "POST",
            "reactions.add",
            json={
                "channel": channel,
                "timestamp": timestamp,
                "name": reaction
            }
        )

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "🎉 " + reaction + " 이모지 추가에 성공했습니다 🎉"
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 이모지 반응 추가에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
    
    def remove_reaction(self, channel: str, timestamp: str, reaction: str) -> Dict[str, Any]:
        """메시지에 추가한 이모지 반응을 삭제합니다.
        
        Args:
            channel (str): 메시지가 있는 채널 ID
            timestamp (str): 메시지의 타임스탬프
            reaction (str): 삭제할 이모지 이름 (콜론 제외, 영어로 입력)
            
        Returns:
            Dict[str, Any]: 반응 삭제 결과
        """

        response = self._make_request(
            "POST",
            "reactions.remove",
            json={
                "channel": channel,
                "timestamp": timestamp,
                "name": reaction
            }
        )

        formatted_response = {}
        if response["ok"]:
            formatted_response = {
                "ok": True,
                "description": "🎉 " + reaction + " 이모지 삭제에 성공했습니다 🎉"
            }
        else:
            formatted_response = {
                "ok": False,
                "description": "❌ 이모지 반응 삭제에 실패했습니다 ❌",
                "error": response["error"]
            }

        return formatted_response
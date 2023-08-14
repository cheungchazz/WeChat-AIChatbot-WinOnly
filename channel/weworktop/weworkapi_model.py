import requests


class MyApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def client_create(self):
        """
        创建实例
        """
        return requests.post(f"{self.base_url}/create").json()

    def client_open(self, guid, smart):
        """
        打开企业微信
        """
        return requests.post(f"{self.base_url}/open", json={"guid": guid, "smart": smart}).json()

    def client_set_callback_url(self, callback_url):
        """
        设置接收通知地址
        """
        return requests.post(f"{self.base_url}/set_callback_url", json={"callback_url": callback_url}).json()

    def user_get_profile(self, guid):
        """
        获取自己的信息
        """
        return requests.post(f"{self.base_url}/get_profile", json={"guid": guid}).json()

    def get_inner_contacts(self, guid, page_num, page_size):
        """
        获取同事列表
        """
        return requests.post(f"{self.base_url}/get_inner_contacts",
                             json={"guid": guid, "page_num": page_num, "page_size": page_size}).json()

    def get_external_contacts(self, guid, page_num, page_size):
        """
        获取客户列表
        """
        return requests.post(f"{self.base_url}/get_external_contacts",
                             json={"guid": guid, "page_num": page_num, "page_size": page_size}).json()

    def get_contact_detail(self, guid, user_id):
        """
        获取指定联系人详细信息
        """
        return requests.post(f"{self.base_url}/get_contact_detail",
                             json={"guid": guid, "user_id": user_id}).json()

    def get_rooms(self, guid):
        """
        获取群列表
        """
        return requests.post(f"{self.base_url}/get_rooms", json={"guid": guid}).json()

    def get_room_members(self, guid, conversation_id, page_num, page_size):
        """
        获取群成员列表
        """
        return requests.post(f"{self.base_url}/get_room_members",
                             json={"guid": guid, "conversation_id": conversation_id, "page_num": page_num,
                                   "page_size": page_size}).json()

    def msg_send_text(self, guid, conversation_id, content):
        """
        发送文本消息
        """
        return requests.post(f"{self.base_url}/send_text",
                             json={"guid": guid, "conversation_id": conversation_id, "content": content}).json()

    def send_room_at(self, guid, conversation_id, content, at_list):
        """
        发送群@消息
        """
        return requests.post(f"{self.base_url}/send_room_at",
                             json={"guid": guid, "conversation_id": conversation_id, "content": content,
                                   "at_list": at_list}).json()

    def send_card(self, guid, conversation_id, user_id):
        """
        发送名片
        """
        return requests.post(f"{self.base_url}/send_card",
                             json={"guid": guid, "conversation_id": conversation_id, "user_id": user_id}).json()

    def send_link_card(self, guid, conversation_id, title, desc, url, image_url):
        """
        发送链接卡片消息
        """
        return requests.post(f"{self.base_url}/send_link_card",
                             json={"guid": guid, "conversation_id": conversation_id, "title": title, "desc": desc,
                                   "url": url, "image_url": image_url}).json()

    def send_image(self, guid, conversation_id, file_path):
        """
        发送图片
        """
        return requests.post(f"{self.base_url}/send_image",
                             json={"guid": guid, "conversation_id": conversation_id, "file_path": file_path}).json()

    def send_file(self, guid, conversation_id, file_path):
        """
        发送文件
        """
        return requests.post(f"{self.base_url}/send_file",
                             json={"guid": guid, "conversation_id": conversation_id, "file_path": file_path}).json()

    def send_video(self, guid, conversation_id, file_path):
        """
        发送视频
        """
        return requests.post(f"{self.base_url}/send_video",
                             json={"guid": guid, "conversation_id": conversation_id, "file_path": file_path}).json()

    def send_gif(self, guid, conversation_id, file_path):
        """
        发送GIF
        """
        return requests.post(f"{self.base_url}/send_gif",
                             json={"guid": guid, "conversation_id": conversation_id, "file_path": file_path}).json()

    def send_voice(self, guid, conversation_id, file_id, size, voice_time, aes_key, md5):
        """
        发送语音
        """
        return requests.post(f"{self.base_url}/send_voice",
                             json={"guid": guid, "conversation_id": conversation_id, "file_id": file_id, "size": size,
                                   "voice_time": voice_time, "aes_key": aes_key, "md5": md5}).json()

    def cdn_upload(self, guid, file_path, file_type):
        """
        上传CDN文件
        """
        return requests.post(f"{self.base_url}/cdn_upload",
                             json={"guid": guid, "file_path": file_path, "file_type": file_type}).json()

    def c2c_cdn_download(self, guid, file_id, aes_key, file_size, file_type, save_path):
        """
        下载c2c类型的cdn文件
        """
        return requests.post(f"{self.base_url}/c2c_cdn_download",
                             json={"guid": guid, "file_id": file_id, "aes_key": aes_key, "file_size": file_size,
                                   "file_type": file_type, "save_path": save_path}).json()

    def wx_cdn_download(self, guid, url, auth_key, aes_key, size, save_path):
        """
        下载wx类型的cdn文件
        """
        return requests.post(f"{self.base_url}/wx_cdn_download",
                             json={"guid": guid, "url": url, "auth_key": auth_key, "aes_key": aes_key, "size": size,
                                   "save_path": save_path}).json()

    def accept_friend(self, guid, user_id, corp_id):
        """
        同意加好友请求
        """
        return requests.post(f"{self.base_url}/accept_friend",
                             json={"guid": guid, "user_id": user_id, "corp_id": corp_id}).json()

    def send_miniapp(self, guid, aes_key, file_id, size, appicon, appid, appname, conversation_id, page_path, title,
                     username):
        """
        发送小程序
        """
        return requests.post(f"{self.base_url}/send_miniapp",
                             json={"guid": guid, "aes_key": aes_key, "file_id": file_id, "size": size,
                                   "appicon": appicon, "appid": appid, "appname": appname,
                                   "conversation_id": conversation_id, "page_path": page_path, "title": title,
                                   "username": username}).json()

    def invite_to_room(self, user_list: list, conversation_id: str):
        """
        添加或邀请好友进群
        """
        return requests.post(f"{self.base_url}/invite_to_room",
                             json={"user_list": user_list, "conversation_id": conversation_id}).json()

    def create_empty_room(self):
        """
        创建空外部群聊
        """
        return requests.post(f"{self.base_url}/create_empty_room", json={}).json()

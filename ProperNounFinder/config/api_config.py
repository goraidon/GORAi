import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

class APIConfig:
    """OpenAI API設定クラス"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルに設定してください。")
    
    def get_api_key(self):
        """APIキーを取得"""
        return self.api_key
    
    def get_model(self):
        """使用するモデルを取得"""
        return self.model 
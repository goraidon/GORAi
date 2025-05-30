import os
import sys
import pandas as pd
import json
from openai import OpenAI
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.api_config import APIConfig
from prompts.prompts import ProperNounAnalyzer

class ProperNounProcessor:
    """固有名詞処理クラス"""
    
    def __init__(self):
        """初期化"""
        self.config = APIConfig()
        self.client = OpenAI(api_key=self.config.get_api_key())
        self.analyzer = ProperNounAnalyzer()
        self.project_root = project_root
    
    def analyze_text(self, text):
        """テキストの固有名詞分析"""
        if pd.isna(text) or str(text).strip() == "":
            return {
                "contains_proper_noun": False,
                "reason": "空のテキストです",
                "proper_nouns": [],
                "replaced_text": str(text)
            }
        
        try:
            prompt = self.analyzer.get_analysis_prompt(str(text))
            
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": "あなたは日本語テキストの固有名詞を分析する専門家です。正確にJSON形式で回答してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content.strip()
            # JSONの前後にある説明文を削除
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            result = json.loads(result_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON解析エラー: {e}")
            print(f"レスポンス: {result_text}")
            return {
                "contains_proper_noun": False,
                "reason": f"API応答の解析に失敗しました: {str(e)}",
                "proper_nouns": [],
                "replaced_text": str(text)
            }
        except Exception as e:
            print(f"API呼び出しエラー: {e}")
            return {
                "contains_proper_noun": False,
                "reason": f"API呼び出しに失敗しました: {str(e)}",
                "proper_nouns": [],
                "replaced_text": str(text)
            }
    
    def process_csv(self, input_file, output_file):
        """CSVファイルを処理"""
        try:
            # CSVファイルを読み込み
            df = pd.read_csv(input_file)
            print(f"入力ファイル読み込み完了: {len(df)}行 x {len(df.columns)}列")
            
            # 結果を格納する新しいDataFrame
            results = []
            
            for idx, row in df.iterrows():
                print(f"処理中: {idx + 1}/{len(df)}行目")
                row_result = {"row_index": idx}
                
                # 各カラムを分析
                for column in df.columns:
                    cell_value = row[column]
                    analysis = self.analyze_text(cell_value)
                    
                    # 結果をカラムに追加
                    row_result[f"{column}_original"] = cell_value
                    row_result[f"{column}_contains_proper_noun"] = analysis["contains_proper_noun"]
                    row_result[f"{column}_reason"] = analysis["reason"]
                    row_result[f"{column}_proper_nouns"] = ", ".join(analysis["proper_nouns"]) if analysis["proper_nouns"] else ""
                    row_result[f"{column}_replaced_text"] = analysis["replaced_text"]
                
                results.append(row_result)
            
            # 結果をDataFrameに変換
            result_df = pd.DataFrame(results)
            
            # CSVファイルに出力
            result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"処理完了: {output_file}")
            
            return result_df
            
        except Exception as e:
            print(f"CSV処理エラー: {e}")
            raise

def main():
    """メイン関数"""
    processor = ProperNounProcessor()
    
    # 入力・出力ファイルパス
    input_dir = processor.project_root / "input"
    output_dir = processor.project_root / "output"
    
    # 入力ディレクトリ内のCSVファイルを検索
    csv_files = list(input_dir.glob("*.csv"))
    
    if not csv_files:
        print("inputディレクトリにCSVファイルが見つかりません。")
        print("サンプルCSVファイルを作成します...")
        
        # サンプルCSVファイルを作成
        sample_data = {
            "name": ["田中太郎", "佐藤花子", "山田次郎"],
            "company": ["トヨタ自動車", "ソニー", "任天堂"],
            "location": ["東京都", "大阪府", "京都市"],
            "description": ["車を作っている", "ゲームを開発している", "音楽を聞く"]
        }
        sample_df = pd.DataFrame(sample_data)
        sample_file = input_dir / "sample.csv"
        sample_df.to_csv(sample_file, index=False, encoding='utf-8-sig')
        print(f"サンプルファイルを作成しました: {sample_file}")
        csv_files = [sample_file]
    
    # 各CSVファイルを処理
    for csv_file in csv_files:
        print(f"\n処理開始: {csv_file.name}")
        output_file = output_dir / f"analyzed_{csv_file.name}"
        
        try:
            processor.process_csv(csv_file, output_file)
            print(f"✅ 処理完了: {output_file.name}")
        except Exception as e:
            print(f"❌ エラー: {csv_file.name} - {e}")

if __name__ == "__main__":
    main() 
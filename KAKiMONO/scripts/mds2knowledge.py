import os
import glob
from pathlib import Path
from datetime import datetime

def merge_md_files():
    """
    指定されたディレクトリ内のmdファイルを全て読み込み、
    各ファイルの内容の冒頭にファイル名をヘッダーとして追加し、
    一つのmdファイルにまとめて出力する
    """
    
    # スクリプトファイルの場所を基準とした相対パス
    script_dir = Path(__file__).parent
    input_dir = script_dir.parent / "inputs" / "processed"
    output_dir = script_dir.parent / "outputs"
    
    # 出力ディレクトリが存在しない場合は作成
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 入力ディレクトリ内のmdファイルを取得（ソート済み）
    md_files = sorted(input_dir.glob("*.md"))
    
    if not md_files:
        print("処理対象のmdファイルが見つかりませんでした。")
        return
    
    # 出力ファイル名（現在の日時を含む）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"merged_knowledge_{timestamp}.md"
    
    # 統合されたコンテンツを格納するリスト
    merged_content = []
    
    print(f"処理開始: {len(md_files)}個のファイルを処理します...")
    
    # 各mdファイルを処理
    for file_path in md_files:
        try:
            # ファイル名（拡張子なし）を取得
            filename = file_path.stem
            
            # ファイルの内容を読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # ファイル名をヘッダーとして追加し、内容と結合
            file_section = f"# {filename}\n\n{content}\n\n"
            merged_content.append(file_section)
            
            print(f"処理完了: {filename}")
            
        except Exception as e:
            print(f"エラー: {file_path} の処理中にエラーが発生しました: {e}")
            continue
    
    # 統合されたコンテンツを出力ファイルに書き込み
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 全体のヘッダーを追加
            f.write(f"# 統合ナレッジベース\n\n")
            f.write(f"生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
            f.write(f"処理ファイル数: {len(merged_content)}個\n\n")
            f.write("---\n\n")
            
            # 各ファイルの内容を書き込み
            for content in merged_content:
                f.write(content)
                f.write("---\n\n")  # セクション区切り
        
        print(f"\n✅ 処理完了!")
        print(f"📁 出力ファイル: {output_file}")
        print(f"📊 処理されたファイル数: {len(merged_content)}個")
        
    except Exception as e:
        print(f"❌ 出力ファイルの書き込み中にエラーが発生しました: {e}")

if __name__ == "__main__":
    merge_md_files()

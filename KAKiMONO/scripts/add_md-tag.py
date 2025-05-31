import os
import re
from pathlib import Path

def add_heading_level(content):
    """
    Markdownファイルの内容で、見出し（#で始まる行）に#を1つ追加する
    """
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # 行の先頭が#で始まる場合（見出し行）
        if re.match(r'^#+\s', line):
            # #を1つ追加
            processed_line = '#' + line
            processed_lines.append(processed_line)
        else:
            # 見出し行でない場合はそのまま
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def process_markdown_files():
    """
    raw-dataディレクトリ内の全てのmdファイルを処理して、
    processedディレクトリに出力する
    """
    # スクリプトファイルの場所を基準にした相対パスを設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # scriptsディレクトリの親ディレクトリ
    
    input_dir = project_root / "inputs" / "raw-data"
    output_dir = project_root / "inputs" / "processed"
    
    # 入力ディレクトリが存在するかチェック
    if not input_dir.exists():
        print(f"エラー: 入力ディレクトリが見つかりません: {input_dir}")
        return
    
    # 出力ディレクトリが存在しない場合は作成
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 処理したファイル数をカウント
    processed_count = 0
    
    # raw-dataディレクトリ内の全てのmdファイルを処理
    for md_file in input_dir.glob("*.md"):
        try:
            # ファイルを読み込み
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 見出しレベルを1つ下げる処理
            processed_content = add_heading_level(content)
            
            # 出力ファイルパスを設定
            output_file = output_dir / md_file.name
            
            # 処理済みファイルを出力
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            processed_count += 1
            print(f"処理完了: {md_file.name}")
            
        except Exception as e:
            print(f"エラー: {md_file.name} の処理中にエラーが発生しました: {e}")
    
    print(f"\n処理完了: {processed_count}個のファイルを処理しました")
    print(f"入力元: {input_dir}")
    print(f"出力先: {output_dir}")

if __name__ == "__main__":
    process_markdown_files()

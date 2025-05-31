import os
import re
from pathlib import Path

def extract_books_from_md(file_path):
    """
    mdファイルから本のタイトルとリンクを抽出する
    """
    books = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Markdownのリンク形式 [タイトル](URL) を抽出
        # リンクがあるもののみを対象とする
        link_pattern = r'- \[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        for title, url in matches:
            books.append({
                'title': title.strip(),
                'url': url.strip()
            })
            
        # リンクがない本のタイトルも抽出（小説など）
        # ただし、リンクがない場合はURLを空にする
        no_link_pattern = r'- ([^[\n]+)(?:\n|$)'
        no_link_matches = re.findall(no_link_pattern, content)
        
        for title in no_link_matches:
            title = title.strip()
            # 既にリンク付きで抽出されていないかチェック
            if title and not any(book['title'] == title for book in books):
                # リンク形式でないことを確認
                if not re.match(r'\[.*\]\(.*\)', title):
                    books.append({
                        'title': title,
                        'url': ''
                    })
    
    except Exception as e:
        print(f"ファイル {file_path} の読み込み中にエラーが発生しました: {e}")
    
    return books

def process_all_md_files():
    """
    inputsディレクトリ内のすべてのmdファイルを処理し、
    本のタイトルとリンクを抽出してoutputsディレクトリに出力する
    """
    # スクリプトの場所を基準に相対パスを設定
    script_dir = Path(__file__).parent
    inputs_dir = script_dir.parent / 'inputs'
    outputs_dir = script_dir.parent / 'outputs'
    
    # outputsディレクトリが存在しない場合は作成
    outputs_dir.mkdir(exist_ok=True)
    
    all_books = []
    processed_files = []
    
    # inputsディレクトリ内のすべてのmdファイルを処理
    if inputs_dir.exists():
        for md_file in inputs_dir.glob('*.md'):
            print(f"処理中: {md_file.name}")
            books = extract_books_from_md(md_file)
            all_books.extend(books)
            processed_files.append(md_file.name)
    else:
        print(f"inputsディレクトリが見つかりません: {inputs_dir}")
        return
    
    if not all_books:
        print("本の情報が見つかりませんでした。")
        return
    
    # 重複を除去（タイトルベース）
    unique_books = []
    seen_titles = set()
    
    for book in all_books:
        if book['title'] not in seen_titles:
            unique_books.append(book)
            seen_titles.add(book['title'])
    
    # 出力ファイルを作成
    output_file = outputs_dir / 'consolidated_booklist.md'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("# 読書リスト\n\n")
            file.write(f"## 処理したファイル\n")
            for filename in processed_files:
                file.write(f"- {filename}\n")
            file.write(f"\n## 抽出された本の数: {len(unique_books)}冊\n\n")
            
            # リンクありの本とリンクなしの本を分けて出力
            books_with_links = [book for book in unique_books if book['url']]
            books_without_links = [book for book in unique_books if not book['url']]
            
            if books_with_links:
                file.write("## リンク付きの本\n\n")
                for book in books_with_links:
                    file.write(f"- [{book['title']}]({book['url']})\n")
                file.write("\n")
            
            if books_without_links:
                file.write("## リンクなしの本\n\n")
                for book in books_without_links:
                    file.write(f"- {book['title']}\n")
                file.write("\n")
            
            file.write("---\n\n")
            file.write("*このファイルは自動生成されました*\n")
        
        print(f"✅ 処理完了！")
        print(f"📁 出力ファイル: {output_file}")
        print(f"📚 抽出された本の数: {len(unique_books)}冊")
        print(f"🔗 リンク付き: {len(books_with_links)}冊")
        print(f"📖 リンクなし: {len(books_without_links)}冊")
        
    except Exception as e:
        print(f"出力ファイルの作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    process_all_md_files()

"""
汎用スクレイピングツール用設定ファイル生成ツール
対話形式で設定ファイルを簡単に作成
"""

import json
import os
from typing import Dict, List


def get_user_input(prompt: str, default: str = "", required: bool = True) -> str:
    """ユーザー入力を取得"""
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("この項目は必須です。")


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Yes/No入力を取得"""
    default_str = "Y/n" if default else "y/N"
    while True:
        value = input(f"{prompt} [{default_str}]: ").strip().lower()
        if value in ['y', 'yes']:
            return True
        elif value in ['n', 'no']:
            return False
        elif value == "":
            return default
        else:
            print("'y' または 'n' を入力してください。")


def create_selector() -> Dict:
    """セレクタ設定を作成"""
    print("\n--- セレクタ設定 ---")
    by_options = {
        "1": "id",
        "2": "class_name", 
        "3": "tag_name",
        "4": "css_selector",
        "5": "xpath",
        "6": "name",
        "7": "link_text",
        "8": "partial_link_text"
    }
    
    print("セレクタの種類を選択してください:")
    for key, value in by_options.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("選択 [4]: ").strip()
        if choice == "":
            choice = "4"
        if choice in by_options:
            by = by_options[choice]
            break
        else:
            print("有効な選択肢を入力してください。")
    
    value = get_user_input(f"{by}の値")
    
    return {
        "by": by,
        "value": value
    }


def create_action() -> Dict:
    """アクション設定を作成"""
    print("\n--- アクション設定 ---")
    action_types = {
        "1": "click",
        "2": "input",
        "3": "select",
        "4": "wait",
        "5": "scroll",
        "6": "javascript",
        "7": "hover",
        "8": "key_press"
    }
    
    print("アクションの種類を選択してください:")
    for key, value in action_types.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("選択 [1]: ").strip()
        if choice == "":
            choice = "1"
        if choice in action_types:
            action_type = action_types[choice]
            break
        else:
            print("有効な選択肢を入力してください。")
    
    action = {"type": action_type}
    
    if action_type in ["click", "input", "select", "hover", "key_press"]:
        action["selector"] = create_selector()
    
    if action_type == "input":
        action["value"] = get_user_input("入力する値")
    
    elif action_type == "select":
        select_by = get_user_input("選択方法 (value/text/index)", "value")
        action[select_by] = get_user_input(f"選択する{select_by}")
    
    elif action_type == "wait":
        seconds = input("待機時間（秒） [1]: ").strip()
        action["seconds"] = int(seconds) if seconds else 1
    
    elif action_type == "scroll":
        if get_yes_no("要素までスクロールしますか？", False):
            action["selector"] = create_selector()
        else:
            pixels = input("スクロール量（ピクセル） [0]: ").strip()
            action["pixels"] = int(pixels) if pixels else 0
    
    elif action_type == "javascript":
        action["script"] = get_user_input("実行するJavaScriptコード")
    
    elif action_type == "key_press":
        action["key"] = get_user_input("押すキー (例: ENTER, TAB)")
    
    # 共通設定
    if action_type != "wait":
        timeout = input("タイムアウト時間（秒） [10]: ").strip()
        action["timeout"] = int(timeout) if timeout else 10
        
        wait_after = input("実行後の待機時間（秒） [1]: ").strip()
        action["wait_after"] = int(wait_after) if wait_after else 1
    
    action["required"] = get_yes_no("必須アクションですか？", False)
    
    return action


def create_field() -> Dict:
    """フィールド設定を作成"""
    field = {}
    
    extract_types = {
        "1": "text",
        "2": "attribute",
        "3": "html",
        "4": "regex"
    }
    
    print("抽出タイプを選択してください:")
    for key, value in extract_types.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("選択 [1]: ").strip()
        if choice == "":
            choice = "1"
        if choice in extract_types:
            field["type"] = extract_types[choice]
            break
        else:
            print("有効な選択肢を入力してください。")
    
    if get_yes_no("個別のセレクタを使用しますか？", True):
        field["selector"] = get_user_input("CSSセレクタ")
    
    if field["type"] == "attribute":
        field["attribute"] = get_user_input("取得する属性名")
    
    elif field["type"] == "regex":
        field["pattern"] = get_user_input("正規表現パターン")
    
    default_value = input("デフォルト値 []: ").strip()
    if default_value:
        field["default"] = default_value
    
    return field


def create_extraction_config() -> Dict:
    """データ抽出設定を作成"""
    print("\n--- データ抽出設定 ---")
    
    extraction_type = "1" if get_yes_no("リスト形式のデータですか？", True) else "2"
    
    extraction = {}
    
    if extraction_type == "1":
        # リスト形式
        extraction["items"] = {}
        extraction["items"]["selector"] = get_user_input("アイテムのCSSセレクタ")
        extraction["items"]["fields"] = {}
        
        print("\nフィールドを追加してください:")
        while True:
            field_name = input("フィールド名 (空白で終了): ").strip()
            if not field_name:
                break
            
            print(f"\n--- {field_name}フィールド設定 ---")
            extraction["items"]["fields"][field_name] = create_field()
    
    else:
        # 単一レコード形式
        extraction["fields"] = {}
        
        print("\nフィールドを追加してください:")
        while True:
            field_name = input("フィールド名 (空白で終了): ").strip()
            if not field_name:
                break
            
            print(f"\n--- {field_name}フィールド設定 ---")
            extraction["fields"][field_name] = create_field()
    
    return extraction


def create_site_config() -> Dict:
    """サイト設定を作成"""
    print("\n=== サイト設定 ===")
    
    site = {}
    site["name"] = get_user_input("サイト名")
    site["url"] = get_user_input("URL")
    
    initial_wait = input("初期待機時間（秒） [3]: ").strip()
    site["initial_wait"] = int(initial_wait) if initial_wait else 3
    
    wait_after = input("サイト処理後の待機時間（秒） [2]: ").strip()
    site["wait_after"] = int(wait_after) if wait_after else 2
    
    # アクション設定
    site["actions"] = []
    if get_yes_no("アクションを追加しますか？", True):
        print("\nアクションを追加してください:")
        while True:
            if get_yes_no("アクションを追加しますか？", True):
                site["actions"].append(create_action())
            else:
                break
    
    # データ抽出設定
    if get_yes_no("データ抽出を行いますか？", True):
        site["extraction"] = create_extraction_config()
    
    return site


def main():
    """メイン関数"""
    print("=== 汎用スクレイピングツール設定ファイル生成 ===\n")
    
    config = {}
    
    # 基本設定
    print("--- 基本設定 ---")
    config["headless"] = get_yes_no("ヘッドレスモードで実行しますか？", True)
    
    implicit_wait = input("要素待機時間（秒） [10]: ").strip()
    config["implicit_wait"] = int(implicit_wait) if implicit_wait else 10
    
    config["log_level"] = get_user_input("ログレベル (DEBUG/INFO/WARNING/ERROR)", "INFO")
    
    user_agent = input("User-Agent [デフォルト]: ").strip()
    if user_agent:
        config["user_agent"] = user_agent
    else:
        config["user_agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # 出力設定
    print("\n--- 出力設定 ---")
    output_file = get_user_input("出力ファイル名", "scraped_data.csv")
    output_format = get_user_input("出力形式 (csv/json/excel)", "csv")
    
    config["output"] = {
        "file": output_file,
        "format": output_format
    }
    
    # サイト設定
    config["sites"] = []
    
    print("\n--- サイト設定 ---")
    while True:
        config["sites"].append(create_site_config())
        
        if not get_yes_no("他のサイトを追加しますか？", False):
            break
    
    # 設定ファイル保存
    print("\n--- 保存 ---")
    config_file = get_user_input("設定ファイル名", "generated_config.json")
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n設定ファイルが作成されました: {config_file}")
    print(f"実行コマンド: python universal_scraper.py --config {config_file}")


if __name__ == "__main__":
    main() 
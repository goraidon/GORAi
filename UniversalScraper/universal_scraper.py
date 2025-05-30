"""
汎用的Webスクレイピングフレームワーク
任意のWebサイトに対応可能な設定ベースのスクレイピングツール
"""

import json
import logging
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd


class UniversalScraper:
    """汎用Webスクレイピングクラス"""
    
    def __init__(self, config: Dict):
        """
        初期化
        
        Args:
            config (Dict): 設定辞書
        """
        self.config = config
        self.driver = None
        self.logger = self._setup_logger()
        self.scraped_data = []
        
    def _setup_logger(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, self.config.get('log_level', 'INFO')))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _setup_driver(self) -> webdriver.Chrome:
        """WebDriver設定"""
        options = Options()
        
        # 基本オプション
        chrome_options = self.config.get('chrome_options', [])
        for option in chrome_options:
            options.add_argument(option)
        
        # デフォルトオプション
        default_options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-blink-features=AutomationControlled"
        ]
        
        for option in default_options:
            if option not in chrome_options:
                options.add_argument(option)
        
        # ヘッドレスモード
        if self.config.get('headless', True):
            options.add_argument("--headless")
            
        # User-Agent設定
        if self.config.get('user_agent'):
            options.add_argument(f"--user-agent={self.config['user_agent']}")
        
        # プロキシ設定
        if self.config.get('proxy'):
            options.add_argument(f"--proxy-server={self.config['proxy']}")
        
        # WebDriverの初期化
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # ウィンドウサイズ設定
        if self.config.get('window_size'):
            width, height = self.config['window_size']
            driver.set_window_size(width, height)
        
        # 待機時間設定
        driver.implicitly_wait(self.config.get('implicit_wait', 10))
        
        return driver
    
    def _get_element(self, selector: Dict, timeout: int = 10) -> Any:
        """要素を取得"""
        by = getattr(By, selector['by'].upper())
        value = selector['value']
        
        if timeout > 0:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        else:
            return self.driver.find_element(by, value)
    
    def _get_elements(self, selector: Dict) -> List[Any]:
        """複数要素を取得"""
        by = getattr(By, selector['by'].upper())
        value = selector['value']
        return self.driver.find_elements(by, value)
    
    def _wait_and_click(self, selector: Dict, timeout: int = 10) -> bool:
        """要素の出現を待ってクリック"""
        try:
            by = getattr(By, selector['by'].upper())
            value = selector['value']
            
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            return True
            
        except TimeoutException:
            self.logger.error(f"要素が見つかりません: {selector}")
            return False
    
    def _execute_action(self, action: Dict) -> bool:
        """アクションを実行"""
        try:
            action_type = action.get('type')
            
            if action_type == 'click':
                return self._wait_and_click(action['selector'], action.get('timeout', 10))
            
            elif action_type == 'input':
                element = self._get_element(action['selector'])
                element.clear()
                element.send_keys(action['value'])
                return True
            
            elif action_type == 'select':
                element = self._get_element(action['selector'])
                select = Select(element)
                
                if 'value' in action:
                    select.select_by_value(action['value'])
                elif 'text' in action:
                    select.select_by_visible_text(action['text'])
                elif 'index' in action:
                    select.select_by_index(action['index'])
                return True
            
            elif action_type == 'wait':
                time.sleep(action.get('seconds', 1))
                return True
            
            elif action_type == 'scroll':
                if 'selector' in action:
                    element = self._get_element(action['selector'])
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                else:
                    self.driver.execute_script(f"window.scrollTo(0, {action.get('pixels', 0)});")
                return True
            
            elif action_type == 'javascript':
                self.driver.execute_script(action['script'])
                return True
            
            elif action_type == 'hover':
                element = self._get_element(action['selector'])
                ActionChains(self.driver).move_to_element(element).perform()
                return True
            
            elif action_type == 'key_press':
                element = self._get_element(action['selector'])
                key = getattr(Keys, action['key'].upper())
                element.send_keys(key)
                return True
            
            else:
                self.logger.error(f"未知のアクションタイプ: {action_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"アクション実行エラー: {action}, エラー: {e}")
            return False
    
    def _extract_data_from_element(self, element, extractor: Dict) -> Any:
        """要素からデータを抽出"""
        extract_type = extractor.get('type', 'text')
        
        if extract_type == 'text':
            return element.get_text(strip=True) if hasattr(element, 'get_text') else element.text.strip()
        
        elif extract_type == 'attribute':
            attr_name = extractor.get('attribute')
            if hasattr(element, 'get'):
                return element.get(attr_name)
            else:
                return element.get_attribute(attr_name)
        
        elif extract_type == 'html':
            return str(element)
        
        elif extract_type == 'regex':
            text = element.get_text(strip=True) if hasattr(element, 'get_text') else element.text.strip()
            pattern = extractor.get('pattern')
            match = re.search(pattern, text)
            return match.group(1) if match and match.groups() else match.group(0) if match else None
        
        else:
            return element.get_text(strip=True) if hasattr(element, 'get_text') else element.text.strip()
    
    def _extract_page_data(self, extraction_config: Dict) -> List[Dict]:
        """ページからデータを抽出"""
        try:
            data = []
            
            # ページソース取得
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # 抽出方法によって分岐
            if 'items' in extraction_config:
                # リスト形式のデータ抽出
                item_selector = extraction_config['items']['selector']
                items = soup.select(item_selector)
                
                for item in items:
                    item_data = {}
                    
                    for field_name, field_config in extraction_config['items']['fields'].items():
                        try:
                            if 'selector' in field_config:
                                field_element = item.select_one(field_config['selector'])
                                if field_element:
                                    item_data[field_name] = self._extract_data_from_element(
                                        field_element, field_config
                                    )
                                else:
                                    item_data[field_name] = field_config.get('default', None)
                            else:
                                item_data[field_name] = self._extract_data_from_element(item, field_config)
                                
                        except Exception as e:
                            self.logger.warning(f"フィールド抽出エラー {field_name}: {e}")
                            item_data[field_name] = field_config.get('default', None)
                    
                    # データ加工
                    item_data['scraped_at'] = datetime.now().isoformat()
                    item_data['source_url'] = self.driver.current_url
                    
                    data.append(item_data)
            
            elif 'fields' in extraction_config:
                # 単一レコード形式のデータ抽出
                single_data = {}
                
                for field_name, field_config in extraction_config['fields'].items():
                    try:
                        element = soup.select_one(field_config['selector'])
                        if element:
                            single_data[field_name] = self._extract_data_from_element(element, field_config)
                        else:
                            single_data[field_name] = field_config.get('default', None)
                            
                    except Exception as e:
                        self.logger.warning(f"フィールド抽出エラー {field_name}: {e}")
                        single_data[field_name] = field_config.get('default', None)
                
                single_data['scraped_at'] = datetime.now().isoformat()
                single_data['source_url'] = self.driver.current_url
                
                data.append(single_data)
            
            self.logger.info(f"データ抽出完了: {len(data)}件")
            return data
            
        except Exception as e:
            self.logger.error(f"データ抽出エラー: {e}")
            return []
    
    def _save_data(self, data: List[Dict], output_config: Dict) -> bool:
        """データ保存"""
        try:
            if not data:
                self.logger.warning("保存するデータがありません")
                return False
            
            output_file = output_config.get('file', 'scraped_data.csv')
            output_format = output_config.get('format', 'csv').lower()
            
            # ファイル形式に応じて保存
            if output_format == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            elif output_format == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(output_file, index=False, encoding='utf-8')
            
            elif output_format == 'excel':
                df = pd.DataFrame(data)
                df.to_excel(output_file, index=False)
            
            else:
                self.logger.error(f"未対応の出力形式: {output_format}")
                return False
            
            self.logger.info(f"データ保存完了: {output_file} ({len(data)}件)")
            return True
            
        except Exception as e:
            self.logger.error(f"データ保存エラー: {e}")
            return False
    
    def scrape(self) -> bool:
        """メインスクレイピング処理"""
        try:
            self.logger.info("スクレイピング開始")
            
            # WebDriver初期化
            self.driver = self._setup_driver()
            
            # サイト設定取得
            sites = self.config.get('sites', [])
            
            for site_config in sites:
                self.logger.info(f"サイト処理開始: {site_config.get('name', 'Unknown')}")
                
                # サイトにアクセス
                url = site_config.get('url')
                if not url:
                    self.logger.error("URLが設定されていません")
                    continue
                
                self.driver.get(url)
                self.logger.info(f"アクセス: {url}")
                
                # 初期化待機
                time.sleep(site_config.get('initial_wait', 2))
                
                # アクション実行
                actions = site_config.get('actions', [])
                for action in actions:
                    if not self._execute_action(action):
                        self.logger.warning(f"アクション失敗: {action}")
                        if action.get('required', False):
                            self.logger.error("必須アクションが失敗しました")
                            return False
                    
                    # アクション間の待機
                    time.sleep(action.get('wait_after', 1))
                
                # データ抽出
                extraction_config = site_config.get('extraction')
                if extraction_config:
                    site_data = self._extract_page_data(extraction_config)
                    self.scraped_data.extend(site_data)
                
                # サイト間の待機
                time.sleep(site_config.get('wait_after', 2))
            
            # データ保存
            output_config = self.config.get('output', {})
            if self.scraped_data and not self._save_data(self.scraped_data, output_config):
                return False
            
            self.logger.info(f"スクレイピング完了: 総件数 {len(self.scraped_data)}件")
            return True
            
        except Exception as e:
            self.logger.error(f"スクレイピングエラー: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()


def load_config(config_file: str) -> Dict:
    """設定ファイル読み込み"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"設定ファイルが見つかりません: {config_file}")
        return {}
    except json.JSONDecodeError:
        print(f"設定ファイルの形式が正しくありません: {config_file}")
        return {}


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='汎用Webスクレイピングツール')
    parser.add_argument('--config', '-c', default='scraper_config.json', help='設定ファイルパス')
    parser.add_argument('--headless', action='store_true', help='ヘッドレスモード')
    parser.add_argument('--output', '-o', help='出力ファイル名')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='ログレベル')
    
    args = parser.parse_args()
    
    # 設定読み込み
    config = load_config(args.config)
    
    if not config:
        print("設定ファイルを作成してください。サンプル設定ファイルを参照してください。")
        return
    
    # コマンドライン引数で上書き
    if args.headless:
        config['headless'] = True
    if args.output:
        if 'output' not in config:
            config['output'] = {}
        config['output']['file'] = args.output
    if args.log_level:
        config['log_level'] = args.log_level
    
    # スクレイピング実行
    scraper = UniversalScraper(config)
    success = scraper.scrape()
    
    if success:
        print("スクレイピングが正常に完了しました")
    else:
        print("スクレイピングに失敗しました")
        exit(1)


if __name__ == "__main__":
    main() 
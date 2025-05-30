# Gorai プロジェクトコレクション

このリポジトリは、学習目的で作成された複数のツール・フレームワークを含むプロジェクトコレクションです。各プロジェクトは独立して動作し、異なる用途に対応しています。

## 📁 プロジェクト一覧

### 1. [NotionChatgpt](./NotionChatgpt/)
**Notion API プロキシサーバー**

NotionのページをChatGPTで検索・取得するためのシンプルなプロキシサーバーです。

- **技術スタック**: Node.js, Express
- **機能**:
  - Notionページのキーワード検索
  - 指定ページの本文取得
  - REST API エンドポイント提供

```bash
# セットアップ例
cd NotionChatgpt
npm install
cp env.example .env  # 環境変数設定
node server.js
```

### 2. [ProperNounFinder](./ProperNounFinder/)
**OpenAI API 固有名詞検出・置換ツール**

CSVファイル内のテキストから固有名詞を検出し、一般的な表現に置き換える処理を行います。

- **技術スタック**: Python, OpenAI API (GPT-4o)
- **機能**:
  - 固有名詞の自動検出
  - 一般的表現への置換
  - CSVバッチ処理
  - 詳細な判定理由記録

```bash
# セットアップ例
cd ProperNounFinder
pip install -r requirements.txt
cp config/env_template.txt .env  # APIキー設定
python scripts/main.py
```

### 3. [UniversalScraper](./UniversalScraper/)
**汎用Webスクレイピングフレームワーク**

JSONファイルによる設定ベースで、あらゆるWebサイトに対応可能なスクレイピングツールです。

- **技術スタック**: Python, Selenium, BeautifulSoup
- **機能**:
  - 設定ベースのスクレイピング
  - 複数フォーマット出力（CSV/JSON/Excel）
  - GUI設定生成
  - 多様なアクション（クリック、入力、スクロールなど）

```bash
# セットアップ例
cd UniversalScraper
pip install selenium webdriver-manager beautifulsoup4 pandas openpyxl
python config_generator.py  # 設定ファイル生成
python universal_scraper.py
```

## 🚀 クイックスタート

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd project
```

### 2. 各プロジェクトのセットアップ
各プロジェクトディレクトリに移動し、それぞれのREADMEに従ってセットアップを行ってください。

### 3. 必要な環境変数・設定ファイルの準備
- **NotionChatgpt**: Notion API Token
- **ProperNounFinder**: OpenAI API Key
- **UniversalScraper**: 設定ファイル（自動生成可能）

## 📋 システム要件

### NotionChatgpt
- Node.js 14.0以降
- npm または yarn

### ProperNounFinder
- Python 3.7以降
- OpenAI APIアカウント

### UniversalScraper
- Python 3.7以降
- Google Chrome ブラウザ

## 📊 各プロジェクトの詳細

| プロジェクト | 主な用途 | 技術 | API要件 |
|-------------|----------|------|---------|
| NotionChatgpt | Notion連携 | Node.js | Notion API |
| ProperNounFinder | テキスト処理 | Python | OpenAI API |
| UniversalScraper | データ収集 | Python | なし |

## ⚠️ 重要な注意事項

### 学習目的での作成
- **すべてのプロジェクトは学習目的で作成されています**
- **本格的な運用環境での使用は推奨しません**
- **セキュリティやエラーハンドリングが不十分な場合があります**

### API利用料金
- **NotionChatgpt**: Notion API（基本無料、制限あり）
- **ProperNounFinder**: OpenAI API（従量課金）
- **UniversalScraper**: 追加料金なし

### コントリビューション
- **コントリビューションやサポートは受け付けておりません**
- 参考目的での利用は自由ですが、商用利用は推奨しません

## 📝 ライセンス

このプロジェクトコレクション内のすべてのプロジェクトは学習目的で作成されており、個別のライセンス表記がない限り、同様の条件が適用されます。

## 🔗 関連リンク

- [Notion API Documentation](https://developers.notion.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)

---

各プロジェクトの詳細な使用方法については、それぞれのディレクトリ内のREADMEファイルをご確認ください。
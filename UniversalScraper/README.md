# 汎用Webスクレイピングフレームワーク

任意のWebサイトに対応可能な設定ベースのスクレイピングツールです。JSONファイルで設定を定義するだけで、プログラミング知識がなくても様々なWebサイトをスクレイピングできます。

## 🌟 特徴

- 🔧 **設定ベース**: JSONファイルで全ての設定を管理
- 🌐 **汎用性**: あらゆるWebサイトに対応可能
- 🎯 **柔軟なアクション**: クリック、入力、スクロール、JavaScript実行など
- 📊 **多様な抽出**: テキスト、属性、HTML、正規表現による抽出
- 💾 **複数フォーマット**: CSV、JSON、Excel形式での出力
- 🛡️ **堅牢性**: エラーハンドリングとリトライ機能
- 📝 **ログ**: 詳細な実行ログ
- 🎨 **GUI設定生成**: 対話形式での設定ファイル作成

## 📦 インストール

### 必要なライブラリをインストール

```bash
pip install selenium webdriver-manager beautifulsoup4 pandas openpyxl
```

### ChromeDriverの自動インストール
webdriver-managerが自動的にChromeDriverをダウンロード・設定します。

## 🚀 使用方法

### 基本的な実行

```bash
# デフォルト設定ファイルで実行
python universal_scraper.py

# 設定ファイルを指定して実行
python universal_scraper.py --config config_sample.json

# ヘッドレスモードを無効にして実行（ブラウザを表示）
python universal_scraper.py --config examples/ecommerce_demo.json --headless false
```

### 設定ファイル生成

```bash
# 対話形式で設定ファイルを作成
python config_generator.py
```

## 📋 設定ファイル構造

### 基本構造

```json
{
  "headless": true,
  "implicit_wait": 10,
  "log_level": "INFO",
  "user_agent": "Mozilla/5.0...",
  "output": {
    "file": "scraped_data.csv",
    "format": "csv"
  },
  "sites": [
    {
      "name": "サイト名",
      "url": "https://example.com",
      "actions": [...],
      "extraction": {...}
    }
  ]
}
```

### アクション設定

#### クリックアクション
```json
{
  "type": "click",
  "selector": {
    "by": "id",
    "value": "search-button"
  },
  "timeout": 10,
  "wait_after": 2,
  "required": false
}
```

#### 入力アクション
```json
{
  "type": "input",
  "selector": {
    "by": "css_selector",
    "value": "#search-box"
  },
  "value": "検索キーワード",
  "timeout": 10,
  "wait_after": 1
}
```

#### 選択アクション
```json
{
  "type": "select",
  "selector": {
    "by": "name",
    "value": "category"
  },
  "value": "books",
  "timeout": 10
}
```

#### 待機アクション
```json
{
  "type": "wait",
  "seconds": 3
}
```

#### スクロールアクション
```json
{
  "type": "scroll",
  "pixels": 1000
}
```

#### JavaScript実行
```json
{
  "type": "javascript",
  "script": "window.scrollTo(0, document.body.scrollHeight);"
}
```

### データ抽出設定

#### リスト形式の抽出
```json
{
  "extraction": {
    "items": {
      "selector": ".product-item",
      "fields": {
        "title": {
          "selector": ".product-title",
          "type": "text",
          "default": "タイトル不明"
        },
        "price": {
          "selector": ".price",
          "type": "text",
          "default": "価格不明"
        },
        "link": {
          "selector": "a",
          "type": "attribute",
          "attribute": "href",
          "default": ""
        }
      }
    }
  }
}
```

#### 単一レコード形式の抽出
```json
{
  "extraction": {
    "fields": {
      "page_title": {
        "selector": "h1",
        "type": "text"
      },
      "meta_description": {
        "selector": "meta[name='description']",
        "type": "attribute",
        "attribute": "content"
      }
    }
  }
}
```

## 📁 ファイル構成

```
.
├── universal_scraper.py      # メインスクレイピングツール
├── config_generator.py       # 設定ファイル生成ツール
├── config_sample.json        # サンプル設定ファイル
├── UNIVERSAL_README.md       # このファイル
├── examples/                 # 設定例
│   ├── ecommerce_demo.json
│   └── news_demo.json
└── output/                   # 出力ファイル
    ├── scraped_data.csv
    └── logs/
```

## 🔧 設定項目一覧

### グローバル設定

| 項目 | 説明 | デフォルト | 必須 |
|------|------|------------|------|
| `headless` | ヘッドレスモード | `true` | × |
| `implicit_wait` | 要素待機時間（秒） | `10` | × |
| `log_level` | ログレベル | `"INFO"` | × |
| `user_agent` | User-Agent文字列 | Chrome標準 | × |
| `window_size` | ウィンドウサイズ `[幅, 高さ]` | `null` | × |
| `proxy` | プロキシサーバー | `null` | × |
| `chrome_options` | Chrome追加オプション | `[]` | × |

### セレクタ指定方法

| by | 説明 | 例 |
|----|------|-----|
| `id` | ID属性 | `"search-button"` |
| `class_name` | クラス名 | `"btn-primary"` |
| `css_selector` | CSSセレクタ | `".product .title"` |
| `xpath` | XPath | `"//div[@class='item']"` |
| `tag_name` | タグ名 | `"button"` |
| `name` | name属性 | `"username"` |
| `link_text` | リンクテキスト | `"詳細を見る"` |
| `partial_link_text` | 部分リンクテキスト | `"詳細"` |

### 抽出タイプ

| type | 説明 | 追加設定 |
|------|------|----------|
| `text` | テキスト内容 | なし |
| `attribute` | 属性値 | `"attribute": "href"` |
| `html` | HTML文字列 | なし |
| `regex` | 正規表現抽出 | `"pattern": "価格: (\\d+)円"` |

## 🎯 使用例

### 1. ECサイト商品検索（デモ）

```bash
python universal_scraper.py --config examples/ecommerce_demo.json
```

商品のタイトル、価格、評価、リンクを抽出します。

### 2. ニュースサイト（デモ）

```bash
python universal_scraper.py --config examples/news_demo.json
```

ニュースサイトから記事情報を収集します。

### 3. カスタム設定

```bash
python universal_scraper.py --config config_sample.json
```

任意のWebサイトに合わせてカスタマイズした設定で実行します。

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. 要素が見つからない
```
ERROR: 要素が見つかりません: {'by': 'id', 'value': 'button-id'}
```
**解決方法:**
- セレクタが正しいか確認
- 要素の読み込みを待つためtimeoutを増やす
- ブラウザの開発者ツールでセレクタをテスト

#### 2. タイムアウトエラー
```
ERROR: TimeoutException
```
**解決方法:**
- `implicit_wait`を増やす
- `timeout`値を調整
- ネットワーク環境を確認

#### 3. データが抽出されない
```
WARNING: データ抽出完了: 0件
```
**解決方法:**
- CSSセレクタを確認
- ページの読み込み完了を待つ
- JavaScriptで動的に生成される要素の場合は適切な待機を追加

#### 4. ChromeDriverエラー
```
ERROR: ChromeDriverのバージョンが一致しません
```
**解決方法:**
```bash
pip install --upgrade webdriver-manager
```

## 📞 使用について

このツールは現状のまま提供されます。サポートやコントリビューションは受け付けておりません。
使用に関する質問や問題については、ご自身で解決していただくか、関連する技術文書をご参照ください。

## ⚖️ 免責事項

このソフトウェアは教育目的および研究目的で提供されています。使用者は以下の点について十分理解し、自己責任で使用してください：

### 使用者の責任
- **法的責任**: 各国の法律、対象サイトの利用規約、robots.txtの遵守は使用者の責任です
- **倫理的責任**: サーバーへの負荷軽減、適切なアクセス間隔の設定は使用者が行ってください
- **データ責任**: 取得したデータの利用、保存、配布に関する責任は使用者にあります
- **損害責任**: 本ツールの使用により生じた一切の損害について、開発者は責任を負いません

### 禁止事項
- 対象サイトの利用規約に違反する行為
- 過度なアクセスによるサーバー負荷の発生
- 個人情報や機密情報の不正取得
- 著作権を侵害するデータの取得・配布
- 商用利用における適切な許可の未取得

### 推奨事項
- 事前に対象サイトの利用規約とrobots.txtを確認
- 適切なアクセス間隔（1秒以上）を設定
- 取得データの用途を明確化
- 必要に応じて対象サイト運営者への事前連絡

**本ツールを使用することで、上記の免責事項に同意したものとみなします。**

## 🆕 更新履歴

- v1.0.0: 初回リリース
  - 汎用スクレイピングフレームワーク
  - 設定ファイル生成ツール
  - 複数フォーマット出力対応
  - 豊富なアクション・抽出機能 
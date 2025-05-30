# Notion ChatGPT Proxy

NotionのページをChatGPTで検索・取得するためのシンプルなプロキシサーバーです。学習目的で作成されました。

## 機能

- Notionページをキーワードで検索
- 指定したページの本文を取得

## セットアップ

### 1. 依存関係のインストール

```bash
npm install
```

### 2. 環境変数の設定

`env.example`ファイルを参考に`.env`ファイルを作成してください：

```bash
cp env.example .env
```

`.env`ファイルに以下の情報を設定：

- `NOTION_TOKEN`: Notion API Integration Token
- `PORT`: サーバーのポート番号（デフォルト: 3000）

### 3. Notion API Tokenの取得

1. [Notion Developers](https://developers.notion.com/)にアクセス
2. 新しいIntegrationを作成
3. Generated Tokenをコピーして`.env`ファイルに設定
4. 検索したいNotionページでIntegrationに権限を付与

### 4. サーバーの起動

```bash
node server.js
```

## API エンドポイント

### GET /search?q={キーワード}

Notionページをキーワードで検索します。

```bash
curl "http://localhost:3000/search?q=検索したいキーワード"
```

### GET /page/{ページID}

指定したページの本文を取得します。

```bash
curl "http://localhost:3000/page/{ページID}"
```

## 注意事項

- このプロジェクトは学習目的で作成されました
- 本格的な運用には適していません
- セキュリティやエラーハンドリングが不十分な場合があります

## ライセンス

このプロジェクトは学習目的で作成されており、**コントリビューションやサポートは受け付けておりません**。

参考目的での利用は自由ですが、商用利用や本格的な運用は推奨しません。 
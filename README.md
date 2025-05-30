# GORAi プロジェクトコレクション

このリポジトリは、AI・自動化・知識管理などの様々な領域をカバーする、学習・実験・創作目的のプロジェクトコレクションです。各プロジェクトは独立して動作し、異なる用途と学習目標に対応しています。

## 📁 プロジェクト一覧

### 🤖 AIアシスタント・チャットボット

#### [TONARiAi](./TONARiAi/)
**ChatGPT カスタムGPTsコレクション**

業務特化型のChatGPTカスタムボット（GPTs）を体系的に整理したポートフォリオです。

- **技術スタック**: ChatGPT API, カスタムGPTs
- **機能**:
  - 部門別業務特化AIボット（ロビー、社長室、バックオフィス等）
  - 専門領域AI（法務、人事、コンサル、開発、教育等）
  - クリエイティブAI（作曲、イラスト、抽象画等）
  - 90以上の専門ボットへのアクセスリンク

```bash
# 利用例
# 各GPTsは ChatGPT アカウントでリンクアクセスして利用
# 詳細は GPTs.md を参照
```

### 🔧 開発・自動化ツール

#### [NotionChatgpt](./NotionChatgpt/)
**Notion API プロキシサーバー**

NotionのページをChatGPTで検索・取得するためのシンプルなプロキシサーバーです。

- **技術スタック**: Node.js, Express
- **機能**:
  - Notionページのキーワード検索
  - 指定ページの本文取得
  - REST API エンドポイント提供

#### [ProperNounFinder](./ProperNounFinder/)
**OpenAI API 固有名詞検出・置換ツール**

CSVファイル内のテキストから固有名詞を検出し、一般的な表現に置き換える処理を行います。

- **技術スタック**: Python, OpenAI API (GPT-4o)
- **機能**:
  - 固有名詞の自動検出
  - 一般的表現への置換
  - CSVバッチ処理
  - 詳細な判定理由記録

#### [UniversalScraper](./UniversalScraper/)
**汎用Webスクレイピングフレームワーク**

JSONファイルによる設定ベースで、あらゆるWebサイトに対応可能なスクレイピングツールです。

- **技術スタック**: Python, Selenium, BeautifulSoup
- **機能**:
  - 設定ベースのスクレイピング
  - 複数フォーマット出力（CSV/JSON/Excel）
  - GUI設定生成
  - 多様なアクション（クリック、入力、スクロールなど）

### 📝 コンテンツ・ナレッジベース

#### [KAKiMONO](./KAKiMONO/)
**日次記録・学習ノートアーカイブ**

日々の学習内容、技術検証、アイデア整理を時系列で記録したマークダウンアーカイブです。

- **内容**: 2024年11月〜2025年2月の約100日分の記録
- **テーマ**: 
  - 技術検証と実装記録
  - 起業・ビジネス戦略の考察
  - AI・データサイエンスの学習記録
  - プロジェクト進捗と振り返り

- **最新記事例**: 
  - サム・アルトマンとスティーブ・ジョブズに学ぶ起業成功マニュアル
  - AI技術の実装と検証記録
  - データ分析手法の比較検討

#### [BookShelf](./BookShelf/)
**デジタル書籍コレクション**

学習・研究・趣味で読んだ書籍のデジタル本棚です。

- **カテゴリー**:
  - AI・データサイエンス（40冊以上）
  - 株式投資・トレード
  - 学術・理論書
  - 小説・文学
  - 技術・ノウハウ本

- **特徴**: Amazonアソシエイトリンク付きの整理済みリスト

#### [ArtGallery](./ArtGallery/)
**デジタルアート作品集**

AI生成やデジタル創作による抽象画・イラスト作品のコレクションです。

- **作品数**: 40点以上のPNG画像
- **テーマ**: 
  - 抽象的概念の視覚化
  - 技術・ビジネス概念のアート表現
  - 創作的データ可視化
  - 哲学的テーマの表現

- **代表作品**: 
  - 統計と直感の二重螺旋
  - AIの予測変換
  - 色によるデータ分類
  - 孤独でアイデア

#### [Sample](./Sample/)
**テンプレート・サンプル文書**

各種サービス・アプリケーション開発で使用する定型文書のテンプレート集です。

- **内容**:
  - プライバシーポリシーサンプル
  - 利用規約サンプル
  - その他法務・運営文書テンプレート

## 📊 各プロジェクトの詳細

| プロジェクト | 主な用途 | 技術 | API要件 |
|-------------|----------|------|---------|
| TONARiAi | ChatGPT活用 | GPTs | ChatGPT Account |
| NotionChatgpt | Notion連携 | Node.js | Notion API |
| ProperNounFinder | テキスト処理 | Python | OpenAI API |
| UniversalScraper | データ収集 | Python | なし |
| KAKiMONO | 知識管理 | Markdown | なし |
| BookShelf | 読書管理 | Markdown | なし |
| ArtGallery | 作品展示 | 画像ファイル | なし |
| Sample | テンプレート | 文書 | なし |

## 📋 システム要件

### 開発ツール系
- **Node.js** 14.0以降（NotionChatgpt）
- **Python** 3.7以降（ProperNounFinder, UniversalScraper）
- **Google Chrome** ブラウザ（UniversalScraper）

### AIサービス系
- **ChatGPT アカウント**（TONARiAi）
- **OpenAI APIアカウント**（ProperNounFinder）
- **Notion APIアカウント**（NotionChatgpt）

### コンテンツ系
- **Markdownビューアー**（KAKiMONO, BookShelf）
- **画像ビューアー**（ArtGallery）

## ⚠️ 重要な注意事項

### 学習・実験目的での作成
- **すべてのプロジェクトは学習・実験目的で作成されています**
- **本格的な運用環境での使用は推奨しません**
- **セキュリティやエラーハンドリングが不十分な場合があります**

### API利用料金
- **TONARiAi**: ChatGPT Plus（月額20ドル推奨）
- **NotionChatgpt**: Notion API（基本無料、制限あり）
- **ProperNounFinder**: OpenAI API（従量課金）
- **UniversalScraper**: 追加料金なし

### コンテンツ利用について
- **KAKiMONO**: 個人の学習記録のため、内容の正確性は保証されません
- **BookShelf**: Amazonアソシエイトリンクが含まれます
- **ArtGallery**: AI生成作品を含むため、商用利用は要確認

### コントリビューション
- **コントリビューションやサポートは受け付けておりません**
- 参考目的での利用は自由ですが、商用利用は推奨しません

## 📝 ライセンス

このプロジェクトコレクション内のすべてのプロジェクトは学習・実験目的で作成されており、個別のライセンス表記がない限り、同様の条件が適用されます。

## 🔗 関連リンク

- [Notion API Documentation](https://developers.notion.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [ChatGPT GPTs](https://openai.com/gpts)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)

---

各プロジェクトの詳細な使用方法については、それぞれのディレクトリ内のREADMEファイルをご確認ください。コンテンツ系プロジェクト（KAKiMONO、BookShelf、ArtGallery）は、知識共有・学習記録・創作活動の参考としてご活用ください。
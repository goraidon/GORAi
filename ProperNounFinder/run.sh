#!/bin/bash

# OpenAI API 固有名詞検出・置換ツール実行スクリプト

echo "=== OpenAI API 固有名詞検出・置換ツール ==="
echo ""

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

# .envファイルの存在確認
if [ ! -f ".env" ]; then
    echo "⚠️  .envファイルが見つかりません。"
    echo "config/env_template.txtを参考に.envファイルを作成してください。"
    echo ""
    echo "手順:"
    echo "1. cp config/env_template.txt .env"
    echo "2. .envファイルを編集してOpenAI APIキーを設定"
    exit 1
fi

# 依存関係のインストール確認
echo "📦 依存関係を確認中..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 依存関係の確認完了"
else
    echo "❌ 依存関係のインストールに失敗しました"
    echo "手動で以下を実行してください:"
    echo "pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "🚀 処理を開始します..."
echo ""

# メインスクリプト実行
python scripts/main.py

echo ""
echo "🎉 処理が完了しました！"
echo "結果はoutput/ディレクトリを確認してください。" 
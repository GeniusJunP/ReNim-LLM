# ReNim LLM Helper

BlenderのReNimアドオン用のボーンマッピング支援ツール。LLMを使って自動的にボーン対応を生成します。

## 機能

- ReNimノードからボーン情報を抽出
- LLM用のプロンプトを自動生成
- ChatGPT/Claudeでボーンマッピングを生成

## インストール

1. `ReNim-LLM-Helper.py`をダウンロード
2. Blenderのテキストエディタで開く
3. 実行ボタンを押す

## 使い方

1. **ReNimノードを選択**
2. **ソース・ターゲットアーマチュアを設定**
3. **"Generate LLM Prompt"ボタンをクリック**
4. **ChatGPT/Claudeに貼り付け**
5. **生成されたJSONをReNimで使用**

## 環境

- **Blender**: 3.0以上
- [**ReNim Node**](https://github.com/anasrar/ReNim)
- **Python**: 3.11（Blender内蔵）

## 出力例

```json
{
  "mappings": [
    {"source": "Hips", "target": "hips"},
    {"source": "Spine", "target": "spine"},
    {"source": "LeftArm", "target": "left_arm"}
  ]
}
```

## ライセンス
MIT License
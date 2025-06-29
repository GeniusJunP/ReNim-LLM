# ReNim LLM Helper

ReNimアドオン用のLLMアシスタントツール。ボーンマッピングの自動化を支援します。

## インストール

1. `ReNim-LLM-Helper.py`をダウンロード
2. Blenderを開き、`編集` > `プリファレンス` > `アドオン` に移動
3. `インストール...` ボタンを押し、ダウンロードした `ReNim-LLM-Helper.py` を選択
4. `ReNim LLM Helper` を検索し、チェックボックスをオンにしてアドオンを有効化

## 使い方

### 完全ワークフロー

1. **ReNimノードエディタを開く**
   - エディタタイプを `Retarget Animation Node` に変更

2. **Target and Source Objectノードを追加**
   - `Shift+A` > `Object` > `Target and Source Object`
   - SourceとTargetアーマチュアを設定

3. **LLMプロンプトを生成**
   - ノードを選択した状態で、右パネル（Nキー）の **ReNim Tools** タブを開く
   - `Generate LLM Prompt`ボタンをクリック（クリップボードにコピーされます）

4. **LLMでボーンマッピングを取得**
   - ChatGPT、Claude等のLLMにプロンプトを貼り付け
   - 返答のJSONをコピー

5. **LLM出力をReNimプリセットに変換**
   - `Convert LLM Output to Preset`ボタンをクリック
   - LLMのJSONレスポンスを貼り付け
   - ファイル名を設定してOK

6. **ReNimでプリセットをインポート**
   - ReNimパネルでプリセットファイルを読み込み
   - ボーンマッピングが自動的に適用されます

## 機能

- **LLMプロンプト生成**: ソース・ターゲットのボーン情報を含む完全なプロンプトを生成
- **プリセット変換**: LLM出力をReNimが読み込めるプリセット形式に変換
- **統合ワークフロー**: ReNimノードエディタ内で完結する使いやすいUI

## 対応LLM

- ChatGPT (GPT-3.5, GPT-4)
- Claude (Anthropic)
- その他のJSON出力対応LLM

## 出力形式

LLMは以下の形式でJSONを出力します：

```json
{
  "mappings": [
    {"source": "ソースボーン名", "target": "ターゲットボーン名"},
    {"source": "mixamorig:Hips", "target": "root"},
    ...
  ]
}
```

## パネル位置

**ノードエディタ** > **ReNim Tools** タブ > **ReNim LLM Helper** パネル

## 要件

- Blender 3.0以上
- ReNimアドオン（インストール済み）
- LLMアクセス（ChatGPT、Claude等）

## トラブルシューティング

**パネルが見つからない場合:**
- ReNimアドオンがインストール・有効化されているか確認
- ノードエディタの種類が **Retarget Animation Node** になっているか確認
- **Target and Source Object** ノードが選択されているか確認

**プリセットが読み込めない場合:**
- 生成されたJSONファイルがBlendファイルと同じフォルダにあるか確認
- ReNimのプリセット読み込み機能を使用してファイルを指定

**LLM出力が変換できない場合:**
- LLMの出力が正しいJSON形式になっているか確認
- `"mappings"` 配列が含まれているか確認

## 開発環境

Python venv環境でのBlenderアドオン開発：

```bash
# Blender内蔵Pythonでvenv作成
/Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.11 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# fake-bpy-moduleをインストール
pip install fake-bpy-module-4.2
```

VS Code設定（`.vscode/settings.json`）:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

## ライセンス

MIT License

# ReNim-LLM-Helper

[ReNim Node](https://github.com/anasrar/ReNim)用のLLMアシスタントツールです。既存モデル同士のボーンマッピングを半自動化します. 
Vibeで書いたコードです（GitHub Copilot）なぜかテキストボックスが実装できないので、クリップボードを読みます。Blenderのアドオン周りよくわからない

## インストール

1. `ReNim-LLM-Helper.py`をダウンロード
2. Blenderを開き、`編集` > `プリファレンス` > `アドオン` に移動
3. `インストール...` ボタンを押し、ダウンロードした `ReNim-LLM-Helper.py` を選択
4. `ReNim LLM Helper` を検索し、チェックボックスをオンにしてアドオンを有効化

## 使い方

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
   - ダイアログが表示されます
   - LLMのJSONをクリップボードにコピー済みであることを確認
   - ~~プリセットファイル名を設定（デフォルト: llm_bone_mapping）~~
   - OKをクリックして変換実行

6. **ReNimでプリセットをインポート**
   - ReNim側で生成されたプリセットファイルを読み込み
   - ボーンマッピングが自動的に適用されます
   - Node Wrangler等で一括でノードを接続すれば手間なし

## 出力形式

LLMは以下の形式でJSONを出力します：

```json
{
  "mappings": [
    {"source": "ソースボーン名", "target": "ターゲットボーン名"},
    {"source": "mixamorig:Hips", "target": "root"},
    ....
  ]
}
```

## パネル位置

**ノードエディタ** > **ReNim Tools** タブ > **ReNim LLM Helper** パネル

## 要件

- **Blender 2.80以上** (クリップボードアクセス機能のため)
- **推奨: Blender 3.0以上** (最適なパフォーマンスのため)
- **ReNimアドオン** (インストール済み)
- **LLM** (ChatGPT、Claude等)

## ライセンス

MIT License

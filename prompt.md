以下のボーンリストから、意味に基づいてソースとターゲットのボーンを対応付けてください。
出力形式は次のようなJSONにしてください：

{{
  "mappings": [
    {{"source": "Hips", "target": "hips"}},
    {{"source": "Spine", "target": "spine"}},
    ...
  ]
}}

ソースリグ: {source_rig_name}
ターゲットリグ: {target_rig_name}

入力データ:
{json.dumps(bone_data, indent=2, ensure_ascii=False)}

注意事項:
- 解剖学的に類似したボーン同士をマッピングしてください
- 完全に一致する名前がない場合は、最も近い意味のボーンを選択してください
- ソースにあってターゲットにないボーンは省略してください
- 左右(Left/Right, L/R, .L/.R等)の区別に注意してください
- 一般的なボーン命名規則を考慮してください（mixamo, rigify, etc.）
- 階層構造も考慮して親子関係を保ってください
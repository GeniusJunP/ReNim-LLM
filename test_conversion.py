#!/usr/bin/env python3
"""
LLM出力からReNimプリセット形式への変換をテストするスクリプト
"""

import json
import os

def convert_llm_mapping_to_renim_preset(mappings_json):
    """LLMの出力JSONをReNimプリセット形式に変換"""
    try:
        # JSON文字列をパース
        if isinstance(mappings_json, str):
            data = json.loads(mappings_json)
        else:
            data = mappings_json
            
        if "mappings" not in data:
            return None
            
        mappings = data["mappings"]
        
        # ReNimプリセット形式のJSONを生成
        preset_data = {
            "version": [0, 0, 1],
            "nodes": {}
        }
        
        # ボーンマッピングノードを作成
        for i, mapping in enumerate(mappings):
            node_name = f"BoneMapping_{i:03d}"
            preset_data["nodes"][node_name] = {
                "type": "ReNimNodeMappingBone",
                "label": f"{mapping['source']} -> {mapping['target']}",
                "location": [i * 50, -i * 100],  # ノードを縦に並べる
                "width": 300,
                "height": 100,
                "hide": False,
                "parent": None,
                "bone_target": mapping["target"],
                "bone_source": mapping["source"],
                
                # デフォルト設定
                "use_location": True,
                "location_axis": [True, True, True],
                "location_influence": [1.0, 1.0, 1.0],
                "location_multiply": [1.0, 1.0, 1.0],
                "location_offset": [0.0, 0.0, 0.0],
                
                "use_rotation_euler": True,
                "rotation_euler_axis": [True, True, True],
                "rotation_euler_influence": [1.0, 1.0, 1.0],
                "rotation_euler_multiply": [1.0, 1.0, 1.0],
                "rotation_euler_offset": [0.0, 0.0, 0.0],
                
                "use_scale": True,
                "scale_axis": [True, True, True],
                "scale_influence": [1.0, 1.0, 1.0],
                "scale_multiply": [1.0, 1.0, 1.0],
                "scale_offset": [0.0, 0.0, 0.0],
                
                "mix_mode": "AFTER"
            }
        
        return preset_data
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error converting LLM mapping: {e}")
        return None

def main():
    # example.jsonを読み込み
    with open('example.json', 'r', encoding='utf-8') as f:
        llm_output = json.load(f)
    
    print("LLM出力（元のデータ）:")
    print(json.dumps(llm_output, indent=2, ensure_ascii=False))
    print("\n" + "="*50 + "\n")
    
    # ReNimプリセット形式に変換
    preset_data = convert_llm_mapping_to_renim_preset(llm_output)
    
    if preset_data:
        print("ReNimプリセット形式（変換後）:")
        print(json.dumps(preset_data, indent=2, ensure_ascii=False))
        
        # 変換結果をファイルに保存
        with open('converted_preset.json', 'w', encoding='utf-8') as f:
            json.dump(preset_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n変換完了！ 結果は 'converted_preset.json' に保存されました。")
        print(f"ノード数: {len(preset_data['nodes'])}")
        
        # 各ノードの情報を表示
        print("\n生成されたノード:")
        for node_name, node_data in preset_data["nodes"].items():
            print(f"  {node_name}: {node_data['label']}")
            
    else:
        print("変換に失敗しました。")

if __name__ == "__main__":
    main()

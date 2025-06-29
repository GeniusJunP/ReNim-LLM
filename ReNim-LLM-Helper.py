bl_info = {
    "name": "ReNim LLM Helper",
    "author": "AI Assistant (Gemini)",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "Node Editor > Sidebar (N key) > ReNim Tools",
    "description": "Generates a bone list JSON for LLM from the active ReNim Node",
    "category": "Node",
}

import bpy
import json

def generate_llm_prompt_template(source_rig_name, target_rig_name, bone_data):
    """LLM用のプロンプトテンプレートを生成"""
    return f"""以下のボーンリストから、意味に基づいてソースとターゲットのボーンを対応付けてください。
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
- 階層構造も考慮して親子関係を保ってください"""

def convert_llm_mapping_to_renim_preset(mappings_json, node_source_target):
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

class RENIM_OT_convert_llm_to_preset(bpy.types.Operator):
    """Convert LLM output JSON to ReNim preset format"""
    bl_label = "Convert LLM Output to ReNim Preset"
    bl_idname = "renim.convert_llm_to_preset"
    
    # プロパティ
    llm_json_text = bpy.props.StringProperty(
        name="LLM Output JSON",
        description="Paste the LLM output JSON here",
        default="",
        maxlen=10000
    )
    
    preset_filename = bpy.props.StringProperty(
        name="Preset Filename",
        description="Name for the preset file (without extension)",
        default="llm_bone_mapping"
    )

    def execute(self, context):
        if not self.llm_json_text:
            self.report({'ERROR'}, "Please paste LLM output JSON")
            return {'CANCELLED'}
        
        try:
            # LLM出力をReNimプリセット形式に変換
            preset_data = convert_llm_mapping_to_renim_preset(self.llm_json_text)
            
            if not preset_data:
                self.report({'ERROR'}, "Failed to convert LLM output to preset format")
                return {'CANCELLED'}
            
            # ファイルパス設定
            import os
            filename = self.preset_filename + ".json"
            file_path = os.path.join(bpy.path.abspath("//"), filename)
            
            # プリセット保存
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(preset_data, f, indent=2, ensure_ascii=False)
            
            self.report({'INFO'}, f"Preset saved to: {filename} ({len(preset_data['nodes'])} nodes)")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error converting LLM output: {str(e)}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Convert LLM Output to ReNim Preset:")
        layout.prop(self, "llm_json_text", text="")
        layout.prop(self, "preset_filename")
        
        box = layout.box()
        box.label(text="Instructions:", icon='INFO')
        box.label(text="1. Get LLM output JSON with bone mappings")
        box.label(text="2. Paste it in the text field above")
        box.label(text="3. Set filename and click OK")
        box.label(text="4. Import the generated preset in ReNim")

class RENIM_OT_generate_json(bpy.types.Operator):
    """Generates and copies a complete LLM prompt for bone mapping from the active ReNim node"""
    bl_label = "Generate LLM Prompt for Bone Mapping"
    bl_idname = "renim.generate_json_for_llm"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.node_tree and context.active_node:
            # ReNimのオブジェクトノード（Target and Source Object）をチェック
            return context.active_node.bl_idname == 'ReNimNodeObjectSourceTarget'
        return False

    def execute(self, context):
        node = context.active_node

        # ReNimノードのソケットからアーマチュアオブジェクトを取得
        socket = node.outputs[0]
        source_arm = socket.source_object
        target_arm = socket.target_object

        if not source_arm or not target_arm:
            self.report({'WARNING'}, "Please select both Source and Target armatures in the node.")
            return {'CANCELLED'}

        # アーマチュアタイプかチェック
        if source_arm.type != 'ARMATURE' or target_arm.type != 'ARMATURE':
            self.report({'WARNING'}, "Both Source and Target must be Armature objects.")
            return {'CANCELLED'}

        # ボーン名リストを取得
        source_bones = [bone.name for bone in source_arm.data.bones]
        target_bones = [bone.name for bone in target_arm.data.bones]
        
        # LLM用の完全なプロンプトを生成
        bone_data = {
            "source_rig": source_arm.name,
            "source_bones": source_bones,
            "target_rig": target_arm.name,
            "target_bones": target_bones
        }
        
        # プロンプトテンプレートを作成
        prompt_template = generate_llm_prompt_template(
            source_arm.name, 
            target_arm.name, 
            bone_data
        )

        # クリップボードにコピー
        context.window_manager.clipboard = prompt_template

        self.report({'INFO'}, f"LLM prompt for '{source_arm.name}' -> '{target_arm.name}' copied to clipboard.")
        
        return {'FINISHED'}

class RENIM_PT_llm_helper_panel(bpy.types.Panel):
    """Creates a Panel in the Node Editor's Sidebar"""
    bl_label = "ReNim LLM Helper"
    bl_idname = "NODE_PT_renim_llm_helper"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    # ReNim Nodeと同じカテゴリにパネルを表示
    bl_category = "ReNim Tools"

    # パネルを表示するコンテキストを指定
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ReNimNode'

    def draw(self, context):
        layout = self.layout
        node = context.active_node
        
        if node and node.bl_idname == 'ReNimNodeObjectSourceTarget':
            col = layout.column(align=True)
            box = col.box()
            box.label(text="Active ReNim Node:")
            
            # ReNimのソケットプロパティを表示
            socket = node.outputs[0]
            box.prop(socket, "source_object", text="Source")
            box.prop(socket, "target_object", text="Target")
            
            col.separator()
            
            # プロンプト生成ボタン
            col.operator(RENIM_OT_generate_json.bl_idname, icon='COPYDOWN', text="Generate LLM Prompt")
            
            col.separator()
            
            # LLM出力変換ボタン
            col.operator(RENIM_OT_convert_llm_to_preset.bl_idname, icon='IMPORT', text="Convert LLM Output to Preset")
            
            # ヘルプテキスト
            help_box = col.box()
            help_box.scale_y = 0.8
            help_box.label(text="Workflow:")
            help_box.label(text="1. Generate LLM prompt")
            help_box.label(text="2. Use prompt with LLM")
            help_box.label(text="3. Convert LLM output to preset")
            help_box.label(text="4. Import preset in ReNim")
        else:
            layout.label(text="Select a ReNim 'Target and Source Object' node.")

def register():
    bpy.utils.register_class(RENIM_OT_generate_json)
    bpy.utils.register_class(RENIM_OT_convert_llm_to_preset)
    bpy.utils.register_class(RENIM_PT_llm_helper_panel)

def unregister():
    bpy.utils.unregister_class(RENIM_OT_generate_json)
    bpy.utils.unregister_class(RENIM_OT_convert_llm_to_preset)
    bpy.utils.unregister_class(RENIM_PT_llm_helper_panel)

if __name__ == "__main__":
    register()
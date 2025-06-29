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

class RENIM_OT_generate_json(bpy.types.Operator):
    """Generates and copies a complete LLM prompt for bone mapping from the active ReNim node"""
    bl_label = "Generate LLM Prompt for Bone Mapping"
    bl_idname = "renim.generate_json_for_llm"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.node_tree and context.active_node:
            # ReNimノードのID名が 'RENIM_OT_retarget_animation' であることを確認
            return hasattr(context.active_node.bl_rna, 'source_armature')
        return False

    def execute(self, context):
        node = context.active_node

        source_arm = node.source_armature
        target_arm = node.target_armature

        if not source_arm or not target_arm:
            self.report({'WARNING'}, "Please select both Source and Target armatures in the node.")
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
        return context.space_data.tree_type == 'ReNimRetargetTreeType'

    def draw(self, context):
        layout = self.layout
        node = context.active_node
        
        if node and hasattr(node.bl_rna, 'source_armature'):
            col = layout.column(align=True)
            box = col.box()
            box.label(text="Active ReNim Node:")
            box.prop(node, "source_armature", text="Source")
            box.prop(node, "target_armature", text="Target")
            
            col.separator()
            
            col.operator(RENIM_OT_generate_json.bl_idname, icon='COPYDOWN', text="Generate LLM Prompt")
            
            # ヘルプテキスト
            help_box = col.box()
            help_box.scale_y = 0.8
            help_box.label(text="Usage:")
            help_box.label(text="1. Click button to copy prompt")
            help_box.label(text="2. Paste to LLM (ChatGPT/Claude)")
            help_box.label(text="3. Get bone mapping JSON")
        else:
            layout.label(text="Select a ReNim node to begin.")

def register():
    bpy.utils.register_class(RENIM_OT_generate_json)
    bpy.utils.register_class(RENIM_PT_llm_helper_panel)

def unregister():
    bpy.utils.unregister_class(RENIM_OT_generate_json)
    bpy.utils.unregister_class(RENIM_PT_llm_helper_panel)

if __name__ == "__main__":
    register()
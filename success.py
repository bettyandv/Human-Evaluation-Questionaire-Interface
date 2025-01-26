# import gradio as gr
# import json
# import pickle

# with open('dialogues.pkl', 'rb') as f:
#     questions = pickle.load(f)
    
# metadata = questions[10]['metadata']
# evaluation = questions[10]['evaluation_result']
# # "scenario_consistency": {
# #                     "location": True,
# #                     "context": True,
# #                     "conversation_context_type": True,
# #                     "main_topic": True,
# #                     "goal_alignment": True,
# #                     "role_nationality": True,
# #                     "overall_scenario_consistency_score": 5
# #                 }
# scenario_consistency = evaluation['consistency']['scenario_consistency']

# def update(variables: dict):
#     for k,v in variables.items():
#         scenario_consistency[k] = variables[k]
        
#     return scenario_consistency

# consist_interface = [
#     gr.Checkbox(label="location", value=True),
#     gr.Checkbox(label="context", value=True),
#     gr.Checkbox(label="conversation_context_type", value=True),
#     gr.Checkbox(label="main_topic", value=True),
#     gr.Checkbox(label="goal_alignment", value=True),
#     gr.Checkbox(label="role_nationality", value=True),
#     gr.Dropdown([1, 2, 3, 4, 5], label="overall_scenario_consistency_score")
# ]

# demo = gr.Interface(
#             update(consist_interface),
#             consist_interface,
#             gr.textbox(label="Final result", interactive=False)

# )

# demo.launch()


# with open('dialogues.pkl', 'wb') as f:
#         pickle.dump(questions, f)
        
# print('question saved into pkl')


import gradio as gr
import json
import pickle

# 加载数据
with open('dialogues.pkl', 'rb') as f:
    questions = pickle.load(f)

metadata = questions[10]['metadata']
evaluation = questions[10]['evaluation_result']

# scenario_consistency 是我们需要更新的字典
scenario_consistency = evaluation['consistency']['scenario_consistency']

# 更新字典的函数
def update(variables: dict):
    # 根据用户选择更新字典中的值
    for k, v in variables.items():
        if isinstance(v, bool):  # 对于勾选框，设置为布尔值
            scenario_consistency[k] = v
        elif isinstance(v, int):  # 对于评分（Dropdown），设置为整数值
            scenario_consistency[k] = v

    return json.dumps(scenario_consistency, indent=4)  # 返回格式化后的结果以便展示

# 界面组件定义
consist_interface = [
    gr.Checkbox(label="location", value=scenario_consistency.get("location", True)),
    gr.Checkbox(label="context", value=scenario_consistency.get("context", True)),
    gr.Checkbox(label="conversation_context_type", value=scenario_consistency.get("conversation_context_type", True)),
    gr.Checkbox(label="main_topic", value=scenario_consistency.get("main_topic", True)),
    gr.Checkbox(label="goal_alignment", value=scenario_consistency.get("goal_alignment", True)),
    gr.Checkbox(label="role_nationality", value=scenario_consistency.get("role_nationality", True)),
    gr.Dropdown([1, 2, 3, 4, 5], label="overall_scenario_consistency_score", value=scenario_consistency.get("overall_scenario_consistency_score", 5))
]

# 创建 Gradio 界面
demo = gr.Interface(
    fn=update,  # 使用更新函数
    inputs=consist_interface,  # 输入组件
    outputs=gr.Textbox(label="Final result", interactive=False)  # 输出更新后的结果
)

# 启动 Gradio 界面
demo.launch()

# 保存更新后的 questions 数据
with open('dialogues.pkl', 'wb') as f:
    pickle.dump(questions, f)

print('question saved into pkl')

import gradio as gr
import json
import pickle
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dialogue_file",
    type=str,
    default="dialogues.pkl",
    help="Path to the dialogue file",
)
parser.add_argument(
    "--output_path",
    type=str,
    default="./eval/",
)

args = parser.parse_args()
os.makedirs(args.output_path, exist_ok=True)


with open(args.dialogue_file, "rb") as f:
    questions = pickle.load(f)

import gradio as gr
import pickle
import copy

with open("dialogues.pkl", "rb") as f:
    questions = pickle.load(f)


def create_eval_form():

    eval_forms = []

    for index, item in enumerate(questions):
        # Add unique ID and evaluation tag
        eval_form = {}
        eval_form["id"] = index
        eval_form["evaluation_tag"] = False

        # Build evaluation_result
        conversation_length = len(item["conversation"]["conversation"])
        evaluation_result = {
            "consistency": {
                "scenario_consistency": {
                    "location": True,
                    "context": True,
                    "conversation_context_type": True,
                    "main_topic": True,
                    "goal_alignment": True,
                    "role_nationality": True,
                    "overall_scenario_consistency_score": 5,
                },
                "self_consistency": {
                    "role_names": True,
                    "role_age": True,
                    "role_occupation": True,
                    "role_relationship": True,
                    "time_of_day": True,
                    "emotional_tone": True,
                    "relationship_dynamic": True,
                    "self_introduction": True,
                    "setting_context_alignment": True,
                    "overall_self_consistency_score": 5,
                },
            },
            "coherence": [
                {
                    "turn_id": turn_id,
                    "topic_relevance": True,
                    "contextual_follow_up": True,
                    "logical_continuity": True,
                    "no_contradiction": True,
                    "script_alignment": True,
                    "coherence_score": 5,
                }
                for turn_id in range(conversation_length)
            ],
            "naturalness": [
                {
                    "turn_id": turn_id,
                    "oral_style": True,
                    "length_and_flow": True,
                    "emotion_appropriateness": True,
                    "text_emotion_consistency": True,
                    "contextual_vocabulary_style": True,
                    "naturalness_score": 5,
                }
                for turn_id in range(conversation_length)
            ],
        }
        eval_form["evaluation_result"] = evaluation_result
        eval_forms.append(eval_form)

    return eval_forms


eval_forms = create_eval_form()

current_index = 0

# question_id = questions[current_index]["id"]
question_id = eval_forms[current_index]["id"]

metadata = questions[current_index]["metadata"]
conversations = questions[current_index]["conversation"]["conversation"]

evaluation = eval_forms[current_index]["evaluation_result"]
evaluation_tag = eval_forms[current_index]["evaluation_tag"]
scenario_consistency = evaluation["consistency"]["scenario_consistency"]
self_consistency = evaluation["consistency"]["self_consistency"]
coherence = evaluation["coherence"]
naturalness = evaluation["naturalness"]


def update_consistency(
    location,
    context,
    conversation_context_type,
    main_topic,
    goal_alignment,
    role_nationality,
    overall_scenario_consistency_score,
    role_names,
    role_age,
    role_occupation,
    role_relationship,
    time_of_day,
    emotional_tone,
    relationship_dynamic,
    self_introduction,
    setting_context_alignment,
    overall_self_consistency_score,
):

    # 更新字典中的值
    scenario_consistency["location"] = location
    scenario_consistency["context"] = context
    scenario_consistency["conversation_context_type"] = conversation_context_type
    scenario_consistency["main_topic"] = main_topic
    scenario_consistency["goal_alignment"] = goal_alignment
    scenario_consistency["role_nationality"] = role_nationality
    scenario_consistency["overall_scenario_consistency_score"] = (
        overall_scenario_consistency_score
    )

    self_consistency["role_names"] = role_names
    self_consistency["role_age"] = role_age
    self_consistency["role_occupation"] = role_occupation
    self_consistency["role_relationship"] = role_relationship
    self_consistency["time_of_day"] = time_of_day
    self_consistency["emotional_tone"] = emotional_tone
    self_consistency["relationship_dynamic"] = relationship_dynamic
    self_consistency["self_introduction"] = self_introduction
    self_consistency["setting_context_alignment"] = setting_context_alignment
    self_consistency["overall_self_consistency_score"] = overall_self_consistency_score
    eval_forms[current_index]["evaluation_result"]["consistency"] = {
        "scenario_consistency": scenario_consistency,
        "self_consistency": self_consistency,
    }
    return "Submit Consistency Evaluation Result Successfully"



def update_coherence(*args):
    clist = args

    num_to_name = {
        0: "topic_relevance",
        1: "contextual_follow_up",
        2: "logical_continuity",
        3: "no_contradiction",
        4: "script_alignment",
        5: "coherence_score",
    }

    if len(coherence_list) % 6 != 0:
        print("sth wrong with the coherence list length")
    
    count = 0
    print(len(coherence), len(args))
    for ti, turn in enumerate(coherence):
        for k, v in turn.items():
            if k == "turn_id":
                continue
            key_name = num_to_name[count % len(num_to_name)]
            coherence[ti][key_name] = clist[count]
            count += 1

    # def clean_questions(questions):
    #     # 假设 questions 是一个字典，遍历其中的每个元素
    #     for key, value in questions.items():
    #         if isinstance(value, threading.Lock):
    #             questions[key] = None  # 或者移除该元素
    #     return questions

    # 在序列化之前先清理 questions 对象
    # cleaned_questions = clean_questions(questions)

    # # 将更新后的数据保存到文件
    # with open("dialogues.pkl", "wb") as f:
    #     pickle.dump(
    #         questions_coherence[current_index]["evaluation_result"]["coherence"], f
    #     )
    eval_forms[current_index]["evaluation_result"]["coherence"] = coherence
    return "Submit Coherence Evaluation Result Successfully"


def save_result():
    output_file = args.output_path + f"{current_index}.json"
    eval_forms[current_index]["evaluation_tag"] = True
    with open(output_file, "w") as f:
        print(eval_forms[current_index])
        json.dump(eval_forms[current_index], f)
    return "Save Successfully"


def next_page():
    global current_index
    current_index += 1
    demo.refresh()
    return current_index


with gr.Blocks() as demo:

    gr.Markdown("# Evaluation Interface")
    with gr.Row():
        gr.Textbox(value=str(question_id), label="Question ID", interactive=False)
        gr.Textbox(value=str(evaluation_tag), label="Is Evaluated", interactive=False)

    with gr.Accordion("Metadata that be used to generate conversation"):
        gr.Markdown("# Metadata about Conversation")

        with gr.Tab("Input Scenario"):
            with gr.Row():
                gr.Textbox(
                    value=metadata["input_scenario"]["interaction_type"],
                    label="Interaction Type",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["input_scenario"]["location"],
                    label="Location",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["input_scenario"]["goal"],
                    label="Goal",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["input_scenario"]["cultural_background"],
                    label="Cultural Background",
                    interactive=False,
                )

        with gr.Tab("Setting"):
            with gr.Row():
                gr.Textbox(
                    value=metadata["setting"]["location"],
                    label="Setting Location",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["setting"]["time_of_day"],
                    label="Time of Day",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["setting"]["context"],
                    label="Context",
                    interactive=False,
                )

        with gr.Tab("Role 1"):
            with gr.Row():
                gr.Textbox(
                    value=metadata["role_1"]["name"],
                    label="Role 1 Name",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["role_1"]["gender"],
                    label="Role 1 Gender",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["role_1"]["age"],
                    label="Role 1 Age",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["role_1"]["occupation"],
                    label="Role 1 Occupation",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["role_1"]["nationality"],
                    label="Role 1 Nationality",
                    interactive=False,
                )
                gr.Textbox(
                    value=", ".join(metadata["role_1"]["personality_traits"]),
                    label="Role 1 Personality Traits",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["role_1"]["relationship_context"],
                    label="Role 1 Relationship Context",
                    interactive=False,
                )
            gr.Textbox(
                value=metadata["role_1"]["self_introduction"],
                label="Role 1 Self Introduction",
                interactive=False,
                lines=5,
            )

        with gr.Tab("Role 2"):
            with gr.Row():
                gr.Textbox(
                    value=metadata["role_2"]["name"],
                    label="Role 2 Name",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["role_2"]["gender"],
                    label="Role 2 Gender",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["role_2"]["age"],
                    label="Role 2 Age",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["role_2"]["occupation"],
                    label="Role 2 Occupation",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["role_2"]["nationality"],
                    label="Role 2 Nationality",
                    interactive=False,
                )
                gr.Textbox(
                    value=", ".join(metadata["role_2"]["personality_traits"]),
                    label="Role 2 Personality Traits",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["role_2"]["relationship_context"],
                    label="Role 2 Relationship Context",
                    interactive=False,
                )
            gr.Textbox(
                value=metadata["role_2"]["self_introduction"],
                label="Role 2 Self Introduction",
                interactive=False,
                lines=5,
            )

        with gr.Tab("Conversation Context"):
            with gr.Row():
                gr.Textbox(
                    value=metadata["conversation_context"]["type"],
                    label="Conversation Type",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["conversation_context"]["main_topic"],
                    label="Main Topic",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["conversation_context"]["relationship_dynamic"],
                    label="Relationship Dynamic",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["conversation_context"]["emotional_tone"],
                    label="Emotional Tone",
                    interactive=False,
                )
                # with gr.Row():
                gr.Textbox(
                    value=metadata["conversation_context"]["expected_duration"],
                    label="Expected Duration",
                    interactive=False,
                )
                gr.Textbox(
                    value=metadata["conversation_context"]["expected_turns"],
                    label="Expected Turns",
                    interactive=False,
                )
            gr.Textbox(
                value=", ".join(metadata["conversation_context"]["key_points"]),
                label="Key Points",
                interactive=False,
                lines=5,
            )

    interactive_components = {}
    with gr.Accordion("Information Below need to be filled"):
        gr.Markdown("# Consistency Evaluation")
        gr.Markdown("### Scenario Consistency")

        location = gr.Checkbox(
            label="location", value=scenario_consistency.get("location", True)
        )
        context = gr.Checkbox(
            label="context", value=scenario_consistency.get("context", True)
        )
        conversation_context_type = gr.Checkbox(
            label="conve_context_type",
            value=scenario_consistency.get("conversation_context_type", True),
        )
        main_topic = gr.Checkbox(
            label="main_topic",
            value=scenario_consistency.get("main_topic", True),
        )
        # with gr.Row():
        goal_alignment = gr.Checkbox(
            label="goal_alignment",
            value=scenario_consistency.get("goal_alignment", True),
        )
        role_nationality = gr.Checkbox(
            label="role_nationality",
            value=scenario_consistency.get("role_nationality", True),
        )
        overall_scenario_consistency_score = gr.Dropdown(
            [1, 2, 3, 4, 5],
            label="overall_scenario_consistency_score",
            value=scenario_consistency.get("overall_scenario_consistency_score", 5),
        )

        gr.Markdown("### Self Consistency")
        with gr.Row():
            role_names = gr.Checkbox(
                label="role_names", value=self_consistency.get("role_names", True)
            )
            role_age = gr.Checkbox(
                label="role_age", value=self_consistency.get("role_age", True)
            )
            role_occupation = gr.Checkbox(
                label="role_occupation",
                value=self_consistency.get("role_occupation", True),
            )
            role_relationship = gr.Checkbox(
                label="role_relationship",
                value=self_consistency.get("role_relationship", True),
            )
            # with gr.Row():
            time_of_day = gr.Checkbox(
                label="time_of_day", value=self_consistency.get("time_of_day", True)
            )
            emotional_tone = gr.Checkbox(
                label="emotional_tone",
                value=self_consistency.get("emotional_tone", True),
            )
            relationship_dynamic = gr.Checkbox(
                label="relationship_dynamic",
                value=self_consistency.get("relationship_dynamic", True),
            )
            self_introduction = gr.Checkbox(
                label="self_introduction",
                value=self_consistency.get("self_introduction", True),
            )
            # with gr.Row():
            setting_context_alignment = gr.Checkbox(
                label="setting_context_alignment",
                value=self_consistency.get("setting_context_alignment", True),
            )
            overall_self_consistency_score = gr.Dropdown(
                [1, 2, 3, 4, 5],
                label="overall_self_consistency_score",
                value=self_consistency.get("overall_self_consistency_score", 5),
            )

        update_consistency_input = {
            "location": location,
            "context": context,
            "conversation_context_type": conversation_context_type,
            "main_topic": main_topic,
            "goal_alignment": goal_alignment,
            "role_nationality": role_nationality,
            "overall_scenario_consistency_score": overall_scenario_consistency_score,
            "role_names": role_names,
            "role_age": role_age,
            "role_occupation": role_occupation,
            "role_relationship": role_relationship,
            "time_of_day": time_of_day,
            "emotional_tone": emotional_tone,
            "relationship_dynamic": relationship_dynamic,
            "self_introduction": self_introduction,
            "setting_context_alignment": setting_context_alignment,
            "overall_self_consistency_score": overall_self_consistency_score,
        }

        # Consistency button
        submit_consist_btn = gr.Button("Submit Consistency Result")
        submit_consist_btn.click(
            update_consistency,
            inputs=list(update_consistency_input.values()),
            outputs=gr.Textbox(label="Submit Feedback"),
        )

    gr.Markdown("# Conversation Log")
    for turn_id, turn in enumerate(conversations):
        with gr.Accordion(f"Turn {turn_id} - {turn['speaker']}"):
            gr.Textbox(value=turn["text"], interactive=False, lines=2, label="Text")
            with gr.Row():
                gr.Textbox(value=turn["emotion"], interactive=False, label="Emotion")
                gr.Textbox(
                    value=turn["speech_rate"],
                    interactive=False,
                    label="Speech Rate",
                )
                gr.Textbox(
                    value=turn["pause_after"],
                    interactive=False,
                    label="Pause After",
                )

            gr.Markdown("### Coherence Evaluation")
            with gr.Row():
                for key, value in evaluation["coherence"][turn_id].items():
                    if key == "turn_id":  # 跳过 turn_id
                        continue
                    if isinstance(value, bool):  # 对于布尔值创建 Checkbox
                        checkbox = gr.Checkbox(label=key, value=value, interactive=True)
                        # 动态赋值给变量 topic_relevance_0 = checkbox
                        globals()[
                            f"coherence_{key}_{turn_id}"
                        ] = checkbox  # 使用 globals() 动态创建变量名

                    elif isinstance(
                        value, int
                    ):  # 对于整数（coherence_score）创建 Dropdown
                        dropdown = gr.Dropdown(
                            [1, 2, 3, 4, 5],
                            label=key,
                            value=value,
                            interactive=True,
                        )
                        # 动态赋值给变量 coherence_score_0 = dropdown
                        globals()[f"coherence_{key}_{turn_id}"] = dropdown

    coherence_var_list = [
        var_name for var_name in globals() if var_name.startswith("coherence_")
    ]
    # 获取对应的对象并存入列表
    coherence_list = [globals()[var_name] for var_name in coherence_var_list]
    print(coherence_var_list[0])
    print(globals()[coherence_var_list[0]])
    print(coherence_list[0])

    # Consistency button
    submit_coherence_btn = gr.Button("Submit Coherence Result")
    submit_coherence_btn.click(
        update_coherence,
        inputs=coherence_list,
        outputs=gr.Textbox(label="Submit Feedback"),
    )
    save_btn = gr.Button("Save Result")
    save_btn.click(
        save_result,
        inputs=[],
        outputs=gr.Textbox(label="Save Feedback"),
    )
    next_btn = gr.Button("Next")
    next_btn.click(
        next_page,
        inputs=[],
        outputs=[],
    )

    demo.launch()

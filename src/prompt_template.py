import re

PROMPT_TEMPLATE = """
You are an expert narrative analyst. Your task is to compare stories based on deep narrative structure.

**Input Data:**
- Anchor Story: {anchor_text}
- Story A: {text_a}
- Story B: {text_b}

**Task:**
**MANDATORY ASPECTS TO ANALYZE (use these as your framework):**
1. Moral Story: The underlying message, lesson, or value conveyed.
2. Motivate Actor: The core driving desire, goal, or need of the protagonist.
3. Ending Story: The final resolution, fate of the characters, or concluding state.
4. Point of Action: The climax, turning point, or critical event that changes the trajectory.
5. Reason of Actor Doing That: The logical justification behind the protagonist's key decisions or actions.

**STRICTLY IGNORE (DO NOT consider these factors):**
- Writing style (e.g., poetic, formal, descriptive).
- Location names, setting specifics, or time periods.
- Subject/Character names (who did what is irrelevant; focus on *why* and *what happened*).
- Text length or level of superficial detail (e.g., weather, color, physical appearance).

**OUTPUT FORMAT (STRICT):**
You MUST respond ONLY with the following XML-style tags. Do not add any introductory text, notes, or markdown outside these tags.

<reason>
[Write your structured reasoning here. Keep it concise, structured (e.g., based on the 5 aspects), and avoid stream-of-consciousness monologues. Compare both stories to the Anchor explicitly.]
</reason>
<Answer>correct label (A/B)</Answer>
"""


def create_sft_prompt(df):
    raw_prompts, raw_outputs, kept_idx = [], [], []

    for idx, row in df.iterrows():
        prompt = PROMPT_TEMPLATE.format(
            anchor_text=row["anchor_text"],
            text_a=row["text_a"],
            text_b=row["text_b"],
        )
        raw_output = (
            f"<think>\n{row['sft_reason']}\n</think>\n"
            f"<Answer>{row['sft_answer']}</Answer>"
        )
        if re.fullmatch(
            r"<think>\s*.*?\s*</think>\s*<Answer>\s*[AB]\s*</Answer>",
            raw_output,
            flags=re.DOTALL,
        ):
            raw_prompts.append(prompt)
            raw_outputs.append(raw_output)
            kept_idx.append(idx)

    df = df.loc[kept_idx].copy()
    df["sft_prompt"] = raw_prompts
    df["generated_raw_output"] = raw_outputs
    return df
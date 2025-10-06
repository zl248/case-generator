"""Gradio UI layer bound to the service functions."""

from __future__ import annotations

from datetime import datetime
from typing import Tuple

import gradio as gr

from .config import get_config
from .service import generate_harvard_case_2api


def _check_password(password_input: str, access_password: str) -> Tuple[gr.Update, gr.Update]:
    """Return visibility updates based on password validity."""

    if password_input == access_password:
        return gr.update(visible=False), gr.update(visible=True)
    return gr.update(visible=True, value="Incorrect password!"), gr.update(visible=False)


def _save_to_file(text: str) -> str:
    """Save generated text to a timestamped file and return filename."""

    filename = f"harvard_case_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    return filename


def build_app() -> gr.Blocks:
    """Construct and return the Gradio Blocks app."""

    config = get_config()

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎓 Harvard Case Study Generator (smart adaptive prompt edition)")
        gr.Markdown("**Automatically adapts to case focus. Best practice, simple for users.**")

        password = gr.Textbox(label="Password", type="password")
        password_button = gr.Button("Enter")

        protected_block = gr.Group(visible=False)
        with protected_block:
            gr.Markdown("### Harvard MBA Case Generation")
            with gr.Row():
                with gr.Column():
                    subject = gr.Textbox(label="Course/Subject", value="Strategic Management")
                    learning_outcomes = gr.Textbox(
                        label="Learning Outcomes",
                        lines=3,
                        value=(
                            "Students will learn to: (1) Analyze strategic decision-making in dynamic industries; "
                            "(2) Evaluate multiple strategic alternatives using decision frameworks; "
                            "(3) Assess stakeholder impacts and implementation challenges; "
                            "(4) Apply financial analysis to strategic choices; "
                            "(5) Develop recommendations for complex business decisions"
                        ),
                    )
                    case_focus = gr.Textbox(
                        label="Case Focus", lines=2, value="Netflix innovation strategy and growth decisions for 2025"
                    )
                    industry_company = gr.Textbox(
                        label="Company", value="Netflix (innovation strategy decisions in 2025)"
                    )
                    case_type = gr.Dropdown(
                        label="Case Type",
                        choices=[
                            "Decision-making case",
                            "Problem-solving case",
                            "Leadership/Teamwork case",
                            "Crisis management case",
                            "Innovation/Change case",
                            "Ethics case",
                            "Valuation case",
                            "Capital Structure case",
                            "Investment Decision case",
                            "Financial Crisis case",
                        ],
                        value="Innovation/Change case",
                    )
        generate_case_btn = gr.Button("🚀 Generate Harvard Case (2 API calls)", variant="primary", size="lg")
        case_output = gr.Textbox(
            label="Full Harvard MBA Case (teaching notes, exhibits, references)",
            lines=60,
            placeholder="Full Harvard MBA case will appear here...",
        )

        download_btn = gr.DownloadButton("💾 Download Case")

        password_button.click(
            fn=lambda pwd: _check_password(pwd, config.access_password), inputs=password, outputs=[password, protected_block]
        )
        generate_case_btn.click(
            fn=lambda s, lo, cf, ic, ct: generate_harvard_case_2api(get_config(), s, lo, cf, ic, ct),
            inputs=[subject, learning_outcomes, case_focus, industry_company, case_type],
            outputs=case_output,
        )
        download_btn.click(fn=_save_to_file, inputs=[case_output], outputs=[download_btn])

    return demo



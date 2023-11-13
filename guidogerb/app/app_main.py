from pathlib import Path
from typing import Optional, Tuple, Union
import os

def run_guidogerb_gpt(
        continuous: bool,
        continuous_limit: int,
        ai_settings: str,
        prompt_settings: str,
        skip_reprompt: bool,
        speak: bool,
        debug: bool,
        gpt3only: bool,
        gpt4only: bool,
        memory_type: str,
        browser_name: str,
        allow_downloads: bool,
        skip_news: bool,
        working_directory: Path,
        workspace_directory: Union[str, Path],
        install_plugin_deps: bool,
        ai_name: Optional[str] = "Default_AI_Name",
        ai_role: Optional[str] = "Default_AI_Role",
        ai_goals: Tuple[str, ...] = ("Goal1", "Goal2"),
):
    """
    This function runs the auto GPT process based on the parameters provided.

    Parameters:
    - continuous:
    - continuous_limit:
    .
    .
    .
    and so on for all parameters

    Returns:
    TODO: Depending on what function returns
    """
    output_dir = f"{os.getcwd()}/output"
    name = "GuidoGerb-GPT"
    print(f"Hello, {name} Dude! Going to build an application in {output_dir}")
    pass
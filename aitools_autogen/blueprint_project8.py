from typing import Optional

import aitools_autogen.utils as utils
from aitools_autogen.agents import WebPageScraperAgent
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR
from autogen import ConversableAgent


class HTMLPageGeneratorBlueprint(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "coding"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        utils.clear_working_dir(self._work_dir)

        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        scraper_agent = WebPageScraperAgent()

        code_generator_agent = ConversableAgent("code_generator_agent",
                                                max_consecutive_auto_reply=6,
                                                llm_config=llm_config,
                                                human_input_mode="NEVER",
                                                code_execution_config=False,
                                                function_map=None,
                                                system_message="""You are an HTML page generator.
        You are tasked with creating a utility that helps developers generate HTML pages.
        The utility should support creating HTML pages with basic elements such as headers, paragraphs, lists, and links.

        The user will provide a description of the HTML page's structure and content.
        The utility should generate the corresponding HTML code.

        The code should be generated in the `aitools_autogen/coding` directory.

        The code must be structured into multiple Python files in a directory structure that makes sense.
        Each Python file should contain a Python class responsible for generating a specific part of the HTML page.

        You must indicate the script type in the code block.
        Do not suggest incomplete code which requires users to modify.
        Always put `# filename: aitools_autogen/coding/<filename>` as the first line of each code block.

        Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.
        """)

        agent0.initiate_chat(scraper_agent, True, True, message=message)

        message = agent0.last_message(scraper_agent)

        agent0.initiate_chat(code_generator_agent, True, True, message=message)

        code_message = agent0.last_message(code_generator_agent)["content"]
        utils.save_code_files(code_message, self.work_dir)

        self._summary_result = utils.summarize_files(self.work_dir)

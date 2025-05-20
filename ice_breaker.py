# Copyright 2025 Eden Marco and Nicole Hessner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

from output_parsers import summary_parser

def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=False) #linkedin_profile_url="https://gist.githubusercontent.com/nikkihessner/5577395b53d2a73fd018d870726f6e03/raw/7f8e739ffbb11517b77eed46a193364cb36e0ec4/nikki-hessner-scrapin.json")
    
    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:

    Please:
    1. Write a short summary.
    2. List two interesting facts about them.
    3. Return firstName and lastName.
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables="information", 
        template=summary_template,
        partial_variables = {"format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    # llm = ChatOllama(model="llama3")
    # chain = summary_prompt_template | llm 
    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")

    ice_break_with(name="Nicole Hessner")
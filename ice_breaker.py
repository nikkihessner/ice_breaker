from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://gist.githubusercontent.com/nikkihessner/5577395b53d2a73fd018d870726f6e03/raw/7f8e739ffbb11517b77eed46a193364cb36e0ec4/nikki-hessner-scrapin.json")

if __name__ == "__main__":
    print("Hello LangChain")

    summary_template = """
    Given the following information about a person:

    {information}

    Please:
    1. Write a short summary.
    2. List two interesting facts about them.
    3. Return firstName and lastName.
    """
    
    summary_prompt_template = PromptTemplate(input_variables="information", template=summary_template)

    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data})

    print(res)
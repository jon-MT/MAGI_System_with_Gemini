import os
from dotenv import load_dotenv
import google.generativeai as genai


class MAGIModuleBuilder:
    def __init__(self, system_prompt):
        load_dotenv()
        API_KEY = os.environ.get("API_KEY")
        genai.configure(api_key=API_KEY)
        self.llm = genai.GenerativeModel("gemini-pro")
        self.system_prompt = system_prompt

    def gen_answer(self, usr_input):
        text = f"""あなたはコンサルタントです。
        {self.system_prompt}
        以下の質問に対してあなたの立場を明確にし、回答してください。
        {usr_input}"""
        answer = self.llm.generate_content(text)
        return answer.text


class MAGIIntegration:
    def __init__(self, casper_role, balthasar_role, merchior_role):
        load_dotenv()
        API_KEY = os.environ.get("API_KEY")
        genai.configure(api_key=API_KEY)
        self.llm = genai.GenerativeModel("gemini-pro")
        self.casper_module = MAGIModuleBuilder(casper_role)
        self.balthasar_module = MAGIModuleBuilder(balthasar_role)
        self.merchior_module = MAGIModuleBuilder(merchior_role)

    def gen_module_answer(self, question):
        casper = self.casper_module.gen_answer(question)
        balthasar = self.balthasar_module.gen_answer(question)
        merchior = self.merchior_module.gen_answer(question)
        self.answers_from_modules = {
            "casper": casper,
            "balthasar": balthasar,
            "merchior": merchior,
        }
        return self


    def find_answer(self, answer):
        first_20_chars = answer[:20]
        position_agree = first_20_chars.find("賛成")
        position_disagree = first_20_chars.find("反対")
        if position_agree != -1 and position_disagree != -1:
            return "賛成" if position_agree < position_disagree else "反対"
        elif position_agree != -1:
            return "賛成"
        elif position_disagree != -1:
            return "反対"
        else:
            return "不明"

    def vote(self):
        ans_list = []
        for ans in self.answers_from_modules.values():
            judge = self.find_answer(ans)
            ans_list.append(judge)
        agree = 0
        disagree = 0
        for answer in ans_list:
            if answer == "賛成":
                agree += 1
            elif answer == "反対":
                disagree += 1
        if agree > disagree:
            self.judge = "賛成"
        elif agree < disagree:
            self.judge = "反対"
        else:
            self.judge = "不明"
        return self
        
    def gen_final_answer(self, question):
        self.gen_module_answer(question)
        text = f"""以下の質問に対して、3者の意見を参考にしながら、あなたの意見を考えて回答してください。
        Casperの意見: {self.answers_from_modules["casper"]}
        Balthasarの意見: {self.answers_from_modules["balthasar"]}
        Merchiorの意見: {self.answers_from_modules["merchior"]}
        {question}"""
        answer = self.llm.generate_content(text)
        return answer.text
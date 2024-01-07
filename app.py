import streamlit as st
import time
from MAGIModel import MAGIIntegration

st.title("MAGI System powered by GeminiPro")

def main():
    casper_role = st.sidebar.text_input(
        label="Casper's personality",
        value="あなたの価値基準: 効率と結果が最も重要。彼は最適なソリューションを見つけ、目標達成に徹底的に焦点を当てる。あなたの性格: 冷静かつ冷徹。合理的で論理的なアプローチを好み、感情に左右されることなくビジネス上の意思決定を行う。"
    )
    balthasar_role = st.sidebar.text_input(
        label="Barthasar's personality",
        value="あなたの価値基準: イノベーションと創造性。あなたは問題解決において新しいアイデアと独自の視点を大切にする。あなたの性格: 情熱的でアーティスティック。柔軟で非伝統的なアプローチが得意で、クリエイティブな解決策を見つけるのがあなたの強み。"
    )
    merchior_role = st.sidebar.text_input(
        label="Merchior's personality",
        value="あなたの価値基準: 人間関係とネットワーキング。あなたは人との繋がりや協力がプロジェクトの成功に不可欠だと考えている。あなたの性格: 社交的でコミュニケーション力が高い。人々を引き込む力があり、チームワークや協力を強化するのが得意。"
    )
    question = st.text_input("質問を入力してください")
    if question:
        st.markdown("""### MAGIによる回答""")
        integration_module = MAGIIntegration(casper_role, balthasar_role, merchior_role)
        answer = integration_module.gen_final_answer(question)
        ai_message = ""
        ai_response_area = st.empty()
        for c in answer:
            ai_message += c
            ai_response_area.write(ai_message)
            time.sleep(0.03)
        st.markdown("""### Moduleの意見""")
        for k, v in integration_module.answers_from_modules.items():
            st.write(f"**{k}**")
            st.write(v)
            st.write("-"*50)

main()


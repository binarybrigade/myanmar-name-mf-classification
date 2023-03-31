import streamlit as st
from utilities import manual_test , convert_en_to_mm, clean_text

def main():

    st.title("မြန်မာနာမည်ကို ကျားမ ခွဲမယ်")
    mmr_input_text = st.text_input("နာမည်လေးရိုက်ထည့်ပေးပါ...")
    mmr_output_text = ""
    if st.button("အဖြေရဖို့နှိပ်ပါ"):
        result = manual_test(clean_text(mmr_input_text))
        if result==1:
            mmr_output_text = mmr_output_text + "\n" + mmr_input_text + " က မိန်းကလေး ပါ။"
        elif result==0:
            mmr_output_text = mmr_output_text + "\n" + mmr_input_text + " က ယောက်ျားလေး ပါ။"
        else:
            mmr_output_text = mmr_output_text + "\n" + mmr_input_text + " က ယောက်ျားလေး ရော မိန်းကလေး ပါ ဖြစ်နိုင်ပါတယ်။"
        st.write(mmr_output_text)
    
    st.title("Let's try to classify Burmese Names by sex")
    
    eng_input_text = st.text_input("Put the burmese name in below box:")
    
    eng_output_text = ""
    
    if st.button("Click here to get answer"):
        translate_test = convert_en_to_mm(eng_input_text)
        result = manual_test(clean_text(translate_test))
        if result==1:
            eng_output_text = eng_output_text + "\n" + eng_input_text + " is female name"
        elif result==0:
            eng_output_text = eng_output_text + "\n" + eng_input_text + " is male name"
        else:
            eng_output_text = eng_output_text + "\n" + eng_input_text + " can be both male and female."
        st.write(eng_output_text)

    st.title("Report Name")
    st.text("If you found wrong one or new names, please submit the right one via following link...")
    st.markdown("[https://docs.google.com/forms/d/e/1FAIpQLSd8XDQHA1ZFk8hjMRH_VThFfI5fGnaJgQO2Dm5xfoVZuLpxbg/viewform?usp=sf_link](https://docs.google.com/forms/d/e/1FAIpQLSd8XDQHA1ZFk8hjMRH_VThFfI5fGnaJgQO2Dm5xfoVZuLpxbg/viewform?usp=sf_link)")

if __name__ == "__main__":
    main()
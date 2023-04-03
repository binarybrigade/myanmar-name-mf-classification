import streamlit as st
from utilities import manual_test , convert_en_to_mm, clean_text

def main():

    st.title("မြန်မာနာမည်ကို ကျားမ ခွဲမယ်")
    mmr_input_text = st.text_input("နာမည်လေးရိုက်ထည့်ပေးပါ... (မြန်မာလိုပဲ ရိုက်ထည့်ပေးပါ)")
    mmr_output_text = ""
    if st.button("အဖြေရဖို့နှိပ်ပါ"):
        if len(mmr_input_text.strip())>0:
            result = manual_test(clean_text(mmr_input_text))
            if result==1:
                mmr_output_text = mmr_output_text + "\nလက်ရှိသုံးနေတဲ့ Data များအရ " + mmr_input_text + " ဆိုတဲ့ နာမည်က မိန်းကလေး အများစု သုံးပါတယ်။"
            elif result==0:
                mmr_output_text = mmr_output_text + "\nလက်ရှိသုံးနေတဲ့ Data များအရ " + mmr_input_text + " ဆိုတဲ့ နာမည်က ယောက်ျားလေး အများစု သုံးပါတယ်။"
            else:
                mmr_output_text = mmr_output_text + "\nလက်ရှိသုံးနေတဲ့ Data များအရ " + mmr_input_text + " ဆိုတဲ့ နာမည်က ယောက်ျားလေး ရော မိန်းကလေး ပါ ဖြစ်နိုင်ပါတယ်။"
            st.write(mmr_output_text)
    
    st.title("Let's try to classify Burmese Names by sex")
    
    eng_input_text = st.text_input("Put the burmese name in below box: (Type in english)")
    
    eng_output_text = ""
    
    if st.button("Click here to get answer"):
        if len(eng_input_text.strip())>0:
            translate_test = convert_en_to_mm(eng_input_text)
            result = manual_test(clean_text(translate_test))
            if result==1:
                #According to the current dataset, .... is mostly used by male.
                eng_output_text = eng_output_text + "\nAccording to the current dataset, " + eng_input_text + " is mostly used by female."
            elif result==0:
                eng_output_text = eng_output_text + "\nAccording to the current dataset, " + eng_input_text + " is mostly used by male."
            else:
                eng_output_text = eng_output_text + "\nAccording to the current dataset, " + eng_input_text + " can be both male and female."
            st.write(eng_output_text)

    st.title("Report Name")
    st.text("If you found wrong one or new names, please submit the right one via following link...")
    st.markdown("[https://docs.google.com/forms/d/e/1FAIpQLSd8XDQHA1ZFk8hjMRH_VThFfI5fGnaJgQO2Dm5xfoVZuLpxbg/viewform?usp=sf_link](https://docs.google.com/forms/d/e/1FAIpQLSd8XDQHA1ZFk8hjMRH_VThFfI5fGnaJgQO2Dm5xfoVZuLpxbg/viewform?usp=sf_link)")

if __name__ == "__main__":
    main()

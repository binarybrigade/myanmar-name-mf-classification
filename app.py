import streamlit as st
from utilities import manual_test

def main():
    st.title("မြန်မာနာမည်ကို ကျားမ ခွဲမယ်")
    
    input_text = st.text_input("နာမည်လေးရိုက်ထည့်ပေးပါ...")
    
    output_text = ""
    
    if st.button("အဖြေရဖို့နှိပ်ပါ"):
        result = manual_test(input_text)
        if result==1:
            output_text = output_text + "\n" + input_text + " က မိန်းကလေး ပါ။"
        elif result==0:
            output_text = output_text + "\n" + input_text + " က ယောက်ျားလေး ပါ။"
        else:
            output_text = output_text + "\n" + input_text + " က ယောက်ျားလေး ရော မိန်းကလေး ပါ ဖြစ်နိုင်ပါတယ်။"
        st.write(output_text)

if __name__ == "__main__":
    main()
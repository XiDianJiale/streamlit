import streamlit as st
import pandas as pd

st.write("## 你好，jiale")

[1 , 2 , 3 ]

{"a":"1","b":"2"}

st.image("./自拍照fixed.png",width=500)

df = pd.DataFrame({
    "兴趣":["社会科学","自媒体","AI+science科研"],
    "合作意愿顺序":[2,0,1],
    "开价":[0,300,0]
})

st.dataframe(df)

st.divider()

st.table(df)


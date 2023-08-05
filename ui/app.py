import streamlit as st
import pandas as pd
import altair as alt

data = {
    'Category': ['Category 1', 'Category 2', 'Category 3'],
    'Value': [30, 40, 50]
}

df = pd.DataFrame(data)


def create_bar_chart(df):
    bar_chart = alt.Chart(df).mark_bar().encode(
        x='Category:N',
        y='Value:Q',
        tooltip=['Category', 'Value']
    ).properties(
        width=400,
        height=300
    )
    return bar_chart


st.title('Bar Chart Example')
st.write(df)
bar_chart = create_bar_chart(df)
st.altair_chart(bar_chart)

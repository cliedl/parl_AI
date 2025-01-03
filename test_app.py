import streamlit as st

if "value_dict" not in st.session_state:
    st.session_state.value_dict = {i: False for i in range(10)}


def set_value(value):
    print(f"Setting value {value} to {not st.session_state.value_dict[value]}")
    st.session_state.value_dict[value] = not st.session_state.value_dict[value]


for i in range(10):
    st.checkbox(
        f"Check value {i}", on_change=set_value, kwargs={"value": i}, key=i * 10
    )


st.write(st.session_state.value_dict)

true_values = [k for k, v in st.session_state.value_dict.items() if v]

st.write(f"Values that are True: {true_values}")

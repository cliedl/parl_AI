import streamlit as st


def support_button(
    text: str,
    link: str,
    bg_color: str = "#FFDD00",
    font_color: str = "#000000",
    bottom: str = "20px",
    right: str = "20px",
    font_size: str = "16px",
):
    """
    Create a floating action button in a Streamlit app.

    Args:
        text (str): The text to display on the button.
        link (str): The URL the button should link to.
        bg_color (str, optional): Background color of the button. Defaults to "#FFDD00".
        font_color (str, optional): Font color of the button. Defaults to "#000000".
        bottom (str, optional): Distance from the bottom of the viewport. Defaults to "20px".
        right (str, optional): Distance from the right of the viewport. Defaults to "20px".
        font_size (str, optional): Font size of the button text. Defaults to "16px".
    """
    button_html = f"""
    <a href="{link}" target="_blank">
        <button style="
            position: fixed;
            bottom: {bottom};
            right: {right};
            background-color: {bg_color};
            color: {font_color};
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: {font_size};
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            z-index: 1000;
        ">
        {text}
        </button>
    </a>
    """
    st.markdown(button_html, unsafe_allow_html=True)


def support_banner(
    text: str,
    link: str,
    bg_color: str = "#FFDD00",
    font_color: str = "#000000",
    top: str = "60px",
    font_size: str = "16px",
):
    """
    Create a floating banner in a Streamlit app.

    Args:
        text (str): The text to display on the banner.
        link (str): The URL the banner should link to.
        bg_color (str, optional): Background color of the banner. Defaults to "#FFDD00".
        font_color (str, optional): Font color of the banner. Defaults to "#000000".
        top (str, optional): Distance from the top of the viewport. Defaults to "20px".
        font_size (str, optional): Font size of the banner text. Defaults to "16px".
    """
    banner_html = f"""
    <a href="{link}" target="_blank">
        <div style="
            position: fixed;
            top: {top};
            center:50%;
            background-color: {bg_color};
            color: {font_color};
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: {font_size};
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            z-index: 1000;
        ">
        {text}
        </div>
    </a>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

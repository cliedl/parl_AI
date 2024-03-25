@extra
def button(
    username: str,
    floating: bool = True,
    text: str = "Buy me a coffee",
    emoji: str = "",
    bg_color: str = "#FFDD00",
    font: Font = "Cookie",
    font_color: str = "#000000",
    coffee_color: str = "#000000",
    width: int = 220,
):
    """
    Display a button which links to your Buy Me a Coffee page.

    Args:
        username (str): Buy Me a Coffee username
        floating (bool, optional): Whether the button should be floating. Defaults to True.
        text (str, optional): Text to show on the button. Defaults to "Buy me a coffee".
        emoji (str, optional): Emoji to show on the button. Defaults to "".
        bg_color (str, optional): Background of the button. Defaults to "#FFDD00".
        font (Font, optional): Font of the button. Defaults to "Cookie".
        font_color (str, optional): Font color. Defaults to "#000000".
        coffee_color (str, optional): Coffee icon color. Defaults to "#000000".
        width (int, optional): Width of the button. Defaults to 220.
    """ """"""
    button = f"""
        <script type="text/javascript"
            src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js"
            data-name="bmc-button"
            data-slug="{username}"
            data-color="{bg_color}"
            data-emoji="{emoji}"
            data-font="{font}"
            data-text="{text}"
            data-outline-color="#000000"
            data-font-color="{font_color}"
            data-coffee-color="{coffee_color}" >
        </script>
    """

    html(button, height=70, width=width)

    if floating:
        st.markdown(
            f"""
            <style>
                iframe[width="{width}"] {{
                    position: fixed;
                    bottom: 60px;
                    right: 40px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
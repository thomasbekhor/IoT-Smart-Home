

import time
import streamlit as st
from streamlit_option_menu import option_menu

class Sidebar():
    def __init__(self, title, components, debug=False):
        self.title = title
        self.components = components
        self.selected = "Home"

        # self.debug = debug

    def render(self):
        with st.sidebar:
            selected = option_menu(
                "My Home", 
                ["Home"] + self.components + ["Settings"], 
                icons=["house"] + ["" for _ in self.components] + ["gear"], 
                menu_icon="house", 
                default_index=0            )
        
        self.selected = selected
        return selected

            # Add Space:
            # st.container(height=250, border=False)

            # Add a checkbox to toggle debug mode
            # debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=self.debug)


if __name__ == "__main__":

    sidebar = Sidebar(
        title="My Home",
        components=["Room 1", "Room 2", "Room 3"],
        debug=True
    )
    selected = sidebar.render()
    print(selected)
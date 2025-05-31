
import streamlit as st

class Settings():
    def __init__(self, title, debug=False):
        self.title = title
        self.debug = debug

    def render(self):
        st.title(self.title)
        
        # Add a checkbox to toggle debug mode
        self.debug = st.checkbox("Enable Debug Mode", value=self.debug)
        
        if self.debug:
            st.write("Debug mode is enabled.")
        else:
            st.write("Debug mode is disabled.")
        
        st.session_state["debug_mode"] = self.debug
        return self.debug
    

if __name__ == "__main__":
    settings = Settings()
    debug_mode = settings.render()
    print(f"Debug mode is {'enabled' if debug_mode else 'disabled'}.")
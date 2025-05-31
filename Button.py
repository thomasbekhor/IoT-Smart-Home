import streamlit as st

class ButtonWidget:
    def __init__(self, label="Toggle Button", state_key="toggle_state", button_key="toggle_button", debug=False):
        self.label = label
        self.state_key = state_key        # Key for storing the toggle state
        self.button_key = button_key      # Unique key for the button widget
        self.debug = debug
        
        # Initialize the toggle state if it does not exist
        if self.state_key not in st.session_state:
            st.session_state[self.state_key] = False

    def render(self):
        # The button uses a separate key so it doesn't conflict with our state_key.
        if st.button(self.label, key=self.button_key):
            # Toggle the persistent state
            st.session_state[self.state_key] = not st.session_state[self.state_key]
        
        toggle_value = st.session_state[self.state_key]

        # st.write("Toggle is", "ON" if toggle_value else "OFF")

        # Optionally display debug info
        if self.debug:
            print(f"[DEBUG] Toggle value: {toggle_value}")
            
        return toggle_value


if __name__ == "__main__":
    def main():
        st.title("Toggle Button Example")
        
        # Create and render our toggle button with separate keys for state and widget.
        toggle = ButtonWidget(
            label="Click to Toggle", 
            state_key="my_toggle_state", 
            button_key="my_toggle_button", 
            debug=True)
        
        # Render the component
        current_toggle = toggle.render()
    
    main()

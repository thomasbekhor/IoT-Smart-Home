
import json
import streamlit as st

from Sidebar import Sidebar

from Page import Page
from FloorPlan import FloorPlan
from MyRoom import MyRoom
from Settings import Settings


class MyHome():
    def __init__(self):
        self.data = self.readDatabase()
        self.room_names = [room["name"] for room in self.data["MyHome"]]

        if "selected" not in st.session_state:
            st.session_state["selected"] = "Home"
        self.selected = st.session_state["selected"]

        if "debug_mode" not in st.session_state:
            st.session_state["debug_mode"] = False
        
        # self.debug = st.session_state["debug_mode"]


    def readDatabase(self):
        with open("./db/dbV3.json", "r") as file:
            data = json.load(file)

        return data


    def setSidebar(self):
        sidebar = Sidebar(
            title="My Home",
            components=self.room_names
        )

        return sidebar


    def mainPage(self):
        mainBody = FloorPlan("My Home", 6, 6)
        mainBody.add_room(0, 5, 0, 5)
        mainBody.add_room(2, 3, 0, 1)
        mainBody.add_room(0, 3, 4, 5)
        mainBody.add_room(4, 5, 0, 2)
        mainBody.add_room(4, 5, 3, 5)

        return Page(mainBody, self.setSidebar())


    def roomPage(self):
        index = next((i for i, room in enumerate(self.data["MyHome"]) if room["name"] == self.selected), -1)
        room = self.data["MyHome"][index]

        roomBody = MyRoom(room["name"], room)

        return Page(roomBody, self.setSidebar())


    def settingsPage(self):
        settings = Settings("Settings", debug=st.session_state["debug_mode"])

        return Page(settings, self.setSidebar())


    def render(self):
        # if self.debug:
            # print(self.selected)


        if self.selected == "Home":
            page = self.mainPage()

        elif self.selected == "Settings":
            page = self.settingsPage()

        else:
            page = self.roomPage()

        new_selection = page.render()
        if new_selection != self.selected:
            st.session_state["selected"] = new_selection
            st.rerun()  # 🚀 Correto na versão atual do Streamlit


if __name__ == "__main__":
    myHome = MyHome()
    myHome.render()



import streamlit as st

class Page():
    def __init__(self, body, sidebar):
        self.body = body
        self.sidebar = sidebar
        # self.title = title

    def render(self):
        self.body.render()
        selected = self.sidebar.render()
        return selected


if __name__ == "__main__":
    from Sidebar import Sidebar
    from FloorPlan import FloorPlan

    MyRoom = FloorPlan("My Home", 6, 6)
    MyRoom.add_room(0, 5, 0, 5)
    MyRoom.add_room(2, 3, 0, 1)
    MyRoom.add_room(0, 3, 4, 5)
    MyRoom.add_room(4, 5, 0, 2)
    MyRoom.add_room(4, 5, 3, 5)

    sidebar = Sidebar(
        title="My Home",
        components=["Room 1", "Room 2", "Room 3"],
        debug=True
    )


    mainPage = Page(MyRoom, sidebar)
    currRoom = mainPage.render()

    print(currRoom)
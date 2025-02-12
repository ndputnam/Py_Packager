unused_button = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 3px solid lightblue;
        border-radius: 15px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: green;
    }
    QPushButton:pressed {
        background-color: yellow;
    }
"""

need_unused_button = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 4px solid blue;
        border-radius: 15px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: green;
    }
    QPushButton:pressed {
        background-color: yellow;
    }
"""

used_button = """
    QPushButton {
        background-color: teal;
        color: white;
        border: 2px solid green;
        border-radius: 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: green;  
    }
    QPushButton:pressed {
        background-color: yellow;
    }
"""

unused_console = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 3px solid yellow;
        border-radius: 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: yellow;
    }
    QPushButton:pressed {
        background-color: orange;
    }
"""

used_console = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 3px solid green;
        border-radius: 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: green;
    }
    QPushButton:pressed {
        background-color: orange;
    }
"""

saved_button = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 5px solid green;
        border-radius: 15px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: green;
    }
    QPushButton:pressed {
        background-color: yellow;
    }
"""

not_saved_button = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 5px solid red;
        border-radius: 15px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: red;
    }
    QPushButton:pressed {
        background-color: yellow;
    }
"""

running_button = """
    QPushButton {
        background-color: aqua;
        color: black;
        border: 5px solid blue;
        border-radius: 0px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: blue;
    }
    QPushButton:pressed {
        background-color: yellow;
    }
"""
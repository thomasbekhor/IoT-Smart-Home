import streamlit as st

# ───────────────────────────────────────────────
# Floor‑plan class
# ───────────────────────────────────────────────
class FloorPlan:
    def __init__(self, title, rows, cols, cell_h=60, gap=4):
        self.title = title

        self.rows   = rows
        self.cols   = cols
        self.cell_h = cell_h          # px
        self.gap    = gap             # px
        self.rooms  = []              # list of dicts

    def add_room(self, xi, xf, yi, yf):
        assert 0 <= xi <= xf < self.cols
        assert 0 <= yi <= yf < self.rows
        self.rooms.append(dict(xi=xi, xf=xf, yi=yi, yf=yf))

    # ───────────────────────────────────────────
    # Render
    # ───────────────────────────────────────────
    def render(self):
        st.title(self.title)

        # ---------- base CSS ----------
        st.markdown(
            f"""
            <style>
            .grid {{
                display: grid;
                grid-template-columns: repeat({self.cols}, 1fr);
                grid-template-rows: repeat({self.rows}, {self.cell_h}px);
                gap: {self.gap}px;
            }}
            .cell-placeholder {{
                width: 100%; height: 100%;
            }}
            .room-block {{
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid #555;      /* outline only */
                border-radius: 6px;
                background: transparent;     /* no fill */
                font-weight: 600;
                color: #444;
                padding: 4px;
                text-align: center;
                user-select: none;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # ---------- HTML grid ----------
        html = ['<div class="grid">']

        # 1. Invisible placeholders keep the base 6×6 shape
        html += ['<div class="cell-placeholder"></div>'
                 for _ in range(self.rows * self.cols)]

        # 2. Overlay every declared room
        for r in self.rooms:
            col_start = r["xi"] + 1
            col_end   = r["xf"] + 2
            row_start = r["yi"] + 1
            row_end   = r["yf"] + 2
            html.append(
                f"""<div class="room-block"
                        style="
                            grid-column:{col_start}/{col_end};
                            grid-row:{row_start}/{row_end};">
                    </div>"""           #  ←  no label inside
            )

        html.append("</div>")
        st.markdown("".join(html), unsafe_allow_html=True)


# ───────────────────────────────────────────────
# Example usage
# ───────────────────────────────────────────────
if __name__ == "__main__":
    fp = FloorPlan("My Home", 6, 6)

    #           xi xf yi yf
    fp.add_room(0, 5, 0, 5)
    fp.add_room(2, 3, 0, 1)
    fp.add_room(0, 3, 4, 5)
    fp.add_room(4, 5, 0, 2)
    fp.add_room(4, 5, 3, 5)

    fp.render()

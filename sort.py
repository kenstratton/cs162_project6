import tkinter as tk
import random as rn
from tkinter.constants import NUMERIC


# W = Width, H = Height, X/Y = X/Y coords, S = Space, T = Vertex coord,
# C = Color, LEN = Length, L = Limit, F = Font
WINDOW_W = 700
WINDOW_H = 550

# Variables for canvas
CANVAS_C = "#000000"
OUTLINE_C = "#eeeeee"

# Variables for rectangles of 100 int values
RECT_W = 5
RECT_H = 3
RECT_X = (WINDOW_W-RECT_W*100)/2
RECT_Y = (WINDOW_H+RECT_H*100)/2
PIVOT_C = "red"
CAND_C = "#ffffff"
SWAP_C = "lightgreen"

# Variables for menus (a start button , a jumble button, and a text saying done)
BTN_W = 5
BTN_C = "#ffffff"
BTN_TXT_C = "#333333"
BTN_F = ("Helvetica", 14)
TXT_F = ("Helvetica", 10)

START_X = WINDOW_W-(BTN_W*16)*2-90
JUMBLE_X = WINDOW_W-(BTN_W*16)-75
DONE_X = WINDOW_W-40
MENU_Y = 10

# Variables for a speed controller
CNTLR_W = 25
CNTLR_H = 10
METER_T = 70
METER_LEN = 100
SPEED = 500
SPEED_L = 10
SPEED_S = 1490

CNTLR_S = 25
CNTLR_X = WINDOW_W-CNTLR_S-CNTLR_W
CNTLR_Y = METER_T + (SPEED-SPEED_L)/SPEED_S*METER_LEN
METER_X = WINDOW_W-CNTLR_S-CNTLR_W/2
METER_Y = METER_T+CNTLR_H/2
FAST_TXT_Y = METER_T-CNTLR_H
SLOW_TXT_Y = METER_T+METER_LEN+20

# A list for a collection of 1~100 int values
COL = []
for i in range(100):
    COL.append(i+1)

# Id of an ongoing after method
AFTER_ID = None

# Records of sorting
RECORD =[]


# [CLASS] Speed Controller
class SpeedController:
    def __init__(self, canvas):
        self.canvas = canvas

        # Y of a mouse cursor and a controller
        self.mouse_y = None
        self.cntlr_y = CNTLR_Y

        # Draws a speed meter
        canvas.create_text(METER_X, FAST_TXT_Y, text="Fast", fill=OUTLINE_C)
        canvas.create_text(METER_X, SLOW_TXT_Y, text="Slow", fill=OUTLINE_C)
        canvas.create_line(
            METER_X,
            METER_Y,
            METER_X,
            METER_Y+METER_LEN,
            fill=OUTLINE_C
        )
        # Draws a speed controller
        canvas.create_rectangle(
            CNTLR_X,
            CNTLR_Y,
            CNTLR_X+CNTLR_W,
            CNTLR_Y+CNTLR_H,
            width=1,
            tag="cntlr_bar",
            fill=CANVAS_C
        )

        # Event handlers for clicking, moving, and releasing a controller
        canvas.tag_bind("cntlr_bar", "<Button-1>", self.cntlr_click)
        canvas.tag_bind("cntlr_bar", "<B1-Motion>", self.cntlr_move)
        canvas.tag_bind("cntlr_bar", "<ButtonRelease-1>", self.cntlr_stop)

    # Gets Y of a mouse cursor
    def cntlr_click(self, evnt):
        self.mouse_y = evnt.y_root

    # Moves Y of a controller the same distance of a moved cursor
    def cntlr_move(self, evnt):
        dst = evnt.y_root - self.mouse_y
        new_pos = self.cntlr_y+dst
        # Speed adjustment works when the moved Y of a controller meets a meter scale
        if 0 <= new_pos-METER_T <= METER_LEN:
            self.canvas.moveto("cntlr_bar", CNTLR_X, new_pos)
            self.change_animation_speed(new_pos)

    # Initializes Y of a cursor and resets Y of a controller (instance properties)
    def cntlr_stop(self, evnt):
        self.mouse_y = None
        pos = self.canvas.bbox("cntlr_bar")
        self.cntlr_y = pos[1]  # Insert Y of the moved bar

    # Adjusts the SPEED variable based on the chaged Y of a controller
    def change_animation_speed(self, change):
        global SPEED
        change_rate = float((change-METER_T)/METER_LEN)
        SPEED = int(SPEED_L + (SPEED_S*change_rate))


# [CLASS] Draw a canvas and its elements
class Canvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root, width=WINDOW_W, height=WINDOW_H, bg=CANVAS_C)
        self.place(x=0, y=0)

        self.root = root
        self.rect_ids =[]
        self.cntlr = SpeedController(self)

        # Rectangles for 100 values
        for i in range(len(COL)):
            self.rect_ids.append(self.create_rectangle(
                RECT_X+RECT_W*i,
                RECT_Y-RECT_H*COL[i],
                RECT_X+RECT_W*(i+1),
                RECT_Y,
                width=1,
                outline=OUTLINE_C,
                disabledfill=CANVAS_C,
                state=tk.DISABLED,
                tag="rect"
            ))
        # Text to tell completion of processing
        self.create_text(
            DONE_X, MENU_Y*2,
            text="*Completed!",
            font=TXT_F,
            activefill=OUTLINE_C,
            disabledfill=CANVAS_C,
            state=tk.DISABLED,
            tag="comp"
        )

    # disable/activate: used to activate activefill or disabledfill of a element
    def disable(self, id_or_tag):
        self.itemconfig(id_or_tag, state=tk.DISABLED)

    def activate(self, id_or_tag):
        self.itemconfig(id_or_tag, state=tk.NORMAL)

    def change_rect_height(self, i, y):   # Change only the y coordinate of a element
        self.coords(self.rect_ids[i], RECT_X+RECT_W*i, y, RECT_X+RECT_W*(i+1), RECT_Y)

    def change_rect_color(self, i=None, color=None):
        if i:
            self.itemconfig(self.rect_ids[i], fill=color)
        else:
            self.itemconfig("rect", fill=CAND_C)

    def set_animation(self):
        self.disable("rect")
        if not RECORD:
            self.activate("comp")
            return
        record = RECORD[0]
        RECORD.pop(0)
        pivot = record["pivot"]
        for i in range(record["l_side"], record["r_side"]+1):
            self.activate(self.rect_ids[i])
        self.highlight(record, pivot)

    def highlight(self, record, p):
        l = record["l"][0]
        r = record["r"][0]
        record["l"].pop(0)
        record["r"].pop(0)
        self.change_rect_color()
        self.change_rect_color(l, SWAP_C)
        self.change_rect_color(r, SWAP_C)
        self.change_rect_color(p, PIVOT_C)
        global AFTER_ID
        AFTER_ID = self.root.after(SPEED, self.swap, record, l, r, p)

    def swap(self, record, l, r, p):
        if l == p:
            self.change_rect_color(l, SWAP_C)
            self.change_rect_color(r, PIVOT_C)
            p = r
        elif r == p:
            self.change_rect_color(r, SWAP_C)
            self.change_rect_color(l, PIVOT_C)
            p = l
        
        pos_l = self.bbox(self.rect_ids[l])
        pos_r = self.bbox(self.rect_ids[r])
        self.change_rect_height(l, pos_r[1]+1)
        self.change_rect_height(r, pos_l[1]+1)
        global AFTER_ID
        if record["l"]:
            AFTER_ID = self.root.after(SPEED, self.highlight, record, p)
        else:
            AFTER_ID = self.root.after(SPEED, self.set_animation)
    """
    Animation Flow:
        set_animation ▷ highlight = (recursive) = swap ▷ set_animation
    Structure of RECORD:
        [ { "pivot": _ , "l_side": _ , "r_side":_ , "l":[], "r":[] }, ... ]
        ◆ Each dictionary in RECORD is content at one pivot-based sorting 
    set_animation():
        ・Pulls out one front record from RECORD (No record in RECORD -> done)
        ・Decides a candidate scale by "l_side" and "r_side"
        ・Throws the record and its pivot to highlight()
    highlight():
        ・Pulls out location info of one swapping from the record ("l" and "r")
        ・Highlights rectangles relating to the positions and the pivot
        ・Throws the record, ("l" and "r"), and pivot to swap()
    swap():
        ・Resizes two rectangles at the locations subject to the swapping
        ・If the pivot itself is swapped, updates its info with a new location
        ・With any other swapping info in the record, throws the record and the current pivot info to highlight()
        ・Without any more swapping info in the record, goes back set_animation()
    """


# [CLASS] Sets up a tkinter and a sorting program
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.title("Quick Sort")
        self.canvas = Canvas(self)

        self.btn_start = tk.Button(
            self, width=5,
            highlightbackground=BTN_C,
            foreground=BTN_TXT_C,
            font=BTN_F,
            text="Start",
            command=self.process
        )
        self.btn_jumble = tk.Button(
            self, width=5,
            highlightbackground=BTN_C,
            foreground=BTN_TXT_C,
            font=BTN_F,
            text="Jumble",
            command=self.jumble
        )
        self.btn_start.place(x=START_X, y=MENU_Y)
        self.btn_jumble.place(x=JUMBLE_X, y=MENU_Y)

    def process(self):
        self.btn_start.config(state=tk.DISABLED)
        quick_sort(0, len(COL)-1)
        self.canvas.set_animation()

    def jumble(self):
        self.reset()
        jumble_a_collection()
        for i in range(len(COL)):  # Resize each rectangle based on the mixed collection
            self.canvas.change_rect_height(i, RECT_Y-RECT_H*COL[i])

    # Stop the ongoing processing and initialize data it has updated
    def reset(self):
        global RECORD
        if AFTER_ID:
            NUM = 0
            RECORD.clear()
            self.after_cancel(AFTER_ID)
            self.btn_start.config(state=tk.NORMAL)
            self.canvas.itemconfig("rect", state=tk.DISABLED)
            self.canvas.itemconfig("comp", state=tk.DISABLED)


# [FUNCTION] Sorting Method
def quick_sort(left, right):
    global COL, RECORD
    if (right - left < 1):
       return

    pivot_idx = (left + right) // 2   # Decide an index of a new pivot
    pivot = COL[pivot_idx]
    l = left
    r = right
    RECORD.append({"pivot":pivot_idx, "l_side":l, "r_side":r, "l":[], "r":[]})

    # Swap a left-side value >= the pivot for a right-side value <= the pivot
    while True:
        for _ in range(l, right+1):
            if COL[l] >= pivot:
               break
            l+=1
        for _ in range(left, r+1):
            if COL[r] <= pivot:
               break
            r-=1
        if l == r:
            if not RECORD[len(RECORD)-1]["l"]: # Without swapping, pass recording
                RECORD.pop(len(RECORD)-1)
            break
        else:
            RECORD[len(RECORD)-1]["l"].append(l)
            RECORD[len(RECORD)-1]["r"].append(r)
            COL[l], COL[r] = COL[r], COL[l]

    quick_sort(left, r-1);   # A lift half (< pivot)
    quick_sort(r+1, right);    # A right half (> pivot)


# [FUNCTION] Sets up a collction of 1~100 int values
def jumble_a_collection():
    global COL
    for i in range(len(COL)):
        ii = rn.randint(0, len(COL)-1-i)
        COL.append(COL[ii])
        COL.pop(ii)
    return COL


if __name__ == "__main__":
    jumble_a_collection()
    app = Application()
    app.mainloop()
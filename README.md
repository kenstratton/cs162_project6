# Project 6 (Sorting)
**Tools :**</br>
・python 3.10.0</br>
・tkinter 8.6.11</br>
・pytest 6.2.5

**Quick Sort?** [- Wikipedia](https://en.wikipedia.org/wiki/Quicksort)</br> 
Quicksort is a divide-and-conquer algorithm. It works by selecting a 'pivot' element from the array and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot.

**How to implement Quick Sort in my program** </br>
・Prepare a list of candidate values which are randomly arranged. </br>
・Repeat the following steps until the values are sorted in ascending order:
1. Decide a candidate scale and a 'pivot' in the scale.
2. Search a value >= the 'pivot' from the right side of the scale and a value <= the 'pivot' from the left side (including 'pivot' itself).
3. If the position of the value from the right side of the scale is < that from the left side, swap their positons. Otherwise, no swapping occurred.
4. With a swapping, go back to Step 2. Without it, go to Step 5. 
5. Decide two new scales from the right side of the original scale to the point just before the 'pivot' and from the left side to the point just after the 'pivot', and go the following with each scale:
    1. If the right side and the left side of the new scale are lost or qual, there is no more progress with the scale. 
    2. Otherwise, go back and execute Step 1 with the scale.

**Performance of My Quick Sort :**</br>
\* Pivot = 3
|4|5|3|1|2|
----|----|----|----|----

▼

|2|5|3|1|4|
----|----|----|----|----

▼

|2|1|3|5|4|
----|----|----|----|----

▼ (Divided to two scales based on the 'pivot')

|2|5|
----|----

|5|4|
----|----

**GUI :**</br>
・The tkinter provides numerous widget classes which help create GUI with thier methods. </br>
・The mainly used widgets for this were Entry, Button, Label, and Canvas. </br>
・The details of how they were used are in explanation for steps of achieving the search system.

![quick_sort_gui_performance](https://user-images.githubusercontent.com/77530003/140919943-aa5a29fe-3624-4909-83a7-0bfbc968d872.gif)

## Each steps to achieve the sorting program
### ▼ Create a collection of 100 int values
・Repeat adding a value plus 1 more than that previously added.

    # sort.py

    COL = []
        for i in range(100):
        COL.append(i+1)

### ▼ Create a GUI to display the collection of int values as rectangles
・Rectangles are created the same number of times as the length of the int-value collection. </br>
・Rectangles -> *.create_rectangle()*, args = starting X, starting Y, ending X, ending Y, options... </br>
・Each number text holds a tag that consists of the tens place from the top layer loop and the ones place from the the second layer.

    # sort.py > Canvasn > .__init__()

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
<img width="350" alt="Screen Shot 2021-11-09 at 23 23 39" src="https://user-images.githubusercontent.com/77530003/140941487-84efbfca-7338-48d8-bb99-cafe9725efc2.png">

### ▼ Include a button to start the sorting process
・The Button widget provides a button to request for sorting.

    # sort.py > Application > .__init__()
    
    self.btn_start = tk.Button(
        self, width=5,
        highlightbackground=BTN_C,
        foreground=BTN_TXT_C,
        font=BTN_F,
        text="Start",
        command=self.process
    )
<img width="350" alt="Screen Shot 2021-11-09 at 23 26 34" src="https://user-images.githubusercontent.com/77530003/140941990-d8b4e0c8-7ee0-4fe3-a234-98c989f9bb1d.png">


### ▼ Highlighting Animation
Canvas class has responsibility for animation.

**Animation Flow:** </br>
set_animation ▷ highlight = (recursive) = swap ▷ set_animation

**Structure of RECORD:** </br>
・List structure: [ { "pivot": _ , "l_side": _ , "r_side":_ , "l":[], "r":[] }, ... ] </br>
・Each dictionary in RECORD is content at one pivot-based sorting.
 
**set_animation():** </br>
・Pulls out one front record from RECORD (No record in RECORD -> done). </br>
・Based on "l_side" and "r_side", decides a candidate scale in which *highlight()* and *swap()* function. </br>
・Throws the record and its pivot to *.highlight()*.
 
    # sort.py > Canvas
     
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
 
**highlight():** </br>
・Pulls out location info of one swapping from the record ("l" and "r"). </br>
・Highlights rectangles relating to a candidate scale, swapped positions, and a pivot. </br>
・Throws the record, ("l" and "r"), and pivot to *.swap()*.
 
    # sort.py > Canvas
 
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

**swap():** </br>
・Resizes two rectangles at the locations subject to the swapping. </br>
・If the pivot itself is swapped, updates its info with a new location. </br>
・With any other swapping info in the record, throws the record and the current pivot info to *.highlight()*. </br>
・Without any more swapping info in the record, goes back *.set_animation()*.

    # sort.py > Canvas
     
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
 ![quick_sort_gui_performance](https://user-images.githubusercontent.com/77530003/140919943-aa5a29fe-3624-4909-83a7-0bfbc968d872.gif)
 
### ▼ Pause after highlighting the candidate value but before moving on
・Pausing was implemented with *.after()* of tkinter.</br>
・Each of the *.highlight()* and *.swap()* has a pausing point at the end that takes some moment progressing.</br>
・There is a speed-controlling slider in a canvas field.</br>
・Moving the slider change the SPEED variable which impacts the pausing time length.</br>
・Update the SPEED by the SpeedController class -> *.change_animation_speed()* 
・Formula to update the SPEED by moving the slider: m-tm + s-scl \* (c-p / c-scl)</br>
\* m-tm = Minimum time length, s-scl = Scale of time length, c-p = Controller position, c-scl = Scale of an area controller is movable

    # sort.py > Canvas > .highlight()

    global AFTER_ID
    AFTER_ID = self.root.after(SPEED, self.swap, record, l, r, p)


    # sort.py > Canvas > .swap()

    global AFTER_ID
    if record["l"]:
        AFTER_ID = self.root.after(SPEED, self.highlight, record, p)
    else:
        AFTER_ID = self.root.after(SPEED, self.set_animation)
  
  
    # sort.py > SpeedController

    def change_animation_speed(self, change):
        global SPEED
        change_rate = float((change-METER_T)/METER_LEN)   # Equals (c-p / c-scl) in the above 
        SPEED = int(SPEED_L + (SPEED_S*change_rate))

### ▼ Make it obvious when it has finished sorting the data set
・When sorting finishes, notification is made as "Completed!". </br>
・Notification text -> *.create_text()* </br>
・*Activefill* turn the text element in another color while it is active. </br>
・The element state is activated by *.activate()*.

    # sort.py > Canvas > .__init__()

    self.create_text(
        DONE_X, MENU_Y*2,
        text="*Completed!",
        font=TXT_F,
        activefill=OUTLINE_C,
        disabledfill=CANVAS_C,
        state=tk.DISABLED,
        tag="comp"
    )


    # sort.py > Canvas
    def activate(self, id_or_tag):
        self.itemconfig(id_or_tag, state=tk.NORMAL)
        

    # sort.py > Canvas > .set_animation()

    if not RECORD:
        self.activate("comp")
        return
<img width="350" alt="Screen Shot 2021-11-10 at 0 23 23" src="https://user-images.githubusercontent.com/77530003/140952545-0627490b-6970-44cb-97ff-ee418573b2b5.png">

## Add tests
### ▼ Kinds of tests to verify the functionality of the sorting program
・It should be necessary to test whether the whole processing is in expected order and gives an appropriate outcome.</br>
・A tester would need prepared data to get output in a supposed situation.</br>

### ▼ Test for Sorting (pytest)
・Test preparation is set by the *.fixture()* decorator which is coded in the conftest.py.</br>
・Install the pytest-mock plugin to use *mock* objects.</br>
・*Mock* helps alter output of methods for a while and test if interdependent methods or classes can properly work.</br>
・Fake a method for specific tests by *mocker* fixture -> *mocker.patch()* , 1st arg = a method path, 2nd = return_value</br>
・Test whether the mocked method has been called only once -> *.assert_called_once_with()*, args = the method path, args of the method...

<img width="1030" alt="Screen Shot 2021-11-10 at 0 39 51" src="https://user-images.githubusercontent.com/77530003/140956446-a5d5e118-545a-4edf-9599-3c20e0c332e2.png">

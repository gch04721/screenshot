from pynput import mouse
import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width =110, height=110)

def on_move(x, y):
    print('pointer moved to {}'.format((x,y)))

def on_click(x,y, button, pressed):
    chk = True
    print('mouse clicked at {}'.format((x,y)))
    x1, y1, x2, y2 = 0,0,0,0
    if mouse.Button.left == button:
        if pressed:
            x1, y1 = x, y
            chk = True
        if not pressed:
            x2, y2 = x,y
            root.quit()
            canvas = tk.Canvas(root, width = abs(x1-x2), height = abs(y1-y2))
            canvas.master.overrideredirect(True)
            canvas.create_rectangle(x1, y1, abs(x1 - x2), abs(y1- y2), fill = 'red')
            
            canvas.pack()
            canvas.mainloop()
        print('left clicked')

    if mouse.Button.right == button:
        root.destroy()
        return False
        
listener = mouse.Listener(on_move = on_move, on_click = on_click)
listener.start()

canvas.pack()
canvas.mainloop()
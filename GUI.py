
import tkinter as tk


def show_color(rgb, advanced: bool = False):
    if advanced:
        def update_hue(degrees):
            r, g, b = rgb_rotate.change_hue(int(degrees))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.config(bg=hex_color)
            canvas.delete("text")
            canvas.create_text(100, 50, text=hex_color, tag="text", fill="white")

        def update_saturation(percentage):
            r, g, b = rgb_rotate.set_saturation(float(percentage))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.config(bg=hex_color)
            canvas.delete("text")
            canvas.create_text(100, 50, text=hex_color, tag="text", fill="white")

        def update_lightness(percentage):
            r, g, b = rgb_rotate.set_lightness(float(percentage))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.config(bg=hex_color)
            canvas.delete("text")
            canvas.create_text(100, 50, text=hex_color, tag="text", fill="white")

        rgb_rotate = RGB(*rgb)
        _, l, s = rgb_rotate.get_hls()

        root = tk.Tk()
        root.title("Hue Rotation")
        root.geometry("400x400")

        canvas_original = tk.Canvas(root, width=200, height=100)
        canvas_original.pack()
        original_hex_color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
        canvas_original.config(bg=original_hex_color)
        canvas_original.delete("text")
        canvas_original.create_text(100, 50, text=original_hex_color, tag="text", fill="white")

        canvas = tk.Canvas(root, width=200, height=100)
        canvas.pack()

        slider_hue = tk.Scale(root, from_=0, to=360, orient="horizontal", command=update_hue)
        slider_hue.pack()
        slider_hue.set(value=0)
        update_hue(degrees=0)

        slider_saturation = tk.Scale(root, from_=0, to=1, resolution=0.01,  orient="horizontal", command=update_saturation)
        slider_saturation.pack()
        slider_saturation.set(value=s)

        slider_lightness = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", command=update_lightness)
        slider_lightness.pack()
        slider_lightness.set(value=l)



        root.mainloop()
    else:
        root = tk.Tk()
        root.title("RGB Color")
        canvas = tk.Canvas(root, width=100, height=100, bg=f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}')
        canvas.pack()
        root.mainloop()

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
from pytube import exceptions, YouTube

# Setting root windows
root = Tk()
root.title("YouTube Downloader")
root.geometry("600x500")
root.iconbitmap(r"C:\Users\qk633\Downloads\youtube.png")
root.configure(background='#5A5A5A')
root.grid_columnconfigure(0, weight=1)

# FONTS
head_font = ("Verdana", 30)
txt_font = ("Monospace", 20)
sm_txt_font = ("Arial", 16)

# backup to original page after downloading
def goBackToStartPage():
    # Clear the widgets created during vidInfo()
    vid_img.grid_forget()
    vid_title.grid_forget()
    vid_len.grid_forget()
    vid_cap.grid_forget()
    vid_auth.grid_forget()
    down_btn.grid_forget()
    back_btn.grid_forget()
    end_lbl.grid_forget()
    clipboard.delete(0, END)

    # Show the clipboard entry and start button again
    clipboard.grid(row=2, column=0, pady=(10, 40))
    start_btn.grid(row=2, column=1, pady=(10, 40), padx=(0, 100))

# creatind download button
def downButton():
    global back_btn, end_lbl
    try:
        down_vid = vid_tube.streams.get_highest_resolution()
        down_vid.download()
        end_lbl = Label(root, text="Video Downloaded Successfully 🥳", font=txt_font, fg='red', bg='yellow')
        end_lbl.grid(row=9, column=0, padx=10, pady=10)
        back_btn = Button(root, text="Go Back ↩", font=sm_txt_font, fg='yellow', bg='brown', padx=20, pady=10, command=goBackToStartPage)
        back_btn.grid(row=9, column=1, padx=(0, 200), pady=10)
        
    #common  error handling        
    except exceptions.AgeRestrictedError:
        messagebox.showerror("Error", "Video is age-restricted ☠️.\nYou need to log in first and verify your age.")
        back_btn()

    except exceptions.VideoUnavailable:
        messagebox.showerror("Error", "Video Unavailable ⚠️")
        back_btn()

    except  exceptions.ExtractError:
        messagebox.showerror("Error", "Video can't be extracted")
        back_btn()

# button for poping up common info about video
def startButton():
    global vid_tube
    url = clipboard.get()
    if url.startswith('http'):
        vid_tube = YouTube(url)
        clipboard.grid_forget()
        start_btn.grid_forget()
        vidInfo()  # Call the vidInfo() function to display video information
    else:
        messagebox.showerror("Error", "Enter the valid URL ❌")
        clipboard.grid(row=2, column=0, pady=(10, 40))
        start_btn.grid(row=2, column=1, pady=(10, 40), padx=(0, 100))

# contain common info about video
def vidInfo():
    global thumbnail_image, vid_img, vid_len, vid_cap, vid_auth, vid_title, down_btn
    title = vid_tube.title
    length = str(int(vid_tube.length // 60)) + ":" + str(int(vid_tube.length % 60)).zfill(2)
    caption = "Not available"  # You can modify this part to extract caption info if needed
    author = vid_tube.author
    thumbnail_url = vid_tube.thumbnail_url

    # Use PIL to open and convert the thumbnail image
    thumbnail_image = Image.open(requests.get(thumbnail_url, stream=True).raw)
    thumbnail_image = thumbnail_image.resize((200, 200), Image.ANTIALIAS)
    thumbnail_image = ImageTk.PhotoImage(thumbnail_image)

    vid_img = Label(root, image=thumbnail_image, width=200, height=200, bd=2)
    vid_img.grid(row=3, column=0, columnspan=2, padx=(0, 10), pady=(20, 20))

    vid_title = Label(root, text=f"Title: {title}", font=sm_txt_font, bg='black', fg='white')
    vid_title.grid(row=4, column=0, columnspan=2, pady=(5, 5))

    vid_len = Label(root, text=f"Length: {length}", font=sm_txt_font, bg='black', fg='white')
    vid_len.grid(row=5, column=0, columnspan=2, pady=(0, 5))

    vid_cap = Label(root, text=f"Caption: {caption}", font=sm_txt_font, bg='black', fg='white')
    vid_cap.grid(row=6, column=0, columnspan=2, pady=(0, 5))

    vid_auth = Label(root, text=f"Author: {author}", font=sm_txt_font, bg='black', fg='white')
    vid_auth.grid(row=7, column=0, columnspan=2, pady=(0, 20))

    down_btn = Button(root, text="Download", font=sm_txt_font, padx=50, pady=12,  bg='#89CFF0', fg='white', command=downButton)
    down_btn.grid(row=8, column=0, columnspan=2, pady=(0, 5))

# setting up the header can preparing page
header = Label(root, text="YouTube Video Downloader", font=head_font, bg='#5A5A5A', fg='white')
header.grid(row=0, column=0, pady=(50, 10))

caption = Label(root, text="Safe, Easy & User-friendly 🤝 YouTube Video Dowloader", font=sm_txt_font, bg='#5A5A5A', fg='bisque')
caption.grid(row=1, column=0, padx=(30, 40))

clipboard = Entry(root, width=50, bd=4, borderwidth=3, bg='white', font=txt_font)
clipboard.grid(row=2, column=0, pady=(10, 40))
clipboard.config(fg='black')

start_btn = Button(root, text="Start", font=sm_txt_font, padx=50, pady=12,  bg='#89CFF0', fg='white', command=startButton)
start_btn.grid(row=2, column=1, pady=(10, 40), padx=(0, 100))

root.mainloop()

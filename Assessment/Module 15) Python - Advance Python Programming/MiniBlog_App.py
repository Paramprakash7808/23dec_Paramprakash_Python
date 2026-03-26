# ================================================================
# MiniBlog - Desktop Blog Application
# Assessment: Module 15 - Advanced Python Programming
#
# PDF Requirements covered:
#   [1] User Post Creation  — name (Entry), title (Entry),
#                             content (Text widget)
#   [2] Save Post to File   — username_title.txt via file handling
#   [3] View Saved Posts    — Listbox to select + display content
#   [4] Basic Error Handling— empty fields, file not found,
#                             messagebox for all errors/success
#   [5] Tkinter GUI         — Entry, Text, Label, Button, Listbox
#   [6] File Handling       — open / write / read
#   [7] Classes & Objects   — User class, Post class
#   [8] Exception Handling  — Try-Except blocks throughout
# ================================================================

import tkinter as tk
from tkinter import messagebox
import os

# ----------------------------------------------------------------
# SECTION 1 — CLASSES & OBJECTS
#   Requirement: "Basic User and Post class"
# ----------------------------------------------------------------

class User:
    """Represents a blog user who authors posts."""

    def __init__(self, name: str):
        self.name = name                    # store the author name

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"User({self.name})"


class Post:
    """Represents a single blog post written by a User."""

    def __init__(self, user: User, title: str, content: str):
        self.user    = user                 # User object (author)
        self.title   = title               # post title string
        self.content = content             # post body string

    def get_filename(self) -> str:
        """
        Build filename in required format: username_title.txt
        Spaces in name/title are replaced with underscores.
        """
        safe_name  = self.user.get_name().strip().replace(" ", "_")
        safe_title = self.title.strip().replace(" ", "_")
        return f"{safe_name}_{safe_title}.txt"

    def formatted_text(self) -> str:
        """Return the full text to be written to the file."""
        return (
            f"Author : {self.user.get_name()}\n"
            f"Title  : {self.title}\n"
            f"{'-' * 40}\n"
            f"{self.content}\n"
        )

    def __str__(self) -> str:
        return f"Post('{self.title}' by {self.user.get_name()})"


# ----------------------------------------------------------------
# SECTION 2 — FILE HANDLING
#   Requirement: "Use file handling to write post content"
#                "Read content from selected file"
# ----------------------------------------------------------------

SAVE_FOLDER = "miniblog_posts"          # all posts saved here


def ensure_folder():
    """Create the save folder if it does not already exist."""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)


def save_post_to_file(post: Post) -> str:
    """
    Write post content to  SAVE_FOLDER/username_title.txt
    Returns the full file path on success.
    Raises ValueError  — if any field is empty.
    Raises IOError     — if the file cannot be written.
    """
    ensure_folder()
    filepath = os.path.join(SAVE_FOLDER, post.get_filename())
    # File Handling — open for writing
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post.formatted_text())
    return filepath


def read_post_from_file(filename: str) -> str:
    """
    Read and return the full text of a saved post file.
    Raises FileNotFoundError — if the file no longer exists.
    Raises IOError           — on any other read error.
    """
    filepath = os.path.join(SAVE_FOLDER, filename)
    # File Handling — open for reading
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_all_saved_posts() -> list:
    """Return a sorted list of all .txt filenames in SAVE_FOLDER."""
    ensure_folder()
    return sorted(
        f for f in os.listdir(SAVE_FOLDER) if f.endswith(".txt")
    )


# ----------------------------------------------------------------
# SECTION 3 — TKINTER GUI
#   Requirement: Entry, Text, Label, Button, Listbox
#                messagebox for errors and success
# ----------------------------------------------------------------

class MiniBlogApp:
    """Main GUI application class for MiniBlog."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MiniBlog")
        self.root.resizable(False, False)
        self._build_gui()
        self._load_post_list()          # populate Listbox on startup

    # ── GUI CONSTRUCTION ────────────────────────────────────────

    def _build_gui(self):
        """Build every widget required by the PDF assessment."""

        PAD = {"padx": 8, "pady": 5}

        # ════════════════════════════════════════
        # LEFT FRAME  —  Create / Save a Post
        # ════════════════════════════════════════
        left = tk.LabelFrame(
            self.root, text=" Create New Post ",
            font=("Helvetica", 10, "bold"), padx=10, pady=10
        )
        left.grid(row=0, column=0, padx=12, pady=10, sticky="nsew")

        # --- Label + Entry: Author Name ---
        tk.Label(left, text="Your Name:", font=("Helvetica", 10))\
            .grid(row=0, column=0, sticky="w", **PAD)
        self.entry_name = tk.Entry(left, width=30, font=("Helvetica", 10))
        self.entry_name.grid(row=0, column=1, **PAD)

        # --- Label + Entry: Post Title ---
        tk.Label(left, text="Post Title:", font=("Helvetica", 10))\
            .grid(row=1, column=0, sticky="w", **PAD)
        self.entry_title = tk.Entry(left, width=30, font=("Helvetica", 10))
        self.entry_title.grid(row=1, column=1, **PAD)

        # --- Label + Text widget: Post Content ---
        # Requirement: "Use GUI input fields (Entry, Text widgets)"
        tk.Label(left, text="Post Content:", font=("Helvetica", 10))\
            .grid(row=2, column=0, sticky="nw", **PAD)
        self.text_content = tk.Text(
            left, width=30, height=9,
            font=("Helvetica", 10), wrap=tk.WORD
        )
        self.text_content.grid(row=2, column=1, **PAD)

        # --- Button: Save Post ---
        tk.Button(
            left, text="Save Post",
            font=("Helvetica", 10, "bold"),
            bg="#27ae60", fg="white", width=22,
            command=self._on_save_post       # calls save handler
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # ════════════════════════════════════════
        # RIGHT FRAME  —  View Saved Posts
        # ════════════════════════════════════════
        right = tk.LabelFrame(
            self.root, text=" View Saved Posts ",
            font=("Helvetica", 10, "bold"), padx=10, pady=10
        )
        right.grid(row=0, column=1, padx=12, pady=10, sticky="nsew")

        # --- Label above Listbox ---
        tk.Label(right, text="Saved Posts:", font=("Helvetica", 10))\
            .grid(row=0, column=0, sticky="w", **PAD)

        # --- Listbox: lists all saved post filenames ---
        # Requirement: "User can select and view previously saved
        #               posts from a dropdown (or Listbox)"
        list_frame = tk.Frame(right)
        list_frame.grid(row=1, column=0, **PAD)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox_posts = tk.Listbox(
            list_frame, width=36, height=6,
            font=("Helvetica", 9),
            yscrollcommand=scrollbar.set,
            selectbackground="#2980b9",
            activestyle="none"
        )
        scrollbar.config(command=self.listbox_posts.yview)
        self.listbox_posts.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Buttons: View Post + Refresh List ---
        btn_row = tk.Frame(right)
        btn_row.grid(row=2, column=0, pady=4)

        tk.Button(
            btn_row, text="View Post",
            font=("Helvetica", 10, "bold"),
            bg="#2980b9", fg="white", width=13,
            command=self._on_view_post       # calls view handler
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            btn_row, text="Refresh",
            font=("Helvetica", 10, "bold"),
            bg="#7f8c8d", fg="white", width=10,
            command=self._load_post_list
        ).pack(side=tk.LEFT, padx=4)

        # --- Label above display area ---
        tk.Label(right, text="Post Content:", font=("Helvetica", 10))\
            .grid(row=3, column=0, sticky="w", **PAD)

        # --- Text widget (read-only): displays selected post ---
        # Requirement: "Read content from selected file and
        #               display in the GUI"
        self.text_display = tk.Text(
            right, width=36, height=9,
            font=("Helvetica", 10), wrap=tk.WORD,
            state=tk.DISABLED,              # read-only
            bg="#f9f9f9"
        )
        self.text_display.grid(row=4, column=0, **PAD)

        # ════════════════════════════════════════
        # STATUS BAR (bottom)
        # ════════════════════════════════════════
        self.var_status = tk.StringVar(value="Welcome to MiniBlog!")
        tk.Label(
            self.root, textvariable=self.var_status,
            anchor="w", relief=tk.SUNKEN,
            font=("Helvetica", 9), bg="#dfe6e9", padx=6
        ).grid(row=1, column=0, columnspan=2, sticky="ew")

    # ── EVENT HANDLERS WITH EXCEPTION HANDLING ──────────────────

    def _on_save_post(self):
        """
        Handle 'Save Post' button click.
        Exception Handling covers:
          - Empty name / title / content  -> ValueError   -> messagebox
          - File write failure            -> IOError      -> messagebox
          - Any unexpected error          -> Exception    -> messagebox
        """
        # --- Try-Except Block ---
        try:
            # Collect values from Entry and Text widgets
            name    = self.entry_name.get().strip()
            title   = self.entry_title.get().strip()
            content = self.text_content.get("1.0", tk.END).strip()

            # Validate — empty field check
            # Requirement: "Handle cases like empty fields"
            if not name:
                raise ValueError("Author name cannot be empty.")
            if not title:
                raise ValueError("Post title cannot be empty.")
            if not content:
                raise ValueError("Post content cannot be empty.")

            # Build User and Post objects
            user = User(name)
            post = Post(user, title, content)

            # Save to file  (username_title.txt)
            filepath = save_post_to_file(post)

            # Clear input fields after successful save
            self.entry_name.delete(0, tk.END)
            self.entry_title.delete(0, tk.END)
            self.text_content.delete("1.0", tk.END)

            # Refresh Listbox so new file appears immediately
            self._load_post_list()

            # Success messagebox
            # Requirement: "Show messages using messagebox"
            messagebox.showinfo(
                "Post Saved",
                f"Post saved successfully!\n\nFile: {os.path.basename(filepath)}"
            )
            self.var_status.set(f"Saved: {os.path.basename(filepath)}")

        except ValueError as ve:
            # Empty field error -> messagebox
            messagebox.showerror("Empty Field", str(ve))
            self.var_status.set(f"Error: {ve}")

        except IOError as ie:
            # File write error -> messagebox
            messagebox.showerror("File Error", f"Could not save post:\n{ie}")
            self.var_status.set("File write error.")

        except Exception as e:
            # Catch-all for unexpected errors -> messagebox
            messagebox.showerror("Error", f"Unexpected error:\n{e}")
            self.var_status.set(f"Error: {e}")

    def _on_view_post(self):
        """
        Handle 'View Post' button click.
        Exception Handling covers:
          - No item selected in Listbox   -> ValueError        -> messagebox
          - File deleted / not found      -> FileNotFoundError -> messagebox
          - Any other read failure        -> IOError           -> messagebox
          - Unexpected errors             -> Exception         -> messagebox
        """
        # --- Try-Except Block ---
        try:
            selection = self.listbox_posts.curselection()

            # Validate — nothing selected in Listbox
            if not selection:
                raise ValueError("Please select a post from the list.")

            filename = self.listbox_posts.get(selection[0])
            content  = read_post_from_file(filename)

            # Display content in the read-only Text widget
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete("1.0", tk.END)
            self.text_display.insert(tk.END, content)
            self.text_display.config(state=tk.DISABLED)

            self.var_status.set(f"Viewing: {filename}")

        except ValueError as ve:
            # Nothing selected -> messagebox
            messagebox.showwarning("No Selection", str(ve))
            self.var_status.set(f"Warning: {ve}")

        except FileNotFoundError:
            # Requirement: "Handle cases like … file not found"
            messagebox.showerror(
                "File Not Found",
                "The selected post file could not be found.\n"
                "It may have been deleted. Refreshing the list."
            )
            self.var_status.set("File not found.")
            self._load_post_list()          # auto-refresh list

        except IOError as ie:
            # Other read errors -> messagebox
            messagebox.showerror("Read Error", f"Could not read file:\n{ie}")
            self.var_status.set("File read error.")

        except Exception as e:
            # Unexpected errors -> messagebox
            messagebox.showerror("Error", f"Unexpected error:\n{e}")
            self.var_status.set(f"Error: {e}")

    # ── HELPERS ─────────────────────────────────────────────────

    def _load_post_list(self):
        """
        Reload the Listbox with all saved .txt post filenames.
        Try-Except included for safety.
        """
        try:
            self.listbox_posts.delete(0, tk.END)
            posts = get_all_saved_posts()

            if posts:
                for filename in posts:
                    self.listbox_posts.insert(tk.END, filename)
                self.var_status.set(f"{len(posts)} post(s) found.")
            else:
                self.listbox_posts.insert(tk.END, "(No posts saved yet)")
                self.var_status.set("No saved posts found.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load post list:\n{e}")


# ----------------------------------------------------------------
# SECTION 4 — MAIN ENTRY POINT
# ----------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app  = MiniBlogApp(root)
    root.mainloop()

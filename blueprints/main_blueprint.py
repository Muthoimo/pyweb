from flask import Blueprint, send_from_directory
main_views = Blueprint("name", __name__)

@main_views.get("/", strict_slashes=False)
def index():
    return "<h2> This is the homepage</h2>"

@main_views.get("/profile<string:username>", strict_slashes=False)
def profile(username):
    return f"<h2> Welcome {username}! This is your profile homepage</h2>"

@main_views.get("/download/<path:filename>", strict_slashes=False)
def download(filename):
    return send_from_directory("/home/kinyua/src/", filename)


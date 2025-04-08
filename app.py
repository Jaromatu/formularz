from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
GENERATED_DIR = "generated_pages"

# Tworzymy folder jeśli nie istnieje
os.makedirs(GENERATED_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        links_raw = request.form.get("links")
        best_games_raw = request.form.get("best_games")

        links = [link.strip() for link in links_raw.splitlines() if link.strip()]
        best_games = [link.strip() for link in best_games_raw.splitlines() if link.strip()][:3]  # max 3

        # Generowanie zawartości HTML
        html_content = render_template("generated_template.html", title=title, description=description, links=links, best_games=best_games)
        # Tworzenie unikalnej nazwy pliku (np. na podstawie daty)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{GENERATED_DIR}/strona_{timestamp}.html"

        # Zapis do pliku
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Przekierowanie do wygenerowanej strony
        return redirect(url_for("preview_page", filename=os.path.basename(filename)))
    return render_template("index.html")

@app.route("/generated/<filename>")
def preview_page(filename):
    filepath = os.path.join(GENERATED_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    return "Plik nie istnieje.", 404

if __name__ == "__main__":
    app.run(debug=True)

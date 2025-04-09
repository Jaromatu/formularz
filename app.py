import logging
logging.basicConfig(level=logging.DEBUG) 

import shutil
from flask import send_file
import datetime
import os


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

@app.route('/download-all')
def download_all():
    # Użyj /tmp jeśli jesteś na Render (zazwyczaj działa dobrze)
    output_dir = "/tmp"
    zip_name = f"generated_pages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_base_path = os.path.join(output_dir, zip_name.replace(".zip", ""))  # bez rozszerzenia

    # Tworzy ZIP z folderu generated_pages
    shutil.make_archive(zip_base_path, 'zip', GENERATED_DIR)

    zip_path = zip_base_path + ".zip"
    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

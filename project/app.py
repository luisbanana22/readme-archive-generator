from flask import Flask, render_template, request, send_from_directory
import os
import zipfile

app = Flask(__name__)
OUTPUT_DIR = "output"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    project_name = request.form["project_name"]
    description = request.form["description"]
    technologies = request.form["technologies"]
    license_text = request.form["license"]

    # Generates README.md
    readme_content = f"# {project_name}\n\n## Descrição\n{description}\n\n## Tecnologias\n{technologies}\n"
    with open(os.path.join(OUTPUT_DIR, "README.md"), "w") as f:
        f.write(readme_content)

    # Generates LICENSE.md
    if license_text:
        with open(os.path.join(OUTPUT_DIR, "LICENSE.md"), "w") as f:
            f.write(license_text)

    # Makes zip archive
    zip_path = os.path.join(OUTPUT_DIR, "markdown_files.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file_name in os.listdir(OUTPUT_DIR):
            if file_name != "markdown_files.zip":
                zipf.write(os.path.join(OUTPUT_DIR, file_name), file_name)

    return send_from_directory(OUTPUT_DIR, "markdown_files.zip", as_attachment=True)

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


from jinja2 import Environment, FileSystemLoader
import json

# Load data
with open("data/data.json") as f:
    data = json.load(f)

# Create Jinja2 environment
env = Environment(loader=FileSystemLoader("templates/"))

# Load template
template = env.get_template("index.html")

# Render template with data
html = template.render(data=data)

# Save to file
with open("index.html", "w") as f:
    f.write(html)

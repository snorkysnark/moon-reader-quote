from pathlib import Path
import subprocess
import shutil

npm_prefix = str(Path("./moon-quote-js"))
subprocess.run(["npm", "install", "--prefix", npm_prefix])
subprocess.run(["npm", "run", "--prefix", npm_prefix, "build"])


Path("./static").mkdir(exist_ok=True)
shutil.copyfile(
    Path("./moon-quote-js/dist/moon-quote.es.js"),
    Path("./static/moon-quote.es.js"),
)

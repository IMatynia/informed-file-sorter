import subprocess
import os
from typing import Optional


def pngify(filename: str):
    components = filename.split(".")
    if components[-1] == "webp":
        return ".".join(components[:-1]) + ".png"
    else:
        return filename


def ffmpeg_conversion_from_webp_to_png(folder, filename, args=None) -> Optional[str]:
    pngified = pngify(filename)
    if pngified == filename:
        return None
    command = [
        "ffmpeg",
        "-i",
        os.path.join(folder, filename),
        "-y",
        os.path.join(folder, pngified)
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as er:
        print(er.output)
        return

    os.remove(f"{os.path.join(folder, filename)}")
    return os.path.join(folder, pngified)

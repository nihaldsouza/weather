#!/usr/bin/env python3
"""Generate demo.gif from four layout renders."""
import subprocess
import sys
import os
import tempfile
import shutil

def run(cmd, check=True):
    """Run shell command."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"ERROR: {' '.join(cmd.split()[:3])}")
        print(result.stderr)
        sys.exit(1)
    return result

def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Capture four layouts
        layouts = ['full', 'half_horizontal', 'half_vertical', 'quadrant']
        for i, layout in enumerate(layouts, 1):
            run(f"curl -s http://localhost:4567/render/{layout}.png > {tmpdir}/{i}_{layout}.png")
            print(f"✓ {layout}")

        # Create concat file
        concat_file = f"{tmpdir}/concat.txt"
        with open(concat_file, 'w') as f:
            for i, layout in enumerate(layouts, 1):
                f.write(f"file '{tmpdir}/{i}_{layout}.png'\n")
                f.write("duration 2\n")

        # Generate palette
        run(f"ffmpeg -f concat -safe 0 -i {concat_file} "
            f"-vf 'fps=10,scale=800:480:force_original_aspect_ratio=decrease' "
            f"-c:v png {tmpdir}/palette.png -y 2>/dev/null", check=False)

        # Create GIF
        out_gif = "docs/demo.gif"
        run(f"ffmpeg -f concat -safe 0 -i {concat_file} "
            f"-vf 'fps=10,scale=800:480:force_original_aspect_ratio=decrease,"
            f"split[x][z]; [x]palettegen[p]; [z][p]paletteuse' "
            f"{out_gif} -y 2>/dev/null")

        size_kb = os.path.getsize(out_gif) / 1024
        print(f"✓ {out_gif} ({size_kb:.0f}KB)")

if __name__ == '__main__':
    main()

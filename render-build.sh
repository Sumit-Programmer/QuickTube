#!/bin/bash
# Install FFmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ
mv ffmpeg-*-static/ffmpeg /usr/local/bin/
mv ffmpeg-*-static/ffprobe /usr/local/bin/
chmod +x /usr/local/bin/ffmpeg
chmod +x /usr/local/bin/ffprobe

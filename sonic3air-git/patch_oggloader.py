#!/usr/bin/env python3
import sys

filepath = 'librmx/source/rmxext_oggvorbis/OggLoader.cpp'

with open(filepath, 'rb') as f:
    content = f.read()

# Add include string.h
if b'#include <string.h>' not in content:
    content = content.replace(
        b'#include "../rmxext_oggvorbis.h"',
        b'#include <string.h>\r\n#include "../rmxext_oggvorbis.h"'
    )

# Replace constructor body
target = b'''OggLoader::OggLoader()\r
{\r
\togg_sync_init(&mSyncState);\r
\togg_stream_clear(&mVorbisStreamState);\r
\tvorbis_block_clear(&mVorbisBlock);\r
\tvorbis_dsp_clear(&mVorbisDspState);\r
\tvorbis_comment_clear(&mVorbisComment);\r
\tvorbis_info_clear(&mVorbisInfo);\r
}'''

replacement = b'''OggLoader::OggLoader()\r
{\r
\tmemset(&mSyncState, 0, sizeof(mSyncState));\r
\tmemset(&mVorbisStreamState, 0, sizeof(mVorbisStreamState));\r
\tmemset(&mVorbisBlock, 0, sizeof(mVorbisBlock));\r
\tmemset(&mVorbisDspState, 0, sizeof(mVorbisDspState));\r
\tmemset(&mVorbisComment, 0, sizeof(mVorbisComment));\r
\tmemset(&mVorbisInfo, 0, sizeof(mVorbisInfo));\r
\r
\togg_sync_init(&mSyncState);\r
}'''

if target in content:
    content = content.replace(target, replacement)
    print("Successfully patched OggLoader.cpp")
else:
    # Try with LF line endings in case git checks out as LF
    target_lf = target.replace(b'\r\n', b'\n')
    replacement_lf = replacement.replace(b'\r\n', b'\n')
    if target_lf in content:
        content = content.replace(target_lf, replacement_lf)
        print("Successfully patched OggLoader.cpp (LF endings)")
    else:
        print("Error: Target constructor block not found in OggLoader.cpp!")
        sys.exit(1)

with open(filepath, 'wb') as f:
    f.write(content)

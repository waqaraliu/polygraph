#pragma once

#include <stdio.h>
#include <stdbool.h>

#include <linux/videodev2.h>

#include "../libs/tools.h"
#include "../libs/logging.h"
#include "../libs/frame.h"
#include "../libs/unjpeg.h"

#include "data/blank_jpeg.h"


frame_s *blank_frame_init(const char *path);

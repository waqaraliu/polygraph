#pragma once

#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <setjmp.h>
#include <assert.h>

#include <sys/types.h>

#include <jpeglib.h>
#include <linux/videodev2.h>

#include "logging.h"
#include "frame.h"


int unjpeg(const frame_s *src, frame_s *dest, bool decode);

#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <limits.h>
#include <getopt.h>
#include <errno.h>
#include <assert.h>

#include "../libs/config.h"
#include "../libs/logging.h"
#include "../libs/process.h"
#include "../libs/frame.h"
#include "../libs/memsink.h"
#include "../libs/options.h"

#include "device.h"
#include "encoder.h"
#include "blank.h"
#include "stream.h"
#include "http/server.h"
#ifdef WITH_GPIO
#	include "gpio/gpio.h"
#endif


typedef struct {
	unsigned	argc;
	char		**argv;
	char		**argv_copy;
	frame_s		*blank;
	memsink_s	*sink;
	memsink_s	*raw_sink;
#	ifdef WITH_OMX
	memsink_s	*h264_sink;
#	endif
} options_s;


options_s *options_init(unsigned argc, char *argv[]);
void options_destroy(options_s *options);

int options_parse(options_s *options, device_s *dev, encoder_s *enc, stream_s *stream, server_s *server);

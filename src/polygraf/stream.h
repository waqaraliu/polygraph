#pragma once

#include <stdlib.h>
#include <stdbool.h>
#include <stdatomic.h>
#include <unistd.h>
#include <errno.h>
#include <assert.h>

#include <pthread.h>
#include <linux/videodev2.h>

#include "../libs/tools.h"
#include "../libs/threading.h"
#include "../libs/logging.h"
#include "../libs/frame.h"
#include "../libs/memsink.h"

#include "blank.h"
#include "device.h"
#include "encoder.h"
#include "workers.h"
#ifdef WITH_OMX
#	include "h264/stream.h"
#endif
#ifdef WITH_GPIO
#	include "gpio/gpio.h"
#endif


typedef struct {
	frame_s			*frame;
	unsigned		captured_fps;
	atomic_bool		updated;
	pthread_mutex_t	mutex;

	atomic_bool		has_clients; // For slowdown
} video_s;

typedef struct {
	video_s		*video;
	long double	last_as_blank_ts;

#	ifdef WITH_OMX
	h264_stream_s *h264;
#	endif

	atomic_bool stop;
} stream_runtime_s;

typedef struct {
	device_s	*dev;
	encoder_s	*enc;

	frame_s		*blank;
	int			last_as_blank;
	bool		slowdown;
	unsigned	error_delay;

	memsink_s	*sink;
	memsink_s	*raw_sink;

#	ifdef WITH_OMX
	memsink_s	*h264_sink;
	unsigned	h264_bitrate;
	unsigned	h264_gop;
#	endif

	stream_runtime_s *run;
} stream_s;


stream_s *stream_init(device_s *dev, encoder_s *enc);
void stream_destroy(stream_s *stream);

void stream_loop(stream_s *stream);
void stream_loop_break(stream_s *stream);

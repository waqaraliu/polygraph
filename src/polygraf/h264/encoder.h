/*****************************************************************************
#                                                                            #
#    uStreamer - Lightweight and fast MJPG-HTTP streamer.                    #
#                                                                            #
#    Copyright (C) 2018-2021  Maxim Devaev <mdevaev@gmail.com>               #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or       #
#    (at your option) any later version.                                     #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU General Public License for more details.                            #
#                                                                            #
#    You should have received a copy of the GNU General Public License       #
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.  #
#                                                                            #
*****************************************************************************/


#pragma once

#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#include <linux/videodev2.h>

#include <interface/mmal/mmal.h>
#include <interface/mmal/mmal_format.h>
#include <interface/mmal/util/mmal_default_components.h>
#include <interface/mmal/util/mmal_component_wrapper.h>
#include <interface/mmal/util/mmal_util_params.h>
#include <interface/vcsm/user-vcsm.h>

#include "../../libs/tools.h"
#include "../../libs/logging.h"
#include "../../libs/frame.h"
#include "../encoders/omx/vcos.h"


typedef struct {
	unsigned bitrate; // Kbit-per-sec
	unsigned gop; // Interval between keyframes
	unsigned fps;

	MMAL_WRAPPER_T		*wrapper;
	MMAL_PORT_T			*input_port;
	MMAL_PORT_T			*output_port;
	VCOS_SEMAPHORE_T	handler_sem;
	bool				i_handler_sem;

	int last_online;

	unsigned	width;
	unsigned	height;
	unsigned	format;
	unsigned	stride;
	bool		zero_copy;
	bool		ready;
} h264_encoder_s;


h264_encoder_s *h264_encoder_init(unsigned bitrate, unsigned gop, unsigned fps);
void h264_encoder_destroy(h264_encoder_s *enc);

bool h264_encoder_is_prepared_for(h264_encoder_s *enc, const frame_s *frame, bool zero_copy);
int h264_encoder_prepare(h264_encoder_s *enc, const frame_s *frame, bool zero_copy);
int h264_encoder_compress(h264_encoder_s *enc, const frame_s *src, int src_vcsm_handle, frame_s *dest, bool force_key);

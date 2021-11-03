#include "blank.h"


static frame_s *_init_internal(void);
static frame_s *_init_external(const char *path);


frame_s *blank_frame_init(const char *path) {
	frame_s *blank = NULL;

	if (path && path[0] != '\0') {
		blank = _init_external(path);
	}

	if (blank) {
		LOG_INFO("Using external blank placeholder: %s", path);
	} else {
		blank = _init_internal();
		LOG_INFO("Using internal blank placeholder");
	}
	return blank;
}

static frame_s *_init_internal(void) {
	frame_s *blank = frame_init();
	frame_set_data(blank, BLANK_JPEG_DATA, BLANK_JPEG_DATA_SIZE);
	blank->width = BLANK_JPEG_WIDTH;
	blank->height = BLANK_JPEG_HEIGHT;
	blank->format = V4L2_PIX_FMT_JPEG;
	return blank;
}

static frame_s *_init_external(const char *path) {
	FILE *fp = NULL;

	frame_s *blank = frame_init();
	blank->format = V4L2_PIX_FMT_JPEG;

	if ((fp = fopen(path, "rb")) == NULL) {
		LOG_PERROR("Can't open blank placeholder '%s'", path);
		goto error;
	}

#	define CHUNK_SIZE ((size_t)(100 * 1024))
	while (true) {
		if (blank->used + CHUNK_SIZE >= blank->allocated) {
			frame_realloc_data(blank, blank->used + CHUNK_SIZE * 2);
		}

		size_t readed = fread(blank->data + blank->used, 1, CHUNK_SIZE, fp);
		blank->used += readed;

		if (readed < CHUNK_SIZE) {
			if (feof(fp)) {
				break;
			} else {
				LOG_PERROR("Can't read blank placeholder");
				goto error;
			}
		}
	}
#	undef CHUNK_SIZE

	frame_s *decoded = frame_init();
	if (unjpeg(blank, decoded, false) < 0) {
		frame_destroy(decoded);
		goto error;
	}
	blank->width = decoded->width;
	blank->height = decoded->height;
	frame_destroy(decoded);

	goto ok;

	error:
		frame_destroy(blank);
		blank = NULL;

	ok:
		if (fp) {
			fclose(fp);
		}

	return blank;
}

#pragma once

#include <errno.h>

#include <sys/ioctl.h>

#include "../libs/tools.h"
#include "../libs/logging.h"


#ifndef CFG_XIOCTL_RETRIES
#	define CFG_XIOCTL_RETRIES 4
#endif
#define XIOCTL_RETRIES ((unsigned)(CFG_XIOCTL_RETRIES))


INLINE int xioctl(int fd, int request, void *arg) {
	int retries = XIOCTL_RETRIES;
	int retval = -1;

	do {
		retval = ioctl(fd, request, arg);
	} while (
		retval
		&& retries--
		&& (
			errno == EINTR
			|| errno == EAGAIN
			|| errno == ETIMEDOUT
		)
	);

	// cppcheck-suppress knownConditionTrueFalse
	if (retval && retries <= 0) {
		LOG_PERROR("ioctl(%d) retried %u times; giving up", request, XIOCTL_RETRIES);
	}
	return retval;
}

#include "logging.h"


enum log_level_t us_log_level;

bool us_log_colored;

pthread_mutex_t us_log_mutex;

#pragma once

#include <stdbool.h>
#include <stdatomic.h>

#include <sys/types.h>

#include <pthread.h>

#include "../libs/tools.h"
#include "../libs/threading.h"
#include "../libs/logging.h"


typedef struct worker_sx {
	pthread_t		tid;
	unsigned		number;
	char			*name;

	long double		last_job_time;

	pthread_mutex_t	has_job_mutex;
	void			*job;
	atomic_bool		has_job;
	bool			job_timely;
	bool			job_failed;
	long double		job_start_ts;
	pthread_cond_t	has_job_cond;

	struct worker_sx *prev_wr;
	struct worker_sx *next_wr;

	struct workers_pool_sx *pool;
} worker_s;

typedef void *(*workers_pool_job_init_f)(void *arg);
typedef void (*workers_pool_job_destroy_f)(void *job);
typedef bool (*workers_pool_run_job_f)(worker_s *wr);

typedef struct workers_pool_sx {
	const char		*name;
	long double		desired_interval;

	workers_pool_job_destroy_f	job_destroy;
	workers_pool_run_job_f		run_job;

	unsigned		n_workers;
	worker_s		*workers;
	worker_s		*oldest_wr;
	worker_s		*latest_wr;

	long double		approx_job_time;

	pthread_mutex_t	free_workers_mutex;
	unsigned		free_workers;
	pthread_cond_t	free_workers_cond;

	atomic_bool		stop;
} workers_pool_s;


workers_pool_s *workers_pool_init(
	const char *name, const char *wr_prefix, unsigned n_workers, long double desired_interval,
	workers_pool_job_init_f job_init, void *job_init_arg,
	workers_pool_job_destroy_f job_destroy,
	workers_pool_run_job_f run_job);

void workers_pool_destroy(workers_pool_s *pool);

worker_s *workers_pool_wait(workers_pool_s *pool);
void workers_pool_assign(workers_pool_s *pool, worker_s *ready_wr/*, void *job*/);

long double workers_pool_get_fluency_delay(workers_pool_s *pool, worker_s *ready_wr);

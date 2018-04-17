
#ifndef _CHAOS_CLUSTER_H_
#define _CHAOS_CLUSTER_H_

#include "contiki.h"

typedef uint16_t node_id_t;
typedef uint8_t node_index_t;

#if CHAOS_CLUSTER
    #include "cluster.h"

    #define IS_CLUSTER_JOIN()                    (is_cluster_service_running)
    #define IS_CLUSTER_HEAD_JOIN_ROUND()         (cluster_head_round_initiated)
    #define IS_CLUSTER_HEAD_ROUND()              ((chaos_get_round_number() % 2 == 0 && !is_cluster_join_round && HAS_CLUSTER_ID() && !IS_CLUSTER_JOIN()) || IS_CLUSTER_HEAD_JOIN_ROUND())
    #define IS_SAME_CLUSTER(RECEIVED_CLUSTER_ID) (RECEIVED_CLUSTER_ID == chaos_get_cluster_id() \
                                               || RECEIVED_CLUSTER_ID == 0 \
                                               || chaos_get_cluster_id() == 0)
    #define IS_MAJOR_CLUSTER_HEAD()              (node_id == 1)
    #define IS_CLUSTER_HEAD()                    (node_id == chaos_get_cluster_id())
    #define HAS_CLUSTER_ID()                     (chaos_get_cluster_id() != 0)

    // During cluster service rounds, use no offset
    #define CLUSTER_HOP_CHANNEL_OFFSET() (IS_CLUSTER_JOIN() || IS_CLUSTER_HEAD_ROUND() ? 0 : chaos_get_cluster_index())

    extern node_id_t cluster_id;
    extern uint8_t cluster_index;

    extern uint8_t is_cluster_join_round;
    extern uint8_t cluster_head_round_initiated;

#endif /* CHAOS_CLUSTER */

ALWAYS_INLINE node_id_t chaos_get_cluster_id(void);
ALWAYS_INLINE uint8_t chaos_get_cluster_index(void);
ALWAYS_INLINE void chaos_cluster_round_end(void);

#endif /* _CHAOS_CLUSTER_H_ */

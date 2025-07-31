from enum import StrEnum


class CacheRedisMode(StrEnum):
    CLUSTER = "cluster"
    SINGLE_NODE = "single_node"

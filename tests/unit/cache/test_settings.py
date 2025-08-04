from unittest.mock import patch
import os

import pytest
from pydantic import ValidationError

from solkit.cache.constants import CacheRedisMode
from solkit.cache.settings import (
    CacheRedisModeSettings,
    CacheRedisSettings,
    CacheRedisClusterSettings,
    CacheRedisSingleNodeSettings,
)


@pytest.mark.parametrize(
    "deployment_mode",
    [
        pytest.param(CacheRedisMode.CLUSTER, id="cluster"),
        pytest.param(CacheRedisMode.SINGLE_NODE, id="single-node"),
    ],
)
def test_valid_deployment_mode(deployment_mode):
    """Test that valid deployment modes are accepted."""
    # arrange
    with patch.dict(os.environ, {"CACHE_DEPLOYMENT_MODE": deployment_mode.value}):
        # act
        settings = CacheRedisModeSettings()
    # assert
    assert settings.deployment_mode == deployment_mode


def test_invalid_deployment_mode():
    """Test that invalid deployment mode raises ValidationError."""
    # arrange
    with pytest.raises(ValidationError) as exc_info:
        # act
        CacheRedisModeSettings(CACHE_DEPLOYMENT_MODE="invalid_mode")
    # assert
    assert "deployment_mode" in str(exc_info.value)


def test_valid_settings_with_defaults():
    """Test that valid settings with defaults work correctly."""
    # arrange
    with patch.dict(os.environ, {
        "CACHE_DEPLOYMENT_MODE": CacheRedisMode.CLUSTER.value,
        "CACHE_HOST": "localhost"
    }):
        # act
        settings = CacheRedisSettings()
    # assert
    assert settings.deployment_mode == CacheRedisMode.CLUSTER
    assert settings.host == "localhost"
    assert settings.port == 6379
    assert settings.db == 0
    assert settings.max_connections == 10
    assert settings.socket_timeout == 5
    assert settings.socket_connect_timeout == 5
    assert settings.socket_keepalive is True
    assert settings.health_check_interval == 10
    assert settings.retry_max_attempts == 3


def test_build_uri_property():
    """Test the build_uri property returns correct URI format."""
    settings = CacheRedisSettings(
        CACHE_DEPLOYMENT_MODE=CacheRedisMode.CLUSTER,
        CACHE_HOST="redis.example.com",
        CACHE_PORT=6380,
        CACHE_DB=5
    )
    
    expected_uri = "redis://redis.example.com:6380/5"
    assert settings.build_uri == expected_uri


def test_valid_cluster_settings_with_defaults():
    """Test that valid cluster settings with defaults work correctly."""
    settings = CacheRedisClusterSettings(
        CACHE_DEPLOYMENT_MODE=CacheRedisMode.CLUSTER,
        CACHE_HOST="localhost"
    )
    
    # Inherited fields
    assert settings.deployment_mode == CacheRedisMode.CLUSTER
    assert settings.host == "localhost"
    assert settings.port == 6379
    
    # Cluster-specific fields
    assert settings.read_from_replicas is True
    assert settings.require_full_coverage is False


def test_valid_single_node_settings_with_defaults():
    """Test that valid single node settings with defaults work correctly."""
    settings = CacheRedisSingleNodeSettings(
        CACHE_DEPLOYMENT_MODE=CacheRedisMode.SINGLE_NODE,
        CACHE_HOST="localhost"
    )
    
    # Inherited fields
    assert settings.deployment_mode == CacheRedisMode.SINGLE_NODE
    assert settings.host == "localhost"
    assert settings.port == 6379
    
    # Single node-specific fields
    assert settings.retry_on_timeout is True

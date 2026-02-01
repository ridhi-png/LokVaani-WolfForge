"""Serialization utilities for Redis storage."""

import json
import pickle
from typing import Any, Optional, Dict, Union
from datetime import datetime, date
from decimal import Decimal

from .exceptions import ProcessingError


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        elif isinstance(obj, date):
            return {"__date__": obj.isoformat()}
        elif isinstance(obj, Decimal):
            return {"__decimal__": str(obj)}
        return super().default(obj)


def datetime_decoder(dct: Dict[str, Any]) -> Dict[str, Any]:
    """JSON decoder that handles datetime objects."""
    if "__datetime__" in dct:
        return datetime.fromisoformat(dct["__datetime__"])
    elif "__date__" in dct:
        return date.fromisoformat(dct["__date__"])
    elif "__decimal__" in dct:
        return Decimal(dct["__decimal__"])
    return dct


def serialize_to_redis(data: Any, use_pickle: bool = False) -> Union[str, bytes]:
    """
    Serialize data for Redis storage.
    
    Args:
        data: The data to serialize
        use_pickle: Whether to use pickle instead of JSON
        
    Returns:
        Serialized data as string or bytes
        
    Raises:
        ProcessingError: If serialization fails
    """
    try:
        if use_pickle:
            return pickle.dumps(data)
        else:
            return json.dumps(data, cls=DateTimeEncoder, ensure_ascii=False)
    except Exception as e:
        raise ProcessingError(f"Failed to serialize data: {e}")


def deserialize_from_redis(data: Union[str, bytes], use_pickle: bool = False) -> Any:
    """
    Deserialize data from Redis storage.
    
    Args:
        data: The serialized data
        use_pickle: Whether the data was pickled
        
    Returns:
        Deserialized data
        
    Raises:
        ProcessingError: If deserialization fails
    """
    try:
        if use_pickle:
            return pickle.loads(data)
        else:
            return json.loads(data, object_hook=datetime_decoder)
    except Exception as e:
        raise ProcessingError(f"Failed to deserialize data: {e}")


def serialize_pydantic_model(model: Any) -> str:
    """
    Serialize a Pydantic model to JSON string.
    
    Args:
        model: The Pydantic model instance
        
    Returns:
        JSON string representation
        
    Raises:
        ProcessingError: If serialization fails
    """
    try:
        return model.model_dump_json()
    except Exception as e:
        raise ProcessingError(f"Failed to serialize Pydantic model: {e}")


def deserialize_pydantic_model(model_class: type, data: str) -> Any:
    """
    Deserialize JSON string to Pydantic model.
    
    Args:
        model_class: The Pydantic model class
        data: JSON string data
        
    Returns:
        Pydantic model instance
        
    Raises:
        ProcessingError: If deserialization fails
    """
    try:
        return model_class.model_validate_json(data)
    except Exception as e:
        raise ProcessingError(f"Failed to deserialize Pydantic model: {e}")


def safe_serialize(data: Any, fallback_to_pickle: bool = True) -> Union[str, bytes]:
    """
    Safely serialize data, falling back to pickle if JSON fails.
    
    Args:
        data: The data to serialize
        fallback_to_pickle: Whether to fallback to pickle if JSON fails
        
    Returns:
        Serialized data
        
    Raises:
        ProcessingError: If all serialization methods fail
    """
    try:
        # Try JSON first
        return serialize_to_redis(data, use_pickle=False)
    except ProcessingError:
        if fallback_to_pickle:
            try:
                # Fallback to pickle
                return serialize_to_redis(data, use_pickle=True)
            except ProcessingError as e:
                raise ProcessingError(f"Failed to serialize with both JSON and pickle: {e}")
        else:
            raise


def safe_deserialize(data: Union[str, bytes], expected_type: Optional[type] = None) -> Any:
    """
    Safely deserialize data, trying both JSON and pickle.
    
    Args:
        data: The serialized data
        expected_type: Expected type for validation
        
    Returns:
        Deserialized data
        
    Raises:
        ProcessingError: If deserialization fails
    """
    # Try to determine if data is pickled (bytes) or JSON (string)
    if isinstance(data, bytes):
        try:
            result = deserialize_from_redis(data, use_pickle=True)
        except ProcessingError:
            # Maybe it's JSON encoded as bytes
            try:
                result = deserialize_from_redis(data.decode('utf-8'), use_pickle=False)
            except ProcessingError as e:
                raise ProcessingError(f"Failed to deserialize bytes data: {e}")
    else:
        try:
            result = deserialize_from_redis(data, use_pickle=False)
        except ProcessingError as e:
            raise ProcessingError(f"Failed to deserialize string data: {e}")
    
    # Validate type if expected
    if expected_type and not isinstance(result, expected_type):
        raise ProcessingError(f"Deserialized data is not of expected type {expected_type}")
    
    return result
import uuid

def validate_thread_id(thread_id: str) -> bool:
    """
    校验 thread_id 是否合法。

    Args:
        thread_id (str): 需要校验的 thread_id。

    Returns:
        bool: 是否合法。
    """
    try:
        # 对 thread_id 进行 uuid4 校验
        uuid.UUID(thread_id, version=4)
        return True
    except ValueError:
        return False
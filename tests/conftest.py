import time
from functools import wraps
import pytest

import esankhyiki

@pytest.fixture(autouse=True, scope="session")
def rate_limit_mospi_api():
    """
    Globally throttle all API calls to MoSPI during testing to 4 requests per minute 
    (15 seconds between requests). This helps avoid 500 errors and temporary IP blocks 
    from the target servers when running the full network test suite.
    """
    original_get = esankhyiki._client.session.get
    original_post = esankhyiki._client.session.post
    
    last_request_time = [0.0]
    min_delay = 5.0
    
    def rate_limited(original_method):
        @wraps(original_method)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_request_time[0]
            if elapsed < min_delay:
                time.sleep(min_delay - elapsed)
            
            response = original_method(*args, **kwargs)
            last_request_time[0] = time.time()
            return response
            
        return wrapper

    # Apply the monkeypatch to the global client instance
    esankhyiki._client.session.get = rate_limited(original_get)
    esankhyiki._client.session.post = rate_limited(original_post)
    
    yield
    
    # Clean up and restore original methods when tests conclude
    esankhyiki._client.session.get = original_get
    esankhyiki._client.session.post = original_post

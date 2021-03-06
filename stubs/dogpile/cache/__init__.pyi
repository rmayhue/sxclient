# Stubs for dogpile.cache (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
from typing import Optional, Any, Callable


class CacheRegion:
    def configure(self, backend: str, expiration_time: Optional[Any]) -> CacheRegion: ...
    def cache_on_arguments(self, namespace: Optional[Any]) -> Callable: ...

def make_region(*arg: Any, **kw: Any) -> CacheRegion: ...

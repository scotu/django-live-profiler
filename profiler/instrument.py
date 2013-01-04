from datetime import datetime

from django.db.models.sql.compiler import SQLCompiler
from django.db import connection

from aggregate.client import get_client

from profiler import _get_current_view

def execute_sql(self, *args, **kwargs):
    client = get_client()
    if client is None:
        return self.__execute_sql(*args, **kwargs)
    q, params = self.as_sql()
    start = datetime.now()
    try:
        return self.__execute_sql(*args, **kwargs)
    finally:
        d = (datetime.now() - start)
        client.insert({'query' : q, 'view' : _get_current_view(), 'type' : 'sql'}, 
                      {'time' : 0.0 + d.seconds * 1000 + d.microseconds/1000, 'count' : 1})
        
INSTRUMENTED = False



if not INSTRUMENTED:
    SQLCompiler.__execute_sql = SQLCompiler.execute_sql
    SQLCompiler.execute_sql = execute_sql
    INSTRUMENTED = True


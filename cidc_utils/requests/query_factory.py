#!/usr/bin/env python3
"""
Convenience methods for performing operations on EVE API resources.
"""
import json


def construct_query(
        endpoint: str, projection: dict=None, condition: dict=None, record_id: str=None
) -> str:
    """
    Takes conditions and turns them into an appropriately formatted query.

    Arguments:
        endpoint {str} -- Resource endpoint.

    Keyword Arguments:
        projection {dict} -- Dict specifying projected fields. (default: {None})
        condition {dict} -- Dict of search conditions. (default: {None})
        record_id {str} -- Specific record ID (default: {None})

    Returns:
        str -- Formatted query.
    """
    query = endpoint
    if record_id and condition:
        raise ValueError('Document queries do not support conditions')
    if record_id:
        query += "/" + record_id
    else:
        query += "?"
        if condition:
            query += 'where=%s' % (json.dumps(condition))
        if projection and condition:
            query += "&"
        if projection:
            query += 'projection=%s' % (json.dumps(projection))

    return query

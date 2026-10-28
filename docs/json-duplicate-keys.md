# Duplicate JSON keys

A JSON object containing the same key more than once must be rejected, not silently overwritten. Regression tests should verify duplicates at root and nested levels, and valid distinct keys in nested sibling objects.

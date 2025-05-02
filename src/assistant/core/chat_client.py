"""
Imports openai, sets the key from config.py, chooses model names, handles retries & error mapping.
Count tokens, catch RateLimitError, write to a log file.
只負責「聊」，不直接打 API
"""
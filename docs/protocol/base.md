
# Base protocol

## Header part

## Content part

Contains the actual content of the message. The content part of a message uses [JSON-RPC](http://www.jsonrpc.org/) to describe requests, responses and notifications. The content part is encoded using the charset provided in the Content-Type field. It defaults to utf-8, which is the only encoding supported right now. If a server or client receives a header with a different encoding than utf-8 it should respond with an error.

```json title="Example"
Content-Length: ...\r\n
\r\n
{
    "jsonrpc": "2.0",
    "id": 1,
    "timestamp": 0,
    "method": "Canvas",
    "params": {
        ...
    }
}
```

## Base types
## Request message
## Response message
## Notification message

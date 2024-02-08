# foo.db
A test key-value store.

## Interaction
### Put

```sh
curl -X POST -H 'Content-Type: application/octet-stream' --data-binary "hello world" http://localhost:5000/db/foo
```

### Get

```sh
curl http://127.0.0.1:5000/db/foo
hello world
```

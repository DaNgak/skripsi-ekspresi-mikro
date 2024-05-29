<h1 align="center">Backend API</h1>

## API Base Response

Struktur Response JSON

### Response Success

```bash
{
    code: 200
    message: "Ok"
    data: {
        "sample_key": "value_key",
        ...
    }
}
```

### Response Error

```bash
{
    code: 500
    message: "Error message"
    errors: {
        "sample_key": "value_key",
        ...
    }
}
```

## API Documentation

-   [Postman App](https://github.com/DaNgak)

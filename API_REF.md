
# Notezz API Reference

## Basic Setup

- Follow the setup instructions given in [READ_ME.md](https://github.com/Sanjie25/notezz/blob/main/README.md) and run the app.
- Run the app with `python run.py`

> The example requests in this file, will be made using the [curl](https://curl.se/download.html) command line tool.

## Setting Up Cookies file

### Issue with curl

  `curl` doesn't maintain session state between requests by default, so we'll have to use `curl`  command with a cookies file. We'll have to use both `-c`, save cookies and `-b`, send cookies flags of `curl`

#### Requests example by using a cookies file

```
# Create cookies file
touch my_cookies.txt

# Login and writing into the cookies file
curl -X POST http://127.0.0.1:12345/auth/<login/register> \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "Password123!"}' \
  -c my_cookies.txt \
  -b my_cookies.txt

# Using the cookies file in future queries
curl -X POST http://127.0.0.1:12345/create \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt \
  -d '{
    "title": "First note",
    "body": "Test content",
  }'

```

# Authentication and Administration Requests and Functions

## Registering a User

Input a json-like POST request with three fields, `username`, `password` and `email` To `http://127.0.0.1:12345/auth/login`.

```

  curl -X POST http://127.0.0.1:12345/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "example123", "email": "testuser@example123.com"}' \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Login as a User

Send a POST request with fields, `username` or `email` and `password`. To `http://127.0.0.1:12345/auth/login`

```

  curl -X POST http://127.0.0.1:12345/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "example123"}' \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Logout as a User

Send an empty POST request to `http://127.0.0.1:12345/auth/login`

```

  curl -X POST http://127.0.0.1:12345/auth/logout \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Check if authorised or not

Send an empty GET request to `http://127.0.0.1:12345/auth/check-auth`

```

  curl -X GET http://127.0.0.1:12345/auth/check-auth \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## To get your profile

Send a GET request to `http://127.0.0.1:12345/auth/profile`

```

  curl -X GET http://127.0.0.1:12345/auth/profile \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt

```

# Data Management

## Create data row

Send a POST request to `http://127.0.0.1:12345/data/create` in json format with two fields, `title` and `body`

```

curl -X POST http://127.0.0.1:12345/data/create \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt \
  -d '{
    "title": "First post",
    "body": "Test content"
  }'

```

## Get a Data row

Send a GET request with `data_id` in url `http://127.0.0.1:12345/data/<data_id>`.

```

curl -X DELETE http://127.0.0.1:12345/data/1 \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt \

```

## Get all data

Send a GET request to `http://127.0.0.1:12345/data/all`

```

curl -X GET http://127.0.0.1:12345/data/all \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt

```

## Edit some data

Send a PUT request with `data_id` to `http://127.0.0.1:12345/data/<data_id>/edit` with two fields `title` and `body`.

```

curl -X PUT http://127.0.0.1:12345/data/1/edit \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt \
  -d '{
    "title": "Example text: Oh ho, you're approaching me.",
    "body": "Edited Note: "
  }'

```

## Delete a note

Send a DELETE request with `data_id` to `http://127.0.0.1:12345/data/<data_id>/delete`.

```

curl -X DELETE http://127.0.0.1:12345/data/1/delete \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt \

```

## Delete a note using it's title

Send a DELETE request to `http://127.0.0.1:12345/data/delete_by_title` with the field of `title` only

```

curl -X DELETE http://127.0.0.1:12345/data/delete_by_title \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt \
-d '{"title": "data title"}'

```

# Authorisation Error due to cookies

it might look something like this,

```

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/auth/login?next=%2Fauth%2Fcheck-auth">/auth/login?next=%2Fauth%2Fcheck-auth</a>. If not, click the link.

```

in curl

# Endpoints reference
## Bikes collection endpoints
List all bikes flagged as "robbed" on the platform. Allow creation of new bikes for **authenticated users only**,
[see authentication](#authentication-endpoints)

### List all *robbed* bikes
`GET /`

Query parameters : 

| Parameter | Type | Default | Description |
| ------------ | :------------: | :----------: | ------------ |
| limit | Number | 20 | Maximum number of items |
| offset | Number | 0 | Position of the cursor (use it for pagination purpose) |
| search_type | String | 'all' | Type of your request (`'all'`, `filtered`, `'near'` or `'owned'`) |
| lon | Number | 2.349903 | Longitude of your point (for `search_type='near'` only) |
| lat | Number | 48.852969 | Latitude of your point (for `search_type='near'` only) |
| traits | String | " " | Coma separated list of traits to filter bikes (for `search_type=filtered` only) |

- *search_type = all* : Return all bikes flagged as "robbed" from the service (sorted by date_of_robbery)
- *search_type = filtered* : Return bikes flagged as "robbed" with matching traits (sorted by date_of_robbery)
- *search_type = near* : Return bikes robbed near a point, default point is set in Paris.
- *search_type = owned* : **For authenticated user only** Return bikes declared by the authenticated account

```javascript
// Expected output

{
    "count": 2537,                                        // Number of bike this request can fetch
    "next": "http://127.0.0.1:8000/?limit=20&offset=20", // Link to the next page
    "previous": null,                                   // Link to the previous page
    "results": [                                       // List of fetched bikes
        {
            "picture": "http://127.0.0.1:8000/media/bikes/default.jpg",
            "reference": "FooSerialNumber",
            "traits": [],
            "robbed": true,
            "robbed_location": {
                "latitute": "48.852969",
                "longitude": "2.349903"
            },
            "robbery_city": null,
            "date_of_robbery": "18/06/21 20h",
            "pk": 5058
        },
        // ... x 20
    ]
```

### Register a bike
`POST /`

> **Important** : If you wish to join a picture, Request body should be encoded as `multipart/form-data`.
> For clarity purpose, example is indicated as a JSON
```javascript
// Request body 
{
    "reference": "FooSerialNumber",
    "robbed": "Boolean",
    "date_of_robbery": "2021-06-18T20:27+02:00", // Datetime encoded as ISO 8602
    "robbed_location": {
        "latitude": "48.852969", // Latitude in radians
        "longitude": "2.349903", // Longitude in radians
    },
    "picture": "Should be form-data encoded"
}
```
````javascript
// Expected response
{
    "picture": "http://127.0.0.1:8000/media/bikes/default.jpg", //If no picture is provided, a default one is set
    "reference": "FooSerialNumber",
    "traits": [],
    "robbed": true,
    "robbed_location": {
        "latitute": "48.852969",
        "longitude": "2.349903"
    },
    "robbery_city": null,
    "date_of_robbery": "18/06/21 20h",
    "pk": 5058
}
````

## Bike detail endpoints
> Path parameter `BikeId` must match `pk` attribute of a bike
### Retrieving a bike
Retrieve a single bike instance

`GET bike/<int: BikeId>/`

Expected request : `https://entrypoint/bike/5058/`
````javascript
// Expected response
{
    "picture": "http://127.0.0.1:8000/media/bikes/default.jpg",
    "reference": "FooSerialNumber",
    "traits": [],
    "robbed": true,
    "robbed_location": {
        "latitute": "48.852969",
        "longitude": "2.349903"
    },
    "robbery_city": null,
    "date_of_robbery": "18/06/21 20h",
    "pk": 5058
}
````
### Patching a bike
For **bike owner or moderator users only**.

Allow edition of attributes on a bike instance.

Patching is the only way for adding traits to a bike.

`PATCH bike/<int: BikeId>/`

```javascript
// Expected Body
{
    "traits":["Test","Foo"]  //Can be any valid attribute other than 'traits'
}
```
````javascript
// Expected response
{
    "picture": "http://127.0.0.1:8000/media/bikes/default.jpg",
    "reference": "FooSerialNumber",
    "traits": ["Test", "Foo"], // Traits are now registered
    "robbed": true,
    "robbed_location": {
        "latitute": "48.852969",
        "longitude": "2.349903"
    },
    "robbery_city": null,
    "date_of_robbery": "18/06/21 20h",
    "pk": 5058
}
````

### Deleting a bike
For **moderator users only**. If you wish to remove a bike from the public listing, you have to patch it and set `robbed:False`.
This behavior ensure all relevant data is preserved in database for data analysis purpose. 

`DELETE bike/<int: BikeId>/`

## Traits endpoints
Traits are basically tags describing a bike. There can be as much as you want for a bike.

Traits cannot be set in initial creation of a bike, [you must patch it after creation](#patching-a-bike).
### Search traits
`GET traits/`

| Parameter | Type | Default | Description |
| ------------ | :------------: | :----------: | ------------ |
| qs | String | " " | **Mandatory parameter** : querystring for searching traits |

Example request : `https://entrypoint/traits/?qs=t`
```javascript
// Expected output
{
    "count": 2,
    "next": null, // Pagination
    "previous": null, // Pagination
    "results": [
        {
            "name": "Test"
        },
        {
            "name": "Truc"
        }
    ]
}
```

### Create trait
**For authenticated users only**

`POST traits/`

```javascript
// Request Body
{
    "name":"foo"
}
```

```javascript
// Expected output
{
    "name": "Foo"
}
```
> Note that traits are capitalized server side

## Found Bike Alert endpoint
Allow creation of an alert when a bike is spotted. When an alert is created, en email is sent to the owner with alert details.

`POST bike/<int: BikeId>/found/` where `BikeId` matches `bike.pk`

```javascript
// Expected Body
{
    "message": "I've seen your bike !", // Message to the owner of the bike
    "coords": {         // Longitude and Latitude where the bike have been spotted
        "lat": "48.852969",
        "lon": "2.349903"
    }
}
```

```javascript
// Expected response
{
    "message": "I've seen your bike !",
    "coords": {
        "lat": "48.852969",
        "lon": "2.349903"
    },
    "date": "09/06/21 à 14h11" // Date is generated server side
}
```

## Authentication endpoints
Authentication is based on 6-digits token sent via mail.
Account creation is automatic on first login.
### Email
Start sending your email

`POST /pwl/auth/email/`
```javascript
// Request body
{
    "email": "youremail@here.com"
}
```
```javascript
// Expected response body
{
    "detail": "A login has been sent to your email."
}
```
### Token
Then fetch the 6 digits login token from your inbox and send it along your email

`POST /pwl/auth/token/`
```javascript
// Request body
{
    "email": "youremail@here.com",
    "token": "123456"
}
```
```javascript
// Expected response body is a long authentication token
{
    "token": "averylongauthtoken8c42f399e4c46208007b"
}
```
#### Setting the Authorization header
Once you have this token, be sure to send it as Authorization headers along any request needing authentication.
Authorization header must be set as in example below.

`Authorization: Token averylongauthtoken8c42f399e4c46208007b`

### Verify
Another endpoint is provided to ensure authentication is well done and token is valid.

`GET /pwl/verify/`

**Expected responses :** 

- Empty response with status code `200` if correctly logged
- Empty response with status code `401` if not correctly logged

## Statistics endpoint (WIP)
**For authenticated & [institutional users](users.md#institutional-users) only !**

`GET /stats/`

| `Accept` header | Expected output |
|-|-|
|`*/*`| XLSX file with **all** bikes bound to user's geographic zones|
|`application/json`| JSON with **all** bikes bound to user's geographic zones|
# Users and permission reference
All [authenticated users](endpoints.md#authentication-endpoints) are referenced as `Owner`
## Anonymous User
Non authenticated user. Have read-only access to every bike flagged as `robbed` and can create an `alert` when spotting a bike.

|**Read only**| **Read/Write** | **Write only** |
|-|-|-|
|[List of robbed bikes](endpoints.md#list-all-robbed-bikes)|[Authentications endpoints](endpoints.md#authentication-endpoints)|[Found bike alert](endpoints.md#found-bike-alert-endpoint)|
|[Details of bike](endpoints.md#retrieving-a-bike)|||
|[Search for traits](endpoints.md#search-traits)|||

## Basic User
Basic authenticated user.

|**Read only**| **Read/Write** | **Write only** |
|-|-|-|
|[Details of bike](endpoints.md#retrieving-a-bike)|[Bikes collection](endpoints.md#bikes-collection-endpoints)|[Edition of bike](endpoints.md#patching-a-bike)|
||[All traits endpoints](endpoints.md#traits-endpoints)|[Found bike alert](endpoints.md#found-bike-alert-endpoint)|

## Institutional users
Institutional users are registered by administrator of the service. If you are an institution (city administration, association, etc.) [contact me for an accreditation](mailto:riandeypierre@gmail.com).
Institutional users have one or several dedicated geographic zones for which they can access all the relevant data (ex: all bikes theft and found, all alerts, etc.)

They inherit from all authorization of Basic users, but have access to a dedicated endpoint :
[Statistics](endpoints.md#statistics-endpoint)

## Moderation users
Moderation users are registered by administrator of the service. They have read-write-delete access to all the endpoints of the API.


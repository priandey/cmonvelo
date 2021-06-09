# Resources reference
## Bike
### Public Bike resource
|**Attribute**|**Type**|**Optional**|**Description**|
|-|-|-|-|
|`reference`|String|No|Unique identifier for a bike (ex: bicycode)|
|`picture`|String|Yes|Path to the picture of the bike|
|`traits`|List|Yes|List of all traits registered for the bike|
|`robbed`|Boolean|No|Status of the bike (if `True`, the bike is in public access)|
|`robbed_location`|JSON|If `robbed=false`|Coordinates of where bike was robbed. Format : {latitude:2.343, longitude:43.435}|
|`date_of_robbery`|String|If `robbed=false`|Date of the theft in ISO 8602 format|
|`pk`|Number|**Read-only**| primary key (ID) of the bike|
|`robbery_city`|String|**Read-only**|city matching `robbed_location`|

### Owned Bike Resource
This resource contains all Public bike resource attributes, in addition to : 

|**Attribute**|**Type**|**Optional**|**Description**|
|-|-|-|-|
|`owner`|String|**Read-only**|Email of the owner|
|`alerts`|JSON|**Read-Only**|All found alerts registered for this bike|

## Traits

|**Attribute**|**Type**|**Optional**|**Description**|
|-|-|-|-|
|`name`|String|No|Name of the trait (serve as primary key)|

## Alerts

|**Attribute**|**Type**|**Optional**|**Description**|
|-|-|-|-|
|`message`|String|No|Message to send to the owner of the spotted bike|
|`coords`|JSON|No|Coordinates of where bike was spotted. Format : {latitude:2.343, longitude:43.435}|
|`bike`|Integer|No|Primary Key of the spotted bike|
|`date`|String|**Read-only**|Date in ISO 8602 format|

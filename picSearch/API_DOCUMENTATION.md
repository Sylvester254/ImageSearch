## Missing Children API Documentation
### Overview

> The Missing Children API allows you to search for missing children based on the images submitted. You can use this API to integrate the search functionality with other websites or applications.

### Base URL
The base URL for the API will depend on where you have deployed your Django application. For example, if you have deployed it on https://your-domain.com, then the base URL would be:

`https://your-domain.com`

### Endpoints
#### Search for missing children

**Request**
- Method: POST
- Endpoint: /api/search/
- Content-Type: multipart/form-data
- Parameters:
    image (required): An image file of the missing child.

**Response**
- Status Code: 200 OK

- Content-Type: application/json

- Body: An array of objects, each representing a missing child that has a similar image to the one provided in the request. Each object contains the following fields:

    id: The unique identifier of the missing child.
    name: The name of the missing child.
    age: The age of the missing child.
    image_url: The URL of the missing child's image.
    date_missing: The date when the child went missing (format: YYYY-MM-DD).
    place_of_birth: The place of birth of the missing child.
    last_seen: The location where the child was last seen.
    guardian_name: The name of the child's guardian.
    guardian_contact: The contact information of the child's guardian.
    
*Example*

**Request:**

```
POST https://your-domain.com/api/search/
Content-Type: multipart/form-data

image=@example_image.jpg
```

**Response:**

```
[
    {
        "id": 8,
        "name": "mike",
        "age": 15,
        "image_url": "/picSearch/media/missing_children/1409862543_0.png",
        "date_missing": "2020-02-02",
        "place_of_birth": "kenya",
        "last_seen": "Roysambu",
        "guardian_name": "Hellen",
        "guardian_contact": "07919298339"
    }
]
```

That's it! This documentation should provide enough information for other developers to integrate your Missing Children API with their websites or applications. Remember to replace https://your-domain.com with the actual domain or IP address where your Django application is hosted.
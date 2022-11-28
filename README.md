# Project's Title

NYPLProject - readingpal is a simple web application for user to search a reading from NYPL test APIs and return max 10 similar readings from the same collection from NYPL dataset.

## Installation

1. To run by local virtual environment by django
   1. (locate into the NYPLProject folder) activate virtual environment
        ```
          source py310_nypl/bin/activate
        ```
   2. Add NYPL APIs token into NYPLProject/readingpal/nyplapi/configs.py
        ```
          NYPL_API_TOKEN = "" # keep it private
        ```

   3. (locate into the readingpal folder) run django command to start server
        ```
          python manage runserver
        ```


## Usage
1. Test web ui: 
    1. open browser with link: http://127.0.0.1:8000
    2. input a title, then click submit to review the result
2. Test API call: 
    1. call http://127.0.0.1:8000/nyplapi/[str:title]/search to check json format return data


## API Structure

   ### GET: nyplapi/[str:title]/search
Request URL: 

http://127.0.0.1:8000/nyplapi/[str:title]/search

PARAMS:

title: string, required, a target reading item title that the user want to search

Description: 

Returns the FIRST target reading item title, type, with NYPL web link, together with max 10 readings from the same collection from NYPL datasource as similar readings.

Examples:

1. Description: search a title "tttttttttttt" from NYPL datasource, but not found anything.

    API call: 

        http://127.0.0.1:8000/nyplapi/tttttttttttt/search

    return value:
    
    ```
    {
        "status": "success",
        "data": {}
    }
    ```

2. Description: search a title "Winter" from NYPL datasource, return first found readings. However, it does not have any other similar readings from the same collection.

    API call: 

        http://127.0.0.1:8000/nyplapi/Winter/search

    return value:

    ```
    {
        "status": "success",
        "data": {
            "reading_title": "Winter",
            "reading_type": "still image",
            "reading_weblink": "http://digitalcollections.nypl.org/items/80d47102-a77f-5fc6-e040-e00a18065e1d",
            "collection_similar_captures": []
        }
    }
    ```
3. Description: search a title "Summer" from NYPL datasource, return first found readings and also returned other similar readings from the same collection.

    API call: 

        http://127.0.0.1:8000/nyplapi/Summer/search

    return value:

    
    ```
    {
        "status": "success",
        "data": {
            "reading_title": "Summer excursion routes",
            "reading_type": "text",
            "reading_weblink": "http://digitalcollections.nypl.org/items/8afc6586-988d-a28e-e040-e00a18067b76",
            "collection_similar_captures": [
                {
                    "title": "Logan House, Altoona.",
                    "type": "still image",
                    "weblink": "http://digitalcollections.nypl.org/items/8afc6586-9892-a28e-e040-e00a18067b76"
                },
                {
                    "title": "New Brunswick, N.J.",
                    "type": "still image",
                    "weblink": "http://digitalcollections.nypl.org/items/8afc6586-9891-a28e-e040-e00a18067b76"
                },
                {
                    "title": "York Springs",
                    "type": "still image",
                    "weblink": "http://digitalcollections.nypl.org/items/8afc6586-9890-a28e-e040-e00a18067b76"
                },
                {
                    "title": "Coatsville Bridge",
                    "type": "still image",
                    "weblink": "http://digitalcollections.nypl.org/items/8afc68fe-a0a2-af73-e040-e00a18067b5e"
                }
            ]
        }
   }
   ```
## Test Case

1. Test Web View functions:
    
    under NYPLProject/readingpal/bookpick/tests.py

2. Test API View function:

    under NYPLProject/readingpal/nyplapi/tests.py

## Tech stack

   Python, DJango, Rest API

## Contributing

1. NYPL APIs collections
2. Danfeng Wang

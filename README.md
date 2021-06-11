# wiki-scraper

In this web application you can paste in any Wikipedia link or type in a phrase and you will see the main title, subtitles, most frequent words for each sub section, and the hyperlinks for each sub section. The most frequent words excludes "stop words".

You can also access the api to integrate for your own use case. Follow the documentation below:

Documentation work in progress...

**Get Wiki Info**
----
  Returns json data about a specific wikipedia link.

* **URL**

  /api/v1/wiki?phrase=(phrase)

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `phrase=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ title : "Dog", subtitles : [ "Taxonomy", "Evolution", "Domestication", ... ], freq_words : { "Anatomy" : [ "dogs", "type", "types", ... ], ... }, hyperlinks : { "Anatomy" : [ "/wiki/Dog_anatomy", "/wiki/File:Dog_anatomy_lateral_skeleton_view.jpg", "/wiki/File:Dog_anatomy_lateral_skeleton_view.jpg", ... ], ... } }`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Wikipedia phrase not found" }`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  JavaScript:
  ```javascript
    $.ajax({
      url: "/api/v1/wiki?phrase=Dog",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```
  
  Python:
  ```python
    import requests
    r = requests.get("https://wiki-scraper-vsfs.herokuapp.com/api/v1/wiki?phrase=Dog")
    r.json()
  ```


To create this, I am using a free background wallpaper that you can view [here](https://wallpaperaccess.com/uhd-abstract).

Created for US Embassy London - The AI Innovation Revolution! a Virtual Student Federal Service Project

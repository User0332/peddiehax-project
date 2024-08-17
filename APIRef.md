# API Reference for Frontend Team

- POST /api/addentry
	- Add Journal Entry

	- CLIENT POSTs form data containing
		- `loc`, `string` - Geographical Location expressed as `lat,long` coordinates
		- `name`, `string` - Geographical Location expressed as a human-friendly name
		- `people`, `string` - Comma-separated list of people who were there EXCLUDING the author/poster
		- `description`, `string` - User-added description
		- `rating`, `stringified integer, 1-5`, - Rating
		- `journey`, `string` - Journey ID of the journey to add this entry to

		- File data - photos (png, jpg, or jpeg), **maximum 3 files**

	- SERVER responds 200 OK (no data)

- GET /api/nearby
	- Get Nearby Attractions
	

	- CLIENT sends: URL arg `loc=<lat>,<long>`
		- Where `lat` and `long` are the latitude and longitude of the client's location, respectively
	- SERVER returns: JSON object mapping strings of nearby attractions to GPS coordinates
	
	
	- Example
		- CLIENT sends request `GET /api/nearby?loc=1.2,5.37`
		- SERVER returns `{ "Carl's Cafe": "1.222,5.403" }`
	
- GET /api/listjourneys
	- Get a list of journey IDs, ordered from newest to oldest

	- CLIENT sends no data
	- SERVER returns JSON list of string IDs, ordered from oldest to newest


	- Example
		- CLIENT sends request `GET /api/listjourneys/`
		- SERVER returns `["g9f-9UQ3TBW5ZEstmDCpsg", "Z273AjgFJIIkWx1NiMZA1g"]`

- GET /api/getjourney
	- Get Journey Data for specified journey ID

	- CLIENT sends URL arg `id` containing journey ID
	- SERVER responds with JSON object containing
		- `id` -> `string`, the journey ID
		- `name` -> `string`, the journey name
		- `entries` -> `array<string>`, the entry IDs associated with the journey

- POST /api/createjourney
	- Create a journey under the current user
	
	- CLIENT sends form data containing the following
		- `name`, `string` - Name of journey
	
	- SERVER responds with JSON string of new journey ID or null on failure

- GET /api/getphoto
	- Get photo by photo ID

	- CLIENT sends: URL arg `id=<id>`
		- Where `id` is the photo id
	- SERVER returns: JSON string of base64 representing the requested photo
		- SERVER returns `null` on failure
	

	- Example
		- CLIENT sends request `GET /api/getphoto?id=9cukjW8ZiXK4XOfiRHdBAA`
		- SERVER returns `"some long base64 string of photo data"`

- GET /api/getentry
	- Get Entry Data for specified entry ID

	- CLIENT sends URL arg `id` containing entry ID
	- SERVER responds with JSON object containing
		- `id` -> `string`, the entry ID
		- `name` -> `string`, the entry location name
		- `location` -> `string`, the `lat,lng` location of the entry
		- `description` -> `string`, the entry description
		- `rating` -> `integer`, the 1-5 rating of the entry
		- `images` -> `array<string>`, the list of image IDs associated with the entry
		- `people` -> `array<string>`, the list of people associated with the entry
		- `timestamp` -> `Date`, the time when the entry was created
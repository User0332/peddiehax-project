# API Reference for Frontend Team

- POST /api/addentry
	- Add Journal Entry

	- CLIENT POSTs form data containing
		- `loc`, `string` - Geographical Location expressed as `lat,long` coordinates
		- `name`, `string` - Geographical Location expressed as a human-friendly name
		- `people`, `string` - Comma-separated list of people who were there EXCLUDING the author/poster
		- `description`, `string` - User-added description
		- `rating`, `stringified integer, 1-5`, - Rating

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
	- SERVER returns JSON list of string IDs, ordered from newest to oldest


	- Example
		- CLIENT sends request `GET /api/listjourneys/`
		- SERVER returns `["g9f-9UQ3TBW5ZEstmDCpsg", "Z273AjgFJIIkWx1NiMZA1g"]`

- GET /api/getjourney
	- Get Journey Data for specified journey ID

- GET /api/getphoto
	- Get photo by photo ID

	- CLIENT sends: URL arg `id=<id>`
		- Where `id` is the photo id
	- SERVER returns: JSON string of base64 representing the requested photo
	

	- Example
		- CLIENT sends request `GET /api/getphoto?id=9cukjW8ZiXK4XOfiRHdBAA`
		- SERVER returns `"some long base64 string of photo data"`
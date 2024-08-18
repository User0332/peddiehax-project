// TODO: make helper functions for all API calls

function makeAPICall(endpoint, authInfo, body) {
	return fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${authInfo.accessToken}`
		},
		body
	})
}

async function getPlotInfo(journeyID, authInfo) {
	return await (await makeAPICall(`/api/getplotdata?id=${journeyID}`, authInfo)).json()
}

async function getEntryInfo(entryID, authInfo) {
	return await (await makeAPICall(`/api/getentry?id=${entryID}`, authInfo)).json()
}

async function getJourneyInfo(journeyID, authInfo) {
	return await (await makeAPICall(`/api/getjourney?id=${journeyID}`, authInfo)).json()
}

async function getBase64ImageData(imageID, authInfo) {
	return await (await makeAPICall(`/api/getphoto?id=${imageID}`, authInfo)).json()
}

async function listJourneys(authInfo) {
	return await (await makeAPICall("/api/listjourneys", authInfo)).json()
}

async function getFeed(authInfo) {
	return await (await makeAPICall("/api/getfeed", authInfo)).json()
}

async function createAccount(userName, authInfo) {
	return await makeAPICall(`/api/createaccount?username=${userName}`, authInfo)
}

async function createJourney(journeyName, isPublic, authInfo) {
	return await (await makeAPICall(`/api/createjourney?name=${journeyName}?public=${isPublic}`, authInfo)).json()
}

async function getNearbyLocations(loc, authInfo) {
	return await (await makeAPICall(`/api/nearby?loc=${loc}`, authInfo)).json()
}
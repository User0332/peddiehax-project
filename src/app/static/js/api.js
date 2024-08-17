// TODO: make helper functions for all API calls

function makeAPICall(endpoint, authInfo, body) {
	return fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${authInfo.accessToken}`
		},
		body
	})
}

async function getEntryInfo(entryID, authInfo) {
	return await (await makeAPICall(`/api/getentry?id=${entryID}`, authInfo)).json()
}

async function getJourneyInfo(journeyID, authInfo) {
	return await (await makeAPICall(`/api/getjourney?id=${journeyID}`, authInfo)).json()
}

async function listJourneys(authInfo) {
	return await (await makeAPICall("/api/listjourneys", authInfo)).json()
}

async function createAccount(userName, authInfo) {
	return await makeAPICall(`/api/createaccount?username=${userName}`, authInfo)
}

async function createJourney(journeyName, authInfo) {
	return await (await makeAPICall(`/api/createjourney?name=${journeyName}`, authInfo)).json()
}
const authUrl = "https://2950078068.propelauthtest.com";

async function getAuthInfo() {
	const authClient = PropelAuth.createClient({
		authUrl
	});

	return await authClient.getAuthenticationInfoOrNull();
}

(async () => { // onload
	if (!await getAuthInfo()) location.href = authUrl;
})()

function execWithUserData(func) {
	let authSaved;

	getAuthInfo().then(
		authInfo => {
			authSaved = authInfo
			
			return fetch(
				"/api/getself", {
					"headers": {
						Authorization: `Bearer ${authInfo.accessToken}`
					}
				}
			)
		}
	).then(
		res => res.json()
	).then(
		userData => { // main function for page
			if (!userData) location.href = "/finalize-account"

			func(userData, authSaved)
		}
	)
}
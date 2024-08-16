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
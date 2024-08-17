// TODO: add elements for navigation bar

function loadNavbar() {
	const navbar = document.createElement("div");
	navbar.id = "navbar";
	const header = document.createElement("div");
	header.classList.add("")
	navbar.appendChild() // for spacing

	const pages = {
		"Dashboard": "/dashboard",
		"My Journeys": "/my-journeys",
		"Profile": "/profile",
	}

	for (const [page, href] of Object.entries(pages)) {
		const anchor = document.createElement('a');
		anchor.href = href;
		anchor.textContent = page;
		anchor.className = "anchor-btn navbar-btn";

		navbar.appendChild(anchor);
	}

	const logout = document.createElement('a');
	logout.href = "";
	logout.className = "anchor-btn navbar-btn";
	logout.textContent = "Logout";

	logout.onclick = () => {
		authClient.logout().then(
			() => location.href = '/'
		);

		return false;
	}

	navbar.appendChild(logout);

	navbar.appendChild(document.createElement("div")) // for spacing

	document.body.appendChild(navbar);
}

loadNavbar()
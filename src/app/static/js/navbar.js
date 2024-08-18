// TODO: add elements for navigation bar

function loadNavbar() {
	const navbar = document.createElement("div");
	navbar.classList.add("mobile-nav");
	const header = document.createElement("div");
	header.classList.add("header")
	navbar.appendChild(header) // for spacing

	const pages = {
		"Dashboard": "/dashboard",
		"My Journeys": "/my-journeys",
		"Profile": "/profile",
	}

	for (const [page, href] of Object.entries(pages)) {
		const anchor = document.createElement('a');
		anchor.href = href;
		anchor.textContent = page;
		// anchor.className = "anchor-btn navbar-btn";
		anchor.className = "bloc-icon";

		const img = document.createElement('img');
		img.src = `/static/images/${page}.svg`;
		anchor.appendChild(img);

		navbar.appendChild(anchor);
	}

	const logout = document.createElement('a');
	logout.href = "";
	logout.className = "anchor-btn navbar-btn";
	logout.textContent = "Logout";

	const img = document.createElement('img');
	img.src = `/static/images/logout.svg`;
	logout.appendChild(img);

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
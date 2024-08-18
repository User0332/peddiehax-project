// TODO: add elements for navigation bar

function loadNavbar() {
	const navbar = document.createElement("div");
	navbar.classList.add("mobile-nav");
	const header = document.createElement("div");

	const pages = {
		"Dashboard": "/dashboard",
		"My Journeys": "/my-journeys",
		"Profile": "/profile",
	}

	for (const [page, href] of Object.entries(pages)) {
		const anchor = document.createElement('a');
		anchor.href = href;
		// anchor.textContent = page;
		anchor.className = "bloc-icon";
		const img = document.createElement('img');
		img.src = `/static/images/${page}.svg`;
		anchor.appendChild(img);
		navbar.appendChild(anchor);
	}

	// Action Button in the center


	const logout = document.createElement('a');
	logout.href = "";
	logout.className = "bloc-icon";
	// logout.textContent = "Logout";

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

	const actionButton = document.createElement("div");
	

	document.body.appendChild(navbar);
}


function tabBar() {
	const navbar = document.createElement("div");
	navbar.className = "tab";

	const toggle = document.createElement("div");
	toggle.className = "toggle"
	toggle.textContent = "+";

	const menu = document.createElement("ul");
	menu.className = "menu";

	// Dashboard
	const item1 = document.createElement('li');
	const dashboard = document.createElement('a');
	dashboard.href = "/dashboard";
	const icon1 = document.createElement('img');
	icon1.src = `/static/images/dashboard.svg`;

	dashboard.appendChild(icon1);
	item1.appendChild(dashboard);
	menu.appendChild(item1);

	// MyJourneys
	const item2 = document.createElement('li');
	const journey = document.createElement('a');
	journey.href = "/my-journeys";
	const icon2 = document.createElement('img');
	icon2.src = `/static/images/My Journeys.svg`;
	
	journey.appendChild(icon2);
	item2.appendChild(journey);
	menu.appendChild(item2);

	// Action Button (Leave Blank)
	const item3 = document.createElement('li');
	menu.appendChild(item3);

	// Profile
	const item4 = document.createElement('li');
	const profile = document.createElement('a');
	profile.href = "/profile";
	const icon4 = document.createElement('img');
	icon4.src = `/static/images/Profile.svg`;

	profile.appendChild(icon4);
	item4.appendChild(profile);
	menu.appendChild(item4);

	// Log Out (feed tbd)
	const item5 = document.createElement('li');
	const logout = document.createElement('a');
	logout.onclick = () => {
		authClient.logout().then(
			() => location.href = '/'
		);

		return false;
	}
	logout.href = "";
	const icon5 = document.createElement('img');
	icon5.src = `/static/images/logout.svg`;

	logout.appendChild(icon5);
	item5.appendChild(logout);
	menu.appendChild(item5);



	// Add all children to navbar
	navbar.appendChild(toggle);
	navbar.appendChild(menu);

	document.body.appendChild(navbar);
}

// loadNavbar()
tabBar();
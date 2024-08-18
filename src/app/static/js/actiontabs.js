let menuToggle = document.querySelector('.toggle');
let tab = document.querySelector('.tab');
menuToggle.onclick = function(){
    tab.classList.toggle('active');
}

const circularBG1 = document.createElement('div');
circularBG1.className = "actions";

const actionRing = document.createElement('ul');
actionRing.className = "action-ring";

// Add action options -- TODO ADD CLICK ACTIONS

// Example Actions -- NEEDS FUNCTIONALITY -- JUST LOOKS PRETTY RN

const journeyID_Fallback = new URLSearchParams(location.search).get("id");

const icons = {
   "add-person": "/profile",
    "add-text": `/new-entry?journeyID=${journeyID_Fallback}`,
    "add-location": "/new-journey"
}

for (const [imgfile, href] of Object.entries(icons)) {
	if ((imgfile == "add-text") && location.pathname != "/view-journey/") continue;

    const action = document.createElement('li');
    const anchor = document.createElement('a');
    anchor.href = href;
    const img = document.createElement('img');
    img.src = `/static/images/${imgfile}.svg`;
    anchor.appendChild(img);
    action.append(anchor);

	action.onclick = () => anchor.click();
	img.onclick = () => anchor.click();

    actionRing.appendChild(action);
}

circularBG1.appendChild(actionRing);

const circularBG2 = document.createElement('div');
circularBG2.className = "actions-bg-1";

const circularBG3 = document.createElement('div');
circularBG3.className = "actions-bg-2";

tab.appendChild(circularBG1);
tab.appendChild(circularBG2);
tab.appendChild(circularBG3);
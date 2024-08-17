function textElement(tag, text) {
	const elem = document.createElement(tag);

	elem.textContent = text;

	return elem;
}
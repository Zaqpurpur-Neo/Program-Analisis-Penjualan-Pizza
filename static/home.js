const fileDropper = document.querySelector("#file-dropper")
const fileDropperLabel = document.querySelector(".file-dropper-label")
const csvFile = document.querySelector('input[name="csv-file"]')

fileDropperLabel.addEventListener('dragover', ev => {
	ev.preventDefault()
	ev.target.classList.add("drag")
})

fileDropperLabel.addEventListener('dragleave', ev => {
	ev.preventDefault()
	ev.target.classList.remove("drag")
})

fileDropperLabel.addEventListener('drop', ev => {
	ev.preventDefault()
	ev.target.classList.remove("drag")
	Array.from(ev.dataTransfer.items).forEach((item, i) => {
		const file = item.getAsFile()
		ev.target.querySelector('p').textContent = file.name.toString()
	})
	csvFile.files = ev.dataTransfer.files;
})

const submit = document.querySelector(".btn-upload")
const textUpload = submit.querySelector(".text-upload")

submit.addEventListener('click', () => {
	textUpload.style.display = 'none';
	document.querySelector(".loader").classList.toggle("hidden");

	const formData = new FormData()
	formData.append('csv-file', csvFile.files[0])

	fetch('/api/result', {
		method: "POST",
		body: formData
	}).then(() => {
		document.querySelector(".loader").classList.toggle("hidden");
		textUpload.style.display = 'unset';
		location.href = location.href + "result"
	})
})

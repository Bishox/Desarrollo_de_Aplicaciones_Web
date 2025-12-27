const gallery = document.getElementById("gallery");
const imageUrlInput = document.getElementById("image-url");
const addButton = document.getElementById("add-image");
const deleteButton = document.getElementById("delete-selected");

let selectedImage = null;

addButton.addEventListener("click", () => {
  const url = imageUrlInput.value.trim();
  if (url === "") return;

  const img = document.createElement("img");
  img.src = url;
  img.alt = "Imagen agregada";
  img.addEventListener("click", () => selectImage(img));
  
  gallery.appendChild(img);
  imageUrlInput.value = "";
});

deleteButton.addEventListener("click", () => {
  if (selectedImage) {
    selectedImage.remove();
    selectedImage = null;
  }
});

function selectImage(img) {
  if (selectedImage) selectedImage.classList.remove("selected");
  img.classList.add("selected");
  selectedImage = img;
}

imageUrlInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") addButton.click();
});

const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const input_font = document.querySelector("#font_input")
const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");
});

optionsList.forEach(o => {
  o.addEventListener("click", () => {
    selected.innerHTML = o.querySelector("label").innerHTML;
    input_font.value = o.querySelector("label").innerHTML;
    selected.style.fontFamily = input_font.value.split('.')[0]
    optionsContainer.classList.remove("active");
  });
});

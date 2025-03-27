let deleteImage = () => {
    fetch("/free").then(response => {
        if (!response.ok) {
          throw new Error('Error: response is bad');
        }
        return response.json();
      })
      .then(data => console.log(data)) 
      .catch(error => console.error('Error:', error));
}

document.getElementById("uploadForm").addEventListener("submit", function(event) {
  event.preventDefault();
  
  let fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) {
      alert("Please select a file first!");
      return;
  }

  let formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("/", {
      method: "POST",
      body: formData
  })
  .then(response => response.json())
  .then(data => console.log("Success:", data))
  .catch(error => console.error("Error:", error));
});
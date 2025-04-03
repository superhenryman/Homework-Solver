document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  document.getElementById('img').style.display = 'none';
  try {
    const response = await fetch('/', { 
      method: 'POST', 
      body: formData 
    });
    
    if (!response.ok) {
      throw new Error(await response.text());
    }
    
    const data = await response.json();
    
    const answerDiv = document.getElementById("answer");
    answerDiv.innerHTML = data.answer;
    
    const graphImg = document.getElementById("graph-img");
    if (data.graph) {
      graphImg.src = `/graph.png?t=${Date.now()}`;
      graphImg.style.display = 'block';
    } else {
      graphImg.style.display = 'none';
    }
  } catch (error) {
    console.error('Error:', error);
    alert(error.message);
  }
});

document.getElementById('fileInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith('image')) {
      const reader = new FileReader();

      reader.onload = function(e) {
          const img = document.createElement('img');
          img.src = e.target.result; 
          img.style.maxWidth = '100%'; 
          img.style.height = 'auto';
          img.style.display = 'block';
          const imagePreview = document.getElementById('img');
          imagePreview.innerHTML = ''; 
          imagePreview.appendChild(img); 
          imagePreview.style.display = 'block';
          imagePreview.src = e.target.result;
      };
      reader.readAsDataURL(file);
  } else {
      alert('Please upload a valid image file.');
  }
});

document.addEventListener('paste', async (event) => {
  const items = event.clipboardData.items;
  for (let i = 0; i < items.length; i++) {
    if (items[i].type.startsWith('image')) {
      const file = items[i].getAsFile();
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      const fileInput = document.getElementById('fileInput');
      fileInput.files = dataTransfer.files;

      // Trigger the change event
      const changeEvent = new Event('change');
      fileInput.dispatchEvent(changeEvent);

      break; // Exit loop after handling the image
    }
  }
});
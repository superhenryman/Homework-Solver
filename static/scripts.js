// In scripts.js
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  
  try {
    const response = (await fetch('/', {method: 'POST', body: formData})).json();
    console.log(response.answer)
    console.log(response.graph)
    const html = await response.text();
    document.getElementById("results").innerHTML = html;
  } catch (error) {
    console.error('Error:', error);
  }
});
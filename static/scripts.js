const { json } = require("express");

// In scripts.js
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  
  try {
    const response = (await fetch('/', {method: 'POST', body: formData}));
    const jsonData = response.json();
    console.log(jsonData);
    const html = await response.text();
    document.getElementById("results").innerHTML = html;
  } catch (error) {
    console.error('Error:', error);
  }
});
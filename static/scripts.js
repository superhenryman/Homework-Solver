document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  
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
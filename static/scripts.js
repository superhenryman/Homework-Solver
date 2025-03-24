let deleteImage = () => {
    fetch("/free").then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();  // Parse JSON data
      })
      .then(data => console.log(data))  // Use the data from the response
      .catch(error => console.error('There was a problem with the fetch operation:', error));
}
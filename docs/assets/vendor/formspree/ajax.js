<script>
  var form = document.getElementById("ajax-form");
  
  async function handleSubmit(event) {
    event.preventDefault();
    var status = document.querySelector(".sent-message");
    var error = document.querySelector(".error-message");
    var loading = document.querySelector(".loading");
    var data = new FormData(event.target);
    
    loading.style.display = "block"; // Show loading indicator
    
    fetch(event.target.action, {
      method: form.method,
      body: data,
      headers: {
          'Accept': 'application/json'
      }
    }).then(response => {
      loading.style.display = "none"; // Hide loading indicator
      if (response.ok) {
        status.style.display = "block";
        status.textContent = "Thanks for your submission!";
        form.reset();
      } else {
        response.json().then(data => {
          if (Object.hasOwn(data, 'errors')) {
            error.textContent = data["errors"].map(error => error["message"]).join(", ");
          } else {
            error.textContent = "Oops! There was a problem submitting your form";
          }
          error.style.display = "block";
        })
      }
    }).catch(error => {
      loading.style.display = "none"; // Hide loading indicator
      error.textContent = "Oops! There was a problem submitting your form";
      error.style.display = "block";
    });
  }
  
  form.addEventListener("submit", handleSubmit);
</script>

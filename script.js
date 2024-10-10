document.getElementById("prediction-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Show processing message
    document.getElementById("prediction-result").innerHTML = "Processing...";

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Check if the response status is OK
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        // Check if there was an error in the result
        if (result.error) {
            document.getElementById("prediction-result").innerHTML = `Error: ${result.error}`;
        } else {
            // Display the prediction result
            document.getElementById("prediction-result").innerHTML = `
                Your predicted credit score classification is: ${result.prediction} <br>
                Probability: ${JSON.stringify(result.probability)}
            `;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        // Handle the error with a user-friendly message
        document.getElementById("prediction-result").innerHTML = "Error in prediction. Please try again.";
    });
});

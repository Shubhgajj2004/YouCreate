// $(document).ready(function() {
//     $('#editForm').on('submit', function(event) {
//         $.ajax({
//             data : {
//                 name : "Shubh",
//             },
//             type : 'POST',
//             url : '/finalImg'
//         })
//         .done(function(data) {
           
        
//                 // $('#result').text(data.output).show();
                
            
//         });
//         event.preventDefault();
//     });
// });

// const nextBtn = document.getElementById("nextBtn");
// const editForm = document.getElementById("editForm");

// nextBtn.addEventListener("click", function(event) {
//   event.preventDefault();
//   const xhr = new XMLHttpRequest();
//   xhr.open("POST", "/finalImg");
//   xhr.send();
//   xhr.onreadystatechange = function() {
//     if (xhr.readyState === 4 && xhr.status === 200) {
//       console.log(xhr.responseText);
//       // Do something with the response from the Flask API
//     }
//   }
// });


const nextBtn = document.getElementById("nextBtn");
const editForm = document.getElementById("editForm");
const submitTypeField = document.getElementById("submit_type");

nextBtn.addEventListener("click", function(event) {
    event.preventDefault();
    
    // Set the value of the hidden field to "next" to indicate that the form is being submitted
    // through the "Next" button
    submitTypeField.value = "next";
    
    // Submit the form
    editForm.submit();

    // Send an AJAX request to the /finalImg endpoint
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/finalImg");
    xhr.send();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            // Do something with the response from the Flask API
        }
    };
});


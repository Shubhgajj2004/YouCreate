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

var idImg = "0"
const para = document.getElementById("paragraph").value;


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
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // const requestBody = JSON.stringify({ idImg: idImg });

    // Get the value from the element with ID 'ind'
    const indValue = document.getElementById("ind").value;
    
    const title = document.getElementById("title").value;

    // xhr.send(requestBody);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            // Do something with the response from the Flask API
        }
    };

    const requestBody = JSON.stringify({ idImg: idImg, ind: indValue, para:para, title:title });
    xhr.send(requestBody);
});



// const images = document.querySelectorAll('.final-image');
//   images.forEach((image) => {
//     image.addEventListener('click', (event) => {
//       const selectedImageId = event.target.id;
//       fetch('/finalImg', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ selectedImageId: selectedImageId })
//       })
//       .then(response => {
//         // handle the response from the Flask API
//       })
//       .catch(error => {
//         // handle the error
//       });
//     });
//   });


const images = document.querySelectorAll(".final-image");

images.forEach((image) => {
  image.addEventListener("click", function () {
    idImg = image.id;

    // console.log(`Selected image id: ${id}`);
  });
});
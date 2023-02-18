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
  });
});



//Generate  Images using AI


// get the button element
const aiImgBtn = $('#aiImgBtn');

// add a click event listener to the button
aiImgBtn.on('click', () => {
  // get the image elements to hide
  const img0 = $('#0');
  const img1 = $('#1');
  const img2 = $('#2');
  const img3 = $('#3');
  const img4 = $('#4');
  const img5 = $('#5');
  const img6 = $('#6');

  // set the display property of the images to "none"
  img0.attr('src', "static/spinner.png");
  img1.css('display', 'none');
  img2.css('display', 'none');
  img3.css('display', 'none');
  img4.css('display', 'none');
  img5.css('display', 'none');
  img6.css('display', 'none');

  // make an AJAX request to the Flask API
  $.ajax({
    url: '/AiGenerate',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ 'paragraph': $('#paragraph').val() }),
    success: function(data) {
      // update the source attribute of the image elements with the new image URLs
      const img0 = $('#0');
      // const img1 = $('#1');
      // const img2 = $('#2');
      // const img3 = $('#3');
      img0.attr('src', data.img0);
      // img1.attr('src', data.img1);
      // img2.attr('src', data.img2);
      // img3.attr('src', data.img3);
    },
    error: function(xhr, textStatus, errorThrown) {
      console.log('Error: ' + errorThrown);
    }
  });
});

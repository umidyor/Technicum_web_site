//document.addEventListener("DOMContentLoaded", function() {
//  // Duration for showing the loading GIF
//  let loadingTime = 10000; // 15 seconds
//
//  // Function to hide loading GIF and show content
//  function showContent() {
//    document.getElementById('loading-container').style.display = 'none';
//    document.getElementById('content').style.display = 'block';
//  }
//
//  // Show loading GIF initially
//  document.getElementById('loading-container').style.display = 'block';
//  document.getElementById('content').style.display = 'none';
//
//  // Set a timeout to hide the loading GIF after the specified time
//  let timeout = setTimeout(showContent, loadingTime);
//
//  // Check if all content including images has fully loaded
//  window.addEventListener('load', function() {
//    clearTimeout(timeout); // Cancel the timeout if content loads faster
//    showContent();
//  });
//});

document.getElementById('menu-toggle').addEventListener('click', function() {
    var menu = document.getElementById('menu');
    menu.classList.toggle('show');
});


const slides = document.querySelectorAll('#slideshow img');
let slideIndex = 0;

function showSlide(n) {
  slides[slideIndex].style.display = 'none';
  slideIndex = (slideIndex + n + slides.length) % slides.length;
  slides[slideIndex].style.display = 'block';

}

showSlide(0);

setInterval(function() {
    showSlide(1);
}, 3000);


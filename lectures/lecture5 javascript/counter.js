let counter = 0;

function count() {
    counter++;
    document.querySelector('h1').innerHTML = counter;
}

/* addEventListener takes 2 arguments, the event and the function 
which content will be executed after the event selected is completed */
/* DOMContentLoaded waits until all the content on the page is loaded */
document.addEventListener('DOMContentLoaded', function() {
    
    // document.querySelector('button').addEventListener('click', count);
    document.querySelector('button').onclick = count;

    // run count function with an interval of 1000 milisecs or 1 sec
    setInterval(count, 1000);
});
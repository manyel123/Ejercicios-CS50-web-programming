document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit the form to send a new email
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelectorAll("button").forEach(button => button.classList.remove("selected"));
  document.querySelector(`#compose`).classList.add("selected");

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function send_email() {
  // Defines email content
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // console.log(recipients);

  // API to make the request into url /emails wich will actually save the new email into the db
  fetch('/emails', {

    // /emails url needs a post request
    method: 'POST',

    // Turn the JS object literal into a JSON string
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
    // Turns response into a JSON
    .then(response => response.json())
      .then(result => {
        if ("message" in result) {
            // The email was sent successfully!
            load_mailbox('sent');
        }

        if ("error" in result) {
            // If there was an error in sending the email
            // Display the error next to the "To:"
            document.querySelector('#to-text-error-message').innerHTML = result['error']

        }
        // console.log(result);
        // console.log("message" in result);
        // console.log("error" in result);
      })
      
        // Catch the error 
        .catch(error => {
            // Print the error
            console.log(error);
        });
  return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}



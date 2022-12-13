document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit the form to send a new email
  document.querySelector('#compose-form').onsubmit = send_email;

  // 

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  /*
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelectorAll("button").forEach(button => button.classList.remove("selected"));
  document.querySelector(`#compose`).classList.add("selected");*/

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
  
  // If not return statement there will be a JSONDecodeError
  return false;
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Update mailboxes with the latest emails (inbox, sent, archive)
  fetch(`/emails/${mailbox}`)

    // Turns response into a JSON
    .then(response => response.json())

    .then(emails => {

      // Defines elements to be displayed in preview, the name and the size for each element
      const sections_to_display = [['sender', 5], ['subject', 3], ['timestamp', 4]];

      // Defines email content to be displayed in preview
      const email_content_to_display = {
        'sender': 'Sender', 'subject': 'Subject', 'timestamp': 'Date and time', 'read': true
      };
      
      // Appending all emails to display to variable emails
      emails = [email_content_to_display, ...emails];
      
      // Displaying every email
      emails.forEach(email => {

        // Creating a div element for every email
        const row_div_element = document.createElement('div');

        // Creating a row for the read/unread property
        // condition ? exprIfTrue : exprIfFalse
        row_div_element.classList.add("row", "email-line-box", email["read"] ? "read" : "unread");
        
        // Adding first row to display titles
        if (email === email_content_to_display) { row_div_element.id = 'titled-first-row'; }

        // Display every email preview as a new section
        sections_to_display.forEach(
          
          // Displaying a single section
          section => {

            // Taking section properties
            const section_name = section[0];
            const section_size = section[1];

            // Opening a div element for the new section
            const div_section = document.createElement('div');
            // Setting section properties
            div_section.classList.add(`col-${section_size}`, `${section_name}-section`);
            // Closing div element
            div_section.innerHTML = `<p>${email[section_name]}</p>`;
            
            // Adding the new section as a a new row
            row_div_element.append(div_section);

          });/* WAITING TO CODE load_email FUNCTION
        if (email !== artificial_first_email) {
          row_div_element.addEventListener('click', () => load_email(email["id"], mailbox));
        }*/
        
        // Adds every email to display as a div element
        document.querySelector('#emails-view').append(row_div_element);
      })

    })
    // Catch the error 
    .catch(error => {
      // Print the error
      console.log(error);
    });
}

function archive_email(email_id, archive) {
  // API to make the request into url /emails/<int:email_id> which get the particular email we need to update
  fetch(`/emails/${email_id}`, {

      // Method for updating a value
      method: 'PUT',

      // Turn the JS object literal into a JSON string
      body: JSON.stringify({

          // Updating the value "archived" will archive or unarchive an email
          archived: archive 
      })
  
  // After updating it will load inbox page
  }).then( () => load_mailbox("inbox"));
}
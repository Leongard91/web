document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  
});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields (or prefill if reply)
  if (email.sender == undefined) {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.slice(0, 4) === "Re: ") {
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `\n\n\nOn ${email.timestamp} ${email.sender} wrote: \n${email.body}`;
  }

  document.querySelector('#compose-form').onsubmit = () => {
    let n_body = document.querySelector('#compose-body').value.replace(/\n/g, '<br>');
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: n_body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });

    setTimeout(() => {load_mailbox('sent');}, 300);
    return false;
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get mailgox API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      // Create a box
      const row = document.createElement('div');
      const col1 = document.createElement('div');
      const col2 = document.createElement('div');
      const col3 = document.createElement('div');
      row.className = 'row';
      col1.className = 'col1';
      col3.className = 'col';
      col1.innerHTML = email.sender;
      col2.innerHTML = email.subject;
      col3.innerHTML = email.timestamp;
      row.appendChild(col1);
      row.appendChild(col2);
      row.appendChild(col3);

      // Check is unread
      if (email.read === true) {
        row.style.backgroundColor = 'rgb(240, 240, 240)';
      };

      // View email
      row.addEventListener('click', () => email_view(email.id));

      document.querySelector('#emails-view').append(row);
    });
  });


}

function email_view(email_id) {

  // Get mail API
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Enter email in email-view
    document.querySelector('#sender').innerHTML = email.sender;
    document.querySelector('#to').innerHTML = email.recipients;
    document.querySelector('#subject').innerHTML = email.subject;
    document.querySelector('#timestamp').innerHTML = email.timestamp;
    document.querySelector('#email_body').innerHTML = email.body;

    // Mark the email as read
    if (email.read == false) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    }

    // Reply button
    document.querySelector('#unarchive').style.display = 'block';
    document.querySelector('#reply').onclick = function() {
      compose_email(email);
    }

    // Archive(Unarchive) button
    if (email.sender === document.querySelector('h2').innerHTML) {
      document.querySelector('#unarchive').style.display = 'none';
      document.querySelector('#archive').style.display = 'none';
    } else{
      if (email.archived == false) {
        document.querySelector('#unarchive').style.display = 'none';
        document.querySelector('#archive').style.display = 'block';
        document.querySelector('#archive').onclick = function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT', 
            body: JSON.stringify({
              archived: true
            })
          });
          setTimeout(() => {load_mailbox('inbox');}, 300);
          return false;
        };
      } else if (email.archived == true) {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display = 'block';
        document.querySelector('#unarchive').onclick = function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT', 
            body: JSON.stringify({
              archived: false
            })
          });
          setTimeout(() => {load_mailbox('inbox');}, 300);
          return false;
        };
      }
    }
    
    // Show email, hide other
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

  });
}


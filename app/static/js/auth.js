// Sign In Data-Callback
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  var name = profile.getName();
  console.log('Name: ' + name);
  var email = profile.getEmail()
  console.log('Email: ' + email); // This is null if the 'email' scope is not present.
  // Send ID token to server to authorize
  var id_token = googleUser.getAuthResponse().id_token;
  console.log(id_token);
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/login');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    console.log('Signed in as: ' + xhr.responseText);
  };
  xhr.send('idtoken=' + id_token);
}

// Google Sign Out
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
    $('#signinButton').attr('style', 'display: block');
  });
  $.ajax({
    method: 'POST',
    url: '/logout'
  })
}

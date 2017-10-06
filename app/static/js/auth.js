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
  var data = {"idtoken": id_token}
  console.log(id_token);

  $.ajax({
    type: "POST",
    url: "/login",
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function(){
      $('#signOutButton').show();
      $('#signInButton').hide();
    }
  })
}

// Google Sign Out
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
  $.ajax({
    type: "GET",
    url: "/logout",
    success: function(){
      location.reload();
      $('#signOutButton').hide();
      $('#signInButton').show();
    }
  })
}

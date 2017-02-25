// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
  console.log('statusChangeCallback', response);
  if (response.status === 'connected') {
    login(response);
  } else if (response.status === 'not_authorized') {
    alert('Please log into this app');
  } else {
    alert('Please log into Facebook');
  }
}


function getProtectedPage(token) {
  var settings = {
    url: '/something-protected',
    headers: {
      'Authorization': 'JWT ' + token
    },
  };
  $.ajax(settings).then(function(resp){
    $("#protected").html(resp)
  }).catch(function(err){
    console.log(err);
    $("#protected").html('There was an error: <br/>' + err.responseText);
  });
}


function login(response){
  var userId = response.authResponse.userID;
  var accessToken = response.authResponse.accessToken;
  $.post('/login',
    {access_token: accessToken, user_id: userId},
    function(resp) {
      if (resp.result === 'ok') {
        $('#check_jwt textarea').html(resp.token);
        $('#login-button').hide();
        $('#restricted').attr('disabled', false).click(function(event){
          event.stopPropagation();
          getProtectedPage(resp.token);
          return false;
        });
      } else {
        alert('Bad response from backend');
      }
    }
  )
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

$(document).ready(function(){

  $.getScript('//connect.facebook.net/en_US/sdk.js', function(){
    FB.init({
      appId: appid,
      version: 'v2.7' // or v2.1, v2.2, v2.3, ...
    });
    $('#loginbutton,#feedbutton').removeAttr('disabled');
    FB.getLoginStatus(statusChangeCallback);
  });

  $('#login-button').click(function(){
    FB.login(statusChangeCallback, {scope: 'public_profile,email'});
    return false;
  });
});

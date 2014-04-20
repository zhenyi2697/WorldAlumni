/*
 * Query user's locatio and nearby schoolmates
 *
 * copyright zhenyi2697
 * Updated 04/20/2014
 *
*/


  // use html 5 to load location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showLocation, showLocationError);
  } else {
    loadErrorMessage("Sorry, Geolocation is not supported by your browser, maybe you could consider using a more advanced one ;)");
  }

  function showLocation(location) {
      $("#latitude").html(location.coords.latitude);
      $("#longitude").html(location.coords.longitude);

      $("#current-location").show();
      $(".find-friend-div").show();
      $("#location-error-message").hide();
      $("#loading-message").hide();
  }

  function loadErrorMessage(message) {
    $("#location-error-message").html(message);
    $("#location-error-message").show();
  }

  function showLocationError(error) {

    var message = ""
    switch(error.code) {
      case error.PERMISSION_DENIED:
        message = "Sorry, we cannot give your nearby friends without knowing your location -_- ...";
        break;
      case error.POSITION_UNAVAILABLE:
        message = "Sorry, we cannot get your current location, try refresh the page ;)";
        break;
      case error.TIMEOUT:
        message = "Location request timedout, retry please ;)";
        break;
      case error.UNKNOWN_ERROR:
        message = "Somethings wierd happens, refresh page please ;)"
        break;
    }
    loadErrorMessage(message);
    $("#current-location").hide();
    $("#loading-message").hide();
  }

  var load_friends = function(friends){

    var rows = [];
    var row_data = "";
    var f;

    if (friends.length <= 1) {
      $("#friend-message").html("It seems that you are the only one around here, come back later!");
    } else {
      $("#friend-message").html("We have found "+ (friends.length - 1) +" schoolmates for you");
    }

    for (var i = 0; i < friends.length; i++) {
      f = friends[i];
      row_data = "<tr>";
      if (f.provider == 'facebook') {
        row_data += "<td><img src='"+ f.image_url +"?width=40&height=40' alt='"+f.firstName+"' class='img-circle friend-thumbnail'/></td>";
        row_data += "<td><a href='http://www.facebook.com/"+ f.uid  +"' target='_blank'>"+ f.first_name + " "+ f.last_name +"</a></td>";
      } else {
        row_data += "<td><img src='"+ f.image_url + "' style='width:40px;height:40px;' class='img-circle friend-thumbnail' /></td>";
        row_data += "<td>"+ f.first_name + " "+ f.last_name +"</td>";
      }

      if (f.associated_attendances.length > 0 && f.attendances.length > 0 ) {
        row_data += "<td>" +f.associated_attendances[0].school + "</td>";
      } else {
        row_data += "<td></td>";
      }

      row_data += "<td class='hidden-xs'>"+ f.distance +"</td>";
      row_data += "<td class='hidden-xs'>"+ f.appear_time +"</td>";
      row_data += "<td class='visible-xs'>"+ f.distance +" ("+ f.appear_time +")</td>";

      rows.push(row_data);
    }
    var html = rows.join();
    $("#friend-table").html(html);
  }

  var user_nearby = function(){
    var latitude =  $("#latitude").html();
    var longitude =  $("#longitude").html();

    post_params = {
      'bindingId': bindingId,
      'longitude': longitude,
      'latitude': latitude
    }

    $.post('/api/nearby_users/', post_params).done(function(d){
      console.log(d);
      $("#sent_result").html("Your location has been sent to server")
      load_friends(d);
    }, 'json');

  }

  var updateSetting = function(entryId){

    var value = 0;
    if (entryId == 1) {

      if($("#distance_only_input").is(':checked') ) {
        value = 1;
      } else {
        value = 0;
      }

    } else if (entryId == 2) {

      if( $("#invisible_input").is(':checked') ) {
        value = 1;
      } else {
        value = 0;
      }

    }

    post_params = {
      'bindingId': bindingId,
      'entryId': entryId,
      'value': value
    }

    $.post('/api/'+bindingId+'/settings/', post_params).done(function(d){
      console.log(d);
    }, 'json');

  }

